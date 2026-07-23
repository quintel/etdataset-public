"""
Plausibility validation for emissions data.

Checks value plausibility:
- Non-negative emissions (outside LULUCF/Waste)
- Total = CO2 + other_ghg
- Subsector sums match parent totals
- Sector 1 is largest energy emitter
- Year-over-year ratios are reasonable
"""

from __future__ import annotations
from pathlib import Path
import pandas as pd

from ..sources.unfccc_excel import UFCCCExcelSource
from .models import (
    DatasetInfo,
    EmissionTotals,
    ValidationResult,
    ExcelSheetTotals,
    ExcelValidationResult,
)
from ..config import (
    COL_OUT_CODE,
    COL_OUT_CO2,
    COL_OUT_OTHER,
    COL_OUT_TOTAL,
    REQUIRED_CODES,
    EXCLUDED_NEGATIVE_SECTORS,
    NEGATIVE_THRESHOLD,
    SUBSECTOR_MISMATCH_TOLERANCE,
    MAX_YEAR_RATIO,
    MOBILE_MACHINERY_CRT_CODES,
    CRT_CODE_RE,
    FISHING_CRT_CODE,
)


def validate_outputs(
    saved: list[Path],
    output_dir: Path,
    nl_folder: str = "nl",
) -> tuple[list[str], list[str]]:
    """
    Plausibility checks on pipeline output values.

    All checks return warnings (soft failures):
    1. CO2 and other_ghg non-negative (outside LULUCF/Waste)
    2. total_ghg = co2 + other_ghg
    3. Subsector CO2 sums match parent totals
    4. Sector 1 (Energy) is largest CO2 emitter
    5. NL off-road codes are non-null and non-zero
    6. Year-over-year ratios are reasonable

    Args:
        saved: List of saved file paths
        output_dir: Base output directory
        nl_folder: Folder name for NL datasets

    Returns:
        Tuple of (fails, warns) lists (all issues are warns)
    """
    fails: list[str] = []
    warns: list[str] = []

    by_folder: dict[str, list[Path]] = _group_by_folder(saved, output_dir)

    for fpath in sorted(saved):
        df = pd.read_csv(fpath)
        label = fpath.relative_to(output_dir)

        if not {COL_OUT_CODE, COL_OUT_CO2, COL_OUT_OTHER}.issubset(df.columns):
            continue

        df = df.copy()
        df[COL_OUT_CODE] = df[COL_OUT_CODE].astype(str)

        _check_non_negative(df, label, warns)
        _check_total_sum(df, label, warns)
        _check_subsector_sums(df, label, warns)
        _check_sector1_largest(df, label, warns)
        _check_nl_offroad_nonzero(fpath, output_dir, nl_folder, df, label, warns)

    _check_year_ratios(by_folder, warns)

    return fails, warns


# ── Private check functions ───────────────────────────────────────────────────


def _group_by_folder(
    saved: list[Path],
    output_dir: Path,
) -> dict[str, list[Path]]:
    """Group files by dataset folder."""
    by_folder: dict[str, list[Path]] = {}
    for fpath in saved:
        dataset_folder = fpath.relative_to(output_dir).parts[0]
        by_folder.setdefault(dataset_folder, []).append(fpath)
    return by_folder


def _check_non_negative(
    df: pd.DataFrame,
    label: Path,
    warns: list[str],
) -> None:
    """Check CO2 and other_ghg are non-negative."""
    crt_rows = df[df[COL_OUT_CODE].str.match(CRT_CODE_RE)]
    non_excluded = crt_rows[
        ~crt_rows[COL_OUT_CODE].str.startswith(EXCLUDED_NEGATIVE_SECTORS)
    ]

    for col, label_str in [(COL_OUT_CO2, "CO2"), (COL_OUT_OTHER, "other GHG")]:
        neg = non_excluded[
            non_excluded[col].notna() & (non_excluded[col] < NEGATIVE_THRESHOLD)
        ]
        for _, row in neg.iterrows():
            warns.append(
                f"NEGATIVE {label_str}  {label}: {row[COL_OUT_CODE]} = {row[col]:.1f}"
            )


def _check_total_sum(
    df: pd.DataFrame,
    label: Path,
    warns: list[str],
) -> None:
    """Check total_ghg = co2 + other_ghg."""
    if COL_OUT_TOTAL not in df.columns:
        return

    has_all = df[[COL_OUT_CO2, COL_OUT_OTHER, COL_OUT_TOTAL]].notna().all(axis=1)
    for _, row in df[has_all].iterrows():
        expected_total = row[COL_OUT_CO2] + row[COL_OUT_OTHER]
        if abs(row[COL_OUT_TOTAL] - expected_total) > 0.01:
            warns.append(
                f"TOTAL MISMATCH  {label}: {row[COL_OUT_CODE]} "
                f"total={row[COL_OUT_TOTAL]:.2f} ≠ CO2+other={expected_total:.2f}"
            )


def _check_subsector_sums(
    df: pd.DataFrame,
    label: Path,
    warns: list[str],
) -> None:
    """Check subsector sums match parent totals."""
    co2_by_code = {
        row[COL_OUT_CODE]: (row[COL_OUT_CO2] if pd.notna(row[COL_OUT_CO2]) else 0.0)
        for _, row in df.iterrows()
        if CRT_CODE_RE.match(str(row[COL_OUT_CODE]))
    }

    children_of: dict[str, list[str]] = {}
    for code in co2_by_code:
        parent = _parent_code(code)
        if parent and parent in co2_by_code:
            children_of.setdefault(parent, []).append(code)

    for parent, children in children_of.items():
        if parent.startswith(EXCLUDED_NEGATIVE_SECTORS) or len(parent) == 1:
            continue
        if parent.count(".") >= 3:
            continue

        parent_val = co2_by_code[parent]
        children_sum = sum(co2_by_code[c] for c in children)

        if abs(parent_val) > 1:
            diff = abs(children_sum - parent_val) / abs(parent_val)
            if diff > SUBSECTOR_MISMATCH_TOLERANCE:
                warns.append(
                    f"SUBSECTOR MISMATCH to be solved in 2.7: {label}: {parent} = {parent_val:.1f}, "
                    f"children sum = {children_sum:.1f} ({diff:.0%} diff)"
                )


def _check_sector1_largest(
    df: pd.DataFrame,
    label: Path,
    warns: list[str],
) -> None:
    """Check Sector 1 is largest CO2 emitter."""
    top = df[df[COL_OUT_CODE].isin(REQUIRED_CODES - set(EXCLUDED_NEGATIVE_SECTORS))]
    if top.empty:
        return

    s1_row = top[top[COL_OUT_CODE] == "1"][COL_OUT_CO2]
    s1_val = s1_row.iloc[0] if not s1_row.empty and pd.notna(s1_row.iloc[0]) else 0.0

    others = top[top[COL_OUT_CODE] != "1"][COL_OUT_CO2].dropna()
    if not others.empty and s1_val < others.max():
        max_code = top.loc[top[COL_OUT_CO2] == others.max(), COL_OUT_CODE].iloc[0]
        warns.append(
            f"SECTOR 1 NOT LARGEST  {label}: "
            f"sector 1 = {s1_val:.1f}, sector {max_code} = {others.max():.1f}"
        )


def _check_nl_offroad_nonzero(
    fpath: Path,
    output_dir: Path,
    nl_folder: str,
    df: pd.DataFrame,
    label: Path,
    warns: list[str],
) -> None:
    """Check NL off-road codes are non-null and non-zero."""
    if fpath.relative_to(output_dir).parts[0] != nl_folder:
        return

    for code in MOBILE_MACHINERY_CRT_CODES:
        row = df[df[COL_OUT_CODE] == code]
        if not row.empty:
            val = row.iloc[0][COL_OUT_CO2]
            if pd.isna(val) or val == 0:
                warns.append(f"NL OFF-ROAD ZERO/NULL  {label}: {code}")


def _check_year_ratios(
    by_folder: dict[str, list[Path]],
    warns: list[str],
) -> None:
    """Check year-over-year emission ratios."""
    for folder, fpaths in by_folder.items():
        totals: dict[int, float] = {}

        for fpath in fpaths:
            df = pd.read_csv(fpath)
            if not {COL_OUT_CODE, COL_OUT_CO2}.issubset(df.columns):
                continue

            df[COL_OUT_CODE] = df[COL_OUT_CODE].astype(str)
            s1 = df[df[COL_OUT_CODE] == "1"][COL_OUT_CO2]

            if not s1.empty and pd.notna(s1.iloc[0]):
                suffix = fpath.stem.split("_")[-1]
                if suffix.isdigit():
                    # e.g. intermediate_emissions_1990.csv → base year 1990
                    year = int(suffix)
                else:
                    # intermediate_emissions_default.csv holds the analysis year,
                    # which is the year directory in the path:
                    # data/<dataset>/<analysis_year>/15_emissions/<file>
                    try:
                        year = int(fpath.parts[-3])
                    except (IndexError, ValueError):
                        continue
                totals[year] = float(s1.iloc[0])

        if 1990 in totals and totals[1990] != 0:
            base = totals[1990]
            for yr, val in totals.items():
                if yr == 1990:
                    continue
                ratio = val / base
                if ratio > MAX_YEAR_RATIO or ratio < 1 / MAX_YEAR_RATIO:
                    warns.append(
                        f"SIGNIFICANT YEAR RATIO to manually check {folder}: sector-1 CO2 {yr}/1990 = {ratio:.2f}× "
                        f"(1990={base:.1f}, {yr}={val:.1f})"
                    )


def _parent_code(code: str) -> str | None:
    """Return direct parent CRT code."""
    parts = code.split(".")
    return ".".join(parts[:-1]) if len(parts) > 1 else None


def _parse_dataset_info(fpath: Path) -> DatasetInfo | None:
    """
    Extract dataset information from emissions file path.

    Parses the file path to extract dataset name and year, and handles
    NL dataset mapping to correct UNFCCC API filenames.

    Args:
        fpath: Path to emissions.csv file

    Returns:
        DatasetInfo if path is valid, None otherwise
    """
    # Path structure: .../data/{dataset}/{year}/15_emissions/emissions.csv
    parts = fpath.parts

    # Skip if not emissions.csv
    if fpath.name != "emissions.csv":
        return None

    # Extract dataset name
    try:
        dataset_idx = parts.index("data") + 1
        dataset = parts[dataset_idx]
    except (ValueError, IndexError):
        return None

    # Extract year
    try:
        year_idx = dataset_idx + 1
        year = int(parts[year_idx])
    except (ValueError, IndexError):
        return None

    # Map NL datasets to correct UNFCCC API filename based on year
    # All NL datasets use folder "nl" but have different UNFCCC API filenames
    dataset_for_unfccc = dataset
    if dataset == "nl":
        if year == 2015:
            dataset_for_unfccc = "nl"
        elif year == 2019:
            dataset_for_unfccc = "nl2019"
        elif year == 2023:
            dataset_for_unfccc = "nl2023"

    return DatasetInfo(
        dataset=dataset, year=year, dataset_for_unfccc=dataset_for_unfccc
    )


def _calculate_emissions_totals(
    df_emissions: pd.DataFrame, year: int
) -> EmissionTotals | None:
    """
    Calculate emission totals for a given year from emissions DataFrame.

    Filters out indirect emissions, international transport, and LULUCF sector
    as per UNFCCC reporting conventions.

    Args:
        df_emissions: DataFrame from emissions.csv
        year: Year to calculate totals for (typically 1990)

    Returns:
        EmissionTotals if data exists, None otherwise
    """
    # Filter for specified year
    df_year = df_emissions[df_emissions["year"] == year]

    if df_year.empty:
        return None

    # Exclude: indirect emissions, international transport, entire LULUCF sector
    df_filtered = df_year[
        ~(
            # Exclude indirect emissions
            (df_year["etm_sector"] == "Other")
            & (df_year["etm_subsector"] == "Indirect emissions")
            & (df_year["use"] == "non_energetic")
        )
        & ~(
            # Exclude international transport
            (df_year["etm_sector"] == "Bunkers")
        )
        & ~(
            # Exclude entire LULUCF sector
            (df_year["etm_sector"] == "LULUCF")
        )
    ]

    # Calculate totals
    co2 = df_filtered[df_filtered["ghg"] == "co2"]["value"].sum()
    other_ghg = df_filtered[df_filtered["ghg"] == "other_ghg"]["value"].sum()
    total_ghg = co2 + other_ghg

    return EmissionTotals(co2=co2, other_ghg=other_ghg, total_ghg=total_ghg)


def _load_unfccc_totals(
    dataset_info: DatasetInfo, source_analyses_dir: Path
) -> EmissionTotals | None:
    """
    Load UNFCCC reported totals from API input file.

    Reads the UNFCCC API input file and extracts "Total GHG emissions without LULUCF"
    for the dataset's analysis year. For NL the reported fishing total is
    subtracted, mirroring the pipeline's NL-only fishing exclusion, so the
    comparison is like-for-like.

    Args:
        dataset_info: Dataset information
        source_analyses_dir: Path to source_analyses directory

    Returns:
        EmissionTotals if data found, None otherwise
    """
    # Build path to UNFCCC API file
    unfccc_path = (
        source_analyses_dir
        / dataset_info.dataset
        / str(dataset_info.year)
        / "15_emissions"
        / f"input_emissions_UNFCCC_API_{dataset_info.dataset_for_unfccc}.csv"
    )

    if not unfccc_path.exists():
        return None

    # Read UNFCCC data
    df_unfccc = pd.read_csv(unfccc_path)

    # Extract reported totals for 1990
    # Filter for: "Total GHG emissions without LULUCF" + "Net emissions/removals" + year=1990
    df_totals = df_unfccc[
        (df_unfccc["category"] == "Total GHG emissions without LULUCF")
        & (df_unfccc["classification"] == "Total for category")
        & (df_unfccc["measure"] == "Net emissions/removals")
        & (df_unfccc["year"] == 1990)
    ]

    # Extract CO2
    co2_rows = df_totals[df_totals["gas"] == "CO2"]
    if co2_rows.empty:
        return None
    co2 = co2_rows.iloc[0]["numberValue"]

    # Extract Aggregate GHGs
    ghg_rows = df_totals[df_totals["gas"] == "Aggregate GHGs"]
    if ghg_rows.empty:
        return None
    total_ghg = ghg_rows.iloc[0]["numberValue"]

    # For NL the pipeline excludes fishing (FISHING_CRT_CODE) via _exclude_fishing,
    # while the UNFCCC "Total GHG without LULUCF" still includes it. Subtract the
    # reported fishing total here so the reference is like-for-like with the output.
    if dataset_info.dataset == "nl":
        fishing_co2, fishing_total = _unfccc_category_total(
            df_unfccc, FISHING_CRT_CODE, year=1990
        )
        co2 -= fishing_co2
        total_ghg -= fishing_total

    # Calculate other GHG
    other_ghg = total_ghg - co2

    return EmissionTotals(co2=co2, other_ghg=other_ghg, total_ghg=total_ghg)


def _unfccc_category_total(
    df_unfccc: pd.DataFrame, crt_code: str, year: int
) -> tuple[float, float]:
    """
    Return (co2, aggregate_ghg) reported for a single CRT category and year.

    Matches the category by its leading CRT code (the UNFCCC "category" column
    is formatted as "<code>  <name>", e.g. "1.A.4.c.iii  Fishing"), using the
    "Total for category" / "Net emissions/removals" rows. Missing values return
    0.0 so callers can subtract unconditionally.
    """
    codes = df_unfccc["category"].astype(str).str.split(n=1).str[0]
    rows = df_unfccc[
        (codes == crt_code)
        & (df_unfccc["classification"] == "Total for category")
        & (df_unfccc["measure"] == "Net emissions/removals")
        & (df_unfccc["year"] == year)
    ]

    co2_rows = rows[rows["gas"] == "CO2"]
    ghg_rows = rows[rows["gas"] == "Aggregate GHGs"]

    co2 = float(co2_rows.iloc[0]["numberValue"]) if not co2_rows.empty else 0.0
    total_ghg = float(ghg_rows.iloc[0]["numberValue"]) if not ghg_rows.empty else 0.0

    return co2, total_ghg


def _compare_emission_totals(
    source1: EmissionTotals,
    source2: EmissionTotals,
    threshold: float,
) -> tuple[dict[str, float | None], bool, list[tuple[str, float, float]]]:
    """
    Generic emission totals comparison.

    Compares two EmissionTotals objects and returns comparison data.
    Caller is responsible for formatting warnings with appropriate context.

    Args:
        source1: First emission totals (e.g., calculated or Summary2)
        source2: Second emission totals (e.g., reported or detailed)
        threshold: Maximum acceptable relative difference

    Returns:
        Tuple of (relative_diffs, passed, mismatches)
        - relative_diffs: Dict of gas type to relative difference (or None)
        - passed: Whether all differences are within threshold
        - mismatches: List of (label, val1, val2) tuples exceeding threshold
    """
    comparisons = [
        ("CO2", source1.co2, source2.co2),
        ("other GHG", source1.other_ghg, source2.other_ghg),
        ("total GHG", source1.total_ghg, source2.total_ghg),
    ]

    rel_diffs = {}
    for label, val1, val2 in comparisons:
        if val2 == 0:
            rel_diffs[label] = None
        else:
            rel_diffs[label] = abs(val1 - val2) / abs(val2)

    max_diff = max((d for d in rel_diffs.values() if d is not None), default=0)
    passed = max_diff <= threshold

    mismatches = [
        (label, val1, val2)
        for label, val1, val2 in comparisons
        if (val2 == 0 and abs(val1) > 0.1)
        or (val2 != 0 and abs(val1 - val2) / abs(val2) > threshold)
    ]

    return rel_diffs, passed, mismatches


def _compare_totals(
    dataset: str,
    calculated: EmissionTotals,
    reported: EmissionTotals,
    threshold: float,
) -> ValidationResult:
    """
    Compare calculated vs reported emission totals.

    Args:
        dataset: Dataset name for result
        calculated: Calculated emission totals
        reported: Reported emission totals from UNFCCC
        threshold: Maximum acceptable relative difference (e.g., 0.01 for 1%)

    Returns:
        ValidationResult with comparison data and warnings
    """
    rel_diffs, passed, mismatches = _compare_emission_totals(
        calculated, reported, threshold
    )

    warnings = []
    for label, calc_val, rep_val in mismatches:
        if rep_val == 0:
            warnings.append(
                f"1990 UNFCCC MISMATCH  {dataset} {label}: "
                f"calculated={calc_val:.1f} kt, reported=0.0 kt"
            )
        else:
            rel_diff = abs(calc_val - rep_val) / abs(rep_val)
            warnings.append(
                f"1990 UNFCCC MISMATCH  {dataset} {label}: "
                f"calculated={calc_val:.1f} kt, reported={rep_val:.1f} kt "
                f"({rel_diff:.1%} diff)"
            )

    return ValidationResult(
        dataset=dataset,
        calculated=calculated,
        reported=reported,
        relative_diffs=rel_diffs,
        passed=passed,
        warnings=warnings,
    )


def _format_percentage_diffs(
    rel_diffs: dict[str, float | None],
) -> tuple[str, str, str]:
    """
    Format relative differences as percentage strings.

    Args:
        rel_diffs: Dict mapping gas type to relative difference (or None)

    Returns:
        Tuple of (co2_pct, other_ghg_pct, total_ghg_pct) formatted strings
    """
    co2_pct = f"{rel_diffs['CO2']:.2%}" if rel_diffs.get("CO2") is not None else "N/A"
    other_pct = (
        f"{rel_diffs['other GHG']:.2%}"
        if rel_diffs.get("other GHG") is not None
        else "N/A"
    )
    total_pct = (
        f"{rel_diffs['total GHG']:.2%}"
        if rel_diffs.get("total GHG") is not None
        else "N/A"
    )
    return co2_pct, other_pct, total_pct


def _format_validation_result(result: ValidationResult) -> str:
    """
    Format validation result as a print line.

    Args:
        result: Validation result to format

    Returns:
        Formatted string for printing
    """
    co2_pct, other_pct, total_pct = _format_percentage_diffs(result.relative_diffs)
    status = "✓" if result.passed else "⚠"

    return (
        f"  {status}  {result.dataset:25} CO2={co2_pct:>6}, "
        f"other_ghg={other_pct:>6}, total={total_pct:>6}"
    )


def validate_1990_unfccc_totals(
    final_emissions_files: list[Path],
    source_analyses_dir: Path,
    datasets_with_unfccc: dict[str, str],
    threshold: float = 0.01,
) -> tuple[list[str], list[str]]:
    """
    Validate 1990 emissions totals against UNFCCC API source data.

    Compares the sum of emissions from final emissions.csv files against
    the "Total GHG emissions without LULUCF" reported totals from UNFCCC API
    input files for 1990.

    For each dataset with UNFCCC API data:
    1. Sum CO2 and other_ghg from emissions.csv for year=1990, excluding:
       - "Other,Indirect emissions,non_energetic"
       - "International transport" sector (reported separately as "International Bunkers")
       - Entire "LULUCF" sector (reported separately as "with LULUCF")
    2. Extract reported totals from input_emissions_UNFCCC_API_{dataset}.csv
       using "Total GHG emissions without LULUCF"
    3. Calculate relative differences
    4. Warn if any difference exceeds threshold (default 1%)

    Args:
        final_emissions_files: List of emissions.csv file paths
        source_analyses_dir: Path to source_analyses directory
        datasets_with_unfccc: Dict mapping dataset names to UNFCCC codes
        threshold: Maximum acceptable relative difference (default 0.01 = 1%)

    Returns:
        Tuple of (fails, warns) lists (all issues are warns)
    """
    fails: list[str] = []
    warns: list[str] = []

    for fpath in final_emissions_files:
        # Parse dataset information from path
        dataset_info = _parse_dataset_info(fpath)
        if not dataset_info:
            continue

        # Skip datasets without UNFCCC API data
        if dataset_info.dataset_for_unfccc not in datasets_with_unfccc:
            continue

        # Calculate emissions totals from emissions.csv
        df_emissions = pd.read_csv(fpath)
        calculated = _calculate_emissions_totals(df_emissions, year=1990)
        if not calculated:
            continue

        # Load UNFCCC reported totals
        reported = _load_unfccc_totals(dataset_info, source_analyses_dir)
        if not reported:
            warns.append(
                f"UNFCCC FILE MISSING  {dataset_info.dataset_for_unfccc}: "
                f"Expected input_emissions_UNFCCC_API_{dataset_info.dataset_for_unfccc}.csv"
            )
            continue

        # Compare calculated vs reported
        result = _compare_totals(
            dataset_info.dataset_for_unfccc, calculated, reported, threshold
        )

        # Print comparison results
        print(_format_validation_result(result))

        # Add warnings if validation failed
        warns.extend(result.warnings)

    return fails, warns


def _load_excel_summary2_totals(excel_path: Path, year: int) -> ExcelSheetTotals | None:
    """
    Extract emission totals from Summary2 sheet of UNFCCC CRT Excel file.

    Sums the top-level sectors 1, 2, 3, 5 (excluding LULUCF) using the shared
    Summary2 parser on UFCCCExcelSource, so validation reads the sheet exactly
    the same way the fetch pipeline does.

    Args:
        excel_path: Path to UNFCCC CRT Excel file
        year: Year to extract (should match file year)

    Returns:
        ExcelSheetTotals if Summary2 sheet found and parsed, None otherwise
    """
    totals = UFCCCExcelSource.summary2_totals(excel_path, year)
    if totals is None:
        return None

    co2_total, other_ghg_total = totals

    return ExcelSheetTotals(
        co2=co2_total,
        other_ghg=other_ghg_total,
        total_ghg=co2_total + other_ghg_total,
        sheet_name="Summary2",
    )


def validate_excel_final_emissions(
    final_emissions_files: list[Path],
    excel_datasets: dict[str, list[tuple[int, Path]]],
    threshold: float = 0.01,
) -> tuple[list[str], list[str]]:
    """
    Validate final emissions for Excel-sourced datasets against Summary2 sheet totals.

    For datasets sourced from UNFCCC CRT Excel files (not API), validates that
    final emissions.csv totals match Summary2 sheet totals.

    Note: Excel CRT files don't contain "Total GHG without LULUCF" reported
    totals, so we can only validate internal consistency between final output
    and Summary2 sheet, not against external ground truth like the API route.

    Validation checks:
    1. Calculate totals from final emissions.csv (excluding LULUCF, intl transport, indirect)
    2. Extract totals from Summary2 sheet (sectors 1, 2, 3, 5)
    3. Compare the two
    4. Warn if relative difference exceeds threshold (default 1%)

    Args:
        final_emissions_files: List of emissions.csv file paths
        excel_datasets: Dict mapping dataset name to [(year, excel_path), ...]
        threshold: Maximum acceptable relative difference (default 0.01 = 1%)

    Returns:
        Tuple of (fails, warns) lists (all issues are warns)
    """
    fails: list[str] = []
    warns: list[str] = []

    # Build lookup: (dataset, year) -> excel_path
    excel_lookup: dict[tuple[str, int], Path] = {}
    for dataset, year_files in excel_datasets.items():
        for year, excel_path in year_files:
            excel_lookup[(dataset, year)] = excel_path

    # Build lookup: dataset -> final_emissions_path
    dataset_to_final: dict[str, Path] = {}
    for fpath in final_emissions_files:
        dataset_info = _parse_dataset_info(fpath)
        if dataset_info:
            dataset_to_final[dataset_info.dataset_for_unfccc] = fpath

    # Iterate through Excel datasets and validate each year
    # NOTE: Only validate 1990 base year data, because analysis year data has
    # GHG filtering applied (config_etm_sector_include_ghg.csv) which makes
    # comparison against unfiltered Summary2 totals meaningless
    for dataset, year_files in excel_datasets.items():
        if dataset not in dataset_to_final:
            continue

        final_path = dataset_to_final[dataset]
        df_emissions = pd.read_csv(final_path)

        for data_year, excel_path in year_files:
            # Skip non-1990 years (analysis year has GHG filtering applied)
            if data_year != 1990:
                continue

            # Calculate emissions totals from final emissions.csv for 1990
            calculated = _calculate_emissions_totals(df_emissions, year=1990)
            if not calculated:
                continue

            # Load Summary2 sheet totals from Excel
            summary = _load_excel_summary2_totals(excel_path, 1990)
            if not summary:
                warns.append(
                    f"EXCEL SUMMARY2 MISSING  {dataset}: "
                    f"Summary2 sheet not found/parseable"
                )
                continue

            # Convert Summary2 totals to EmissionTotals for comparison
            summary_totals = EmissionTotals(
                co2=summary.co2,
                other_ghg=summary.other_ghg,
                total_ghg=summary.total_ghg,
            )

            # Compare final emissions vs Summary2
            rel_diffs, passed, mismatches = _compare_emission_totals(
                calculated, summary_totals, threshold
            )

            # Format and print result
            co2_pct, other_pct, total_pct = _format_percentage_diffs(rel_diffs)
            status = "✓" if passed else "⚠"
            print(
                f"  {status}  {dataset:25} CO2={co2_pct:>6}, "
                f"other_ghg={other_pct:>6}, total={total_pct:>6}"
            )

            # Add warnings for mismatches
            for label, calc_val, sum_val in mismatches:
                if sum_val == 0:
                    warns.append(
                        f"EXCEL MISMATCH  {dataset} {label}: "
                        f"final={calc_val:.1f} kt, Summary2=0.0 kt"
                    )
                else:
                    rel_diff = abs(calc_val - sum_val) / abs(sum_val)
                    warns.append(
                        f"EXCEL MISMATCH  {dataset} {label}: "
                        f"final={calc_val:.1f} kt, Summary2={sum_val:.1f} kt "
                        f"({rel_diff:.1%} diff)"
                    )

    return fails, warns
