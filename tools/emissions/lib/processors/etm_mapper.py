"""
CRT to ETM sector mapping and transformations.

Maps Common Reporting Table (CRT) categories to Energy Transition Model (ETM)
sectors, handles LULUCF splitting, and applies GHG filtering.
"""

from __future__ import annotations
from pathlib import Path
import pandas as pd
import logging

from ..config import FISHING_CRT_CODE


class ETMMapper:
    """Map CRT categories to ETM sectors with aggregation and filtering."""

    def __init__(
        self,
        mapping_df: pd.DataFrame,
        ghg_config_df: pd.DataFrame | None = None,
    ):
        """
        Initialize mapper.

        Args:
            mapping_df: CRT to ETM mapping (crt_code, etm_sector, etm_subsector, use)
            ghg_config_df: GHG inclusion config (optional, for filtering)
        """
        self.mapping_df = mapping_df.copy()
        self.mapping_df["crt_code"] = self.mapping_df["crt_code"].astype(str)
        self.ghg_config_df = ghg_config_df

    def map_crt_to_etm(
        self,
        intermediate_df: pd.DataFrame,
        dataset: str,
        include_parents: bool = False,
        is_nl_dataset: bool = False,
    ) -> pd.DataFrame:
        """
        Map CRT codes to ETM sectors with aggregation.

        Args:
            intermediate_df: Intermediate emissions data with CRT codes
            dataset: Dataset name (for logging)
            include_parents: If True, sum ALL matched codes (parent + children)
            is_nl_dataset: If True, exclude fishing (1.A.4.c.iii)

        Returns:
            DataFrame aggregated by (etm_sector, etm_subsector, use)
            with columns: co2, other_ghg
        """
        df = intermediate_df.copy()
        df["crt_code"] = df["crt_code"].astype(str)

        df = self._fix_industry_categories(df)
        if is_nl_dataset:
            df = self._exclude_fishing(df)

        results = self._map_categories(df, include_parents)
        aggregated = self._aggregate_results(results)

        return aggregated

    def split_lulucf(self, agg_df: pd.DataFrame) -> pd.DataFrame:
        """
        Split LULUCF CO2 into Removals and Emissions subsectors.

        Transformation:
        - Negative CO2 (removals) → "Removals" subsector with abs(value)
        - Positive/zero CO2 → "Emissions" subsector with original value
        - other_ghg always goes to "Emissions"

        Args:
            agg_df: Aggregated DataFrame with (etm_sector, etm_subsector, use, co2, other_ghg)

        Returns:
            DataFrame with LULUCF split into Removals and Emissions
        """
        df = agg_df.copy()
        lulucf_mask = df["etm_sector"] == "LULUCF"
        lulucf_rows = df[lulucf_mask]

        if lulucf_rows.empty:
            logging.warning("No LULUCF rows found - skipping split")
            return df

        df_without_lulucf = df[~lulucf_mask]
        new_rows = self._create_lulucf_split_rows(lulucf_rows)

        result = pd.concat(
            [df_without_lulucf, pd.DataFrame(new_rows)], ignore_index=True
        )
        result_agg = result.groupby(
            ["etm_sector", "etm_subsector", "use"], as_index=False
        ).agg({"co2": "sum", "other_ghg": "sum"})

        logging.info(
            f"Split LULUCF: created {len(new_rows)} rows from {len(lulucf_rows)} original"
        )
        return result_agg

    def filter_ghg(
        self, agg_df: pd.DataFrame, always_include_co2: bool = False
    ) -> pd.DataFrame:
        """
        Filter emissions by GHG inclusion rules and convert to long format.

        Args:
            agg_df: Aggregated DataFrame (etm_sector, etm_subsector, use, co2, other_ghg)
            always_include_co2: When False (default, used for the analysis year),
                only CO2/other_ghg allowed by config_etm_sector_include_ghg.csv are
                kept and sectors without a config entry are dropped (inner join).
                When True (used for 1990 baseline data), all CO2 is preserved
                regardless of the include_co2 config and sectors without a config
                entry are retained (left join), while invalid other_ghg
                combinations are still filtered out.

        Returns:
            Long-format DataFrame (etm_sector, etm_subsector, use, ghg, unit, value)
        """
        if self.ghg_config_df is None:
            return self._to_long_format(agg_df, filter_ghg=False)

        ghg_cfg = self.ghg_config_df.copy()
        ghg_cfg["etm_subsector"] = ghg_cfg["etm_subsector"].fillna("")

        how = "left" if always_include_co2 else "inner"
        merged = agg_df.merge(
            ghg_cfg, on=["etm_sector", "etm_subsector", "use"], how=how
        )

        output_rows = []
        for _, row in merged.iterrows():
            if always_include_co2 or row["include_co2"]:
                output_rows.append(self._create_output_row(row, "co2", row["co2"]))

            # Include other_ghg when config allows it; for rows without a config
            # entry (only possible on the left join) default to including it.
            include_other_ghg = row["include_other_ghg"]
            if pd.isna(include_other_ghg) or include_other_ghg:
                output_rows.append(
                    self._create_output_row(row, "other_ghg", row["other_ghg"])
                )

        return pd.DataFrame(output_rows)

    # ── Private methods ───────────────────────────────────────────────────────

    def _fix_industry_categories(self, df: pd.DataFrame) -> pd.DataFrame:
        """Fix industry category codes (2.B.8, 2.B.10)."""
        for parent, fallback in [("2.B.8", "2.B.8.g"), ("2.B.10", "2.B.10.b")]:
            has_parent = (df["crt_code"] == parent).any()
            has_children = df["crt_code"].str.startswith(parent + ".").any()
            if has_parent and not has_children:
                df.loc[df["crt_code"] == parent, "crt_code"] = fallback
        return df

    def _exclude_fishing(self, df: pd.DataFrame) -> pd.DataFrame:
        """Exclude fishing category for NL datasets."""
        fishing_parent_code = FISHING_CRT_CODE.rsplit(".", 1)[0]
        exclude_mask = (
            (df["crt_code"] == FISHING_CRT_CODE)
            | df["crt_code"].str.startswith(FISHING_CRT_CODE + ".")
            | (df["crt_code"] == fishing_parent_code)
        )
        return df[~exclude_mask]

    def _map_categories(
        self,
        df: pd.DataFrame,
        include_parents: bool,
    ) -> list[dict]:
        """Map CRT codes to ETM sectors."""
        results = []

        for _, map_row in self.mapping_df.iterrows():
            map_code = map_row["crt_code"]
            etm_sector = map_row["etm_sector"]
            etm_subsector = (
                map_row["etm_subsector"] if pd.notna(map_row["etm_subsector"]) else ""
            )
            use = map_row["use"]

            mask = (df["crt_code"] == map_code) | df["crt_code"].str.startswith(
                map_code + "."
            )
            matched = df[mask]

            if not matched.empty:
                co2_val, other_val = self._aggregate_matched(
                    matched, map_code, include_parents, etm_sector, etm_subsector
                )
            else:
                co2_val, other_val = float("nan"), float("nan")

            results.append(
                {
                    "etm_sector": etm_sector,
                    "etm_subsector": etm_subsector,
                    "use": use,
                    "co2": co2_val,
                    "other_ghg": other_val,
                }
            )

        return results

    def _aggregate_matched(
        self,
        matched: pd.DataFrame,
        map_code: str,
        include_parents: bool,
        etm_sector: str,
        etm_subsector: str,
    ) -> tuple[float, float]:
        """Aggregate matched CRT codes."""
        codes = matched["crt_code"].tolist()

        if include_parents:
            return self._sum_all(matched)

        parent_row = matched[matched["crt_code"] == map_code]
        parent_exists = not parent_row.empty and (
            parent_row["co2"].notna().any() or parent_row["other_ghg"].notna().any()
        )

        if parent_exists:
            return self._use_parent(
                parent_row, matched, map_code, codes, etm_sector, etm_subsector
            )

        return self._sum_leaves(matched, codes)

    def _sum_all(self, matched: pd.DataFrame) -> tuple[float, float]:
        """Sum all matched codes (UKNI strategy)."""
        co2_val = matched["co2"].sum() if matched["co2"].notna().any() else float("nan")
        other_val = (
            matched["other_ghg"].sum()
            if matched["other_ghg"].notna().any()
            else float("nan")
        )
        return co2_val, other_val

    def _use_parent(
        self,
        parent_row: pd.DataFrame,
        matched: pd.DataFrame,
        map_code: str,
        codes: list[str],
        etm_sector: str,
        etm_subsector: str,
    ) -> tuple[float, float]:
        """Use parent value and validate against children."""
        co2_val = (
            parent_row["co2"].iloc[0]
            if parent_row["co2"].notna().any()
            else float("nan")
        )
        other_val = (
            parent_row["other_ghg"].iloc[0]
            if parent_row["other_ghg"].notna().any()
            else float("nan")
        )

        children = matched[matched["crt_code"] != map_code]
        if not children.empty:
            child_codes = children["crt_code"].tolist()
            self._validate_parent_children(
                co2_val,
                other_val,
                children,
                child_codes,
                map_code,
                etm_sector,
                etm_subsector,
            )

        return co2_val, other_val

    def _validate_parent_children(
        self,
        co2_val: float,
        other_val: float,
        children: pd.DataFrame,
        child_codes: list[str],
        map_code: str,
        etm_sector: str,
        etm_subsector: str,
    ) -> None:
        """Validate parent value against sum of leaf children."""
        leaf_mask = [
            not any(c.startswith(code + ".") for c in child_codes if c != code)
            for code in child_codes
        ]
        leaf_children = children[leaf_mask]

        child_co2_sum = (
            leaf_children["co2"].sum() if leaf_children["co2"].notna().any() else 0
        )
        child_other_sum = (
            leaf_children["other_ghg"].sum()
            if leaf_children["other_ghg"].notna().any()
            else 0
        )

        co2_diff = abs((co2_val or 0) - child_co2_sum)
        other_diff = abs((other_val or 0) - child_other_sum)
        threshold = 0.0001

        if co2_diff > threshold or other_diff > threshold:
            logging.info(
                f"Using parent value for {map_code} -> {etm_sector}/{etm_subsector}: "
                f"parent CO2={co2_val:.2f} vs leaf sum={child_co2_sum:.2f}, "
                f"parent other_ghg={other_val:.2f} vs leaf sum={child_other_sum:.2f}"
            )

    def _sum_leaves(
        self, matched: pd.DataFrame, codes: list[str]
    ) -> tuple[float, float]:
        """Sum only leaf nodes."""
        leaf_mask = [
            not any(c.startswith(code + ".") for c in codes if c != code)
            for code in codes
        ]
        codes_to_use = matched[leaf_mask]

        co2_val = (
            codes_to_use["co2"].sum()
            if codes_to_use["co2"].notna().any()
            else float("nan")
        )
        other_val = (
            codes_to_use["other_ghg"].sum()
            if codes_to_use["other_ghg"].notna().any()
            else float("nan")
        )
        return co2_val, other_val

    def _aggregate_results(self, results: list[dict]) -> pd.DataFrame:
        """Aggregate mapping results by ETM category."""
        pre_agg_df = pd.DataFrame(results)
        return pre_agg_df.groupby(
            ["etm_sector", "etm_subsector", "use"], as_index=False
        ).agg({"co2": "sum", "other_ghg": "sum"})

    def _create_lulucf_split_rows(self, lulucf_rows: pd.DataFrame) -> list[dict]:
        """Create split LULUCF rows."""
        new_rows = []

        for _, row in lulucf_rows.iterrows():
            co2_val = row["co2"] if pd.notna(row["co2"]) else 0
            other_ghg_val = row["other_ghg"] if pd.notna(row["other_ghg"]) else 0

            if co2_val < 0:
                new_rows.append(
                    {
                        "etm_sector": "LULUCF",
                        "etm_subsector": "Removals",
                        "use": row["use"],
                        "co2": abs(co2_val),
                        "other_ghg": 0,
                    }
                )
                new_rows.append(
                    {
                        "etm_sector": "LULUCF",
                        "etm_subsector": "Emissions",
                        "use": row["use"],
                        "co2": 0,
                        "other_ghg": 0,
                    }
                )
            else:
                new_rows.append(
                    {
                        "etm_sector": "LULUCF",
                        "etm_subsector": "Removals",
                        "use": row["use"],
                        "co2": 0,
                        "other_ghg": 0,
                    }
                )
                new_rows.append(
                    {
                        "etm_sector": "LULUCF",
                        "etm_subsector": "Emissions",
                        "use": row["use"],
                        "co2": co2_val,
                        "other_ghg": 0,
                    }
                )

            if other_ghg_val != 0:
                new_rows.append(
                    {
                        "etm_sector": "LULUCF",
                        "etm_subsector": "Emissions",
                        "use": row["use"],
                        "co2": 0,
                        "other_ghg": other_ghg_val,
                    }
                )

        return new_rows

    def _to_long_format(self, agg_df: pd.DataFrame, filter_ghg: bool) -> pd.DataFrame:
        """Convert aggregated format to long format."""
        output_rows = []
        for _, row in agg_df.iterrows():
            output_rows.append(self._create_output_row(row, "co2", row["co2"]))
            output_rows.append(
                self._create_output_row(row, "other_ghg", row["other_ghg"])
            )
        return pd.DataFrame(output_rows)

    @staticmethod
    def _create_output_row(row: pd.Series, ghg: str, value: float) -> dict:
        """Create output row in long format."""
        return {
            "etm_sector": row["etm_sector"],
            "etm_subsector": row["etm_subsector"],
            "use": row["use"],
            "ghg": ghg,
            "unit": "kton CO2-eq",
            "value": value,
        }
