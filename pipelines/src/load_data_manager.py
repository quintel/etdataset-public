import pandas as pd
from pathlib import Path
from typing import Dict, Optional, List
import importlib


class LoadDataManager:
    """Unified module for loading and combining ETLocal data"""

    def __init__(self, data_dir: str = "data/intermediate", sep: str = ","):
        """
        Initialize the data module

        Args:
            data_dir: Directory containing data files
            sep: CSV separator (default: ",")
        """
        self.data_dir = Path(data_dir)
        self.sep = sep

        # Define file paths once to avoid repetition
        self.file_paths = {
            "template": "ETLocal_template_empty_2025.csv",
            "km_data": "km_source_data_converted.csv",
            "km_meta": "km_meta_data_converted.csv",
            "km_nl_data": "km_national_source_data_converted.csv",
            "km_nl_meta": "km_national_meta_data_converted.csv",
            "transport": "transport_research_cleaned.csv",
            "miscellaneous": "miscellaneous_data_analysis.csv",
            "etm_queries": "etm_query_combined.csv",
            "electric_cars": "shares_cars_road_transport_gasoline_electricity.csv",
        }

    def _load_csv(
        self, file_key: str, index_col: Optional[str] = None, sep: Optional[str] = None
    ) -> pd.DataFrame:
        """
        Generic CSV loader

        Args:
            file_key: Key from self.file_paths
            index_col: Column to use as index
            sep: Override default separator

        Returns:
            Loaded DataFrame
        """
        file_path = self.data_dir / self.file_paths[file_key]
        separator = sep if sep is not None else self.sep
        return pd.read_csv(file_path, sep=separator, index_col=index_col)

    def _transpose_with_headers(
        self, df: pd.DataFrame, skip_rows: int = 1
    ) -> pd.DataFrame:
        """
        Transpose dataframe and use first row as column headers

        Args:
            df: DataFrame to transpose
            skip_rows: Number of rows to skip after setting headers

        Returns:
            Transposed DataFrame
        """
        df_transposed = df.transpose()
        df_transposed.columns = df_transposed.iloc[0]
        return df_transposed[skip_rows:].reset_index(drop=True)

    def load_template(self, group: Optional[str] = None) -> pd.DataFrame:
        """
        Load and prepare the ETLocal template

        Args:
            group: Optional group to filter by (e.g., 'buildings', 'households', 'transport')

        Returns:
            DataFrame with the (filtered) template
        """
        df = self._load_csv("template")

        # Set the multi-level index
        df.set_index(["geo_id", "group", "subgroup", "key"], inplace=True)

        # Set proper data types
        df["value"] = df["value"].astype("float64")
        df["commit"] = df["commit"].astype("str")

        # Filter by group if specified
        if group:
            df = df.loc[(slice(None), group, slice(None), slice(None)), :].copy()

        return df

    def load_klimaatmonitor_data(self) -> Dict[str, pd.DataFrame]:
        """Load all Klimaatmonitor data (municipality and national)"""
        return {
            "km_data": self._load_csv("km_data", index_col="GemeenteCode"),
            "km_meta": self._load_csv("km_meta", index_col="ivar"),
            "km_nl_data": self._load_csv("km_nl_data"),
            "km_nl_meta": self._load_csv("km_nl_meta", index_col="ivar"),
        }

    def load_transport_data(self) -> pd.DataFrame:
        """Load and prepare transport research data"""
        df_raw = self._load_csv("transport")
        return self._transpose_with_headers(df_raw)

    def load_miscellaneous_data(self) -> pd.DataFrame:
        """Load and prepare miscellaneous data (Transport-compatible)"""
        df = self._load_csv("miscellaneous")

        # Set first column as index and rename to match KM data
        df.set_index(df.columns[0], inplace=True)
        df.index.name = "GemeenteCode"  # Standardize index name

        return df

    def load_etm_queries(self) -> pd.DataFrame:
        """Load and prepare ETM query data (Transport-compatible)"""
        # Load with semicolon separator to match the transport notebook
        df_raw = self._load_csv("etm_queries", sep=",")

        # Transpose and set headers like the transport notebook
        df_transposed = df_raw.transpose()
        df_transposed.columns = df_transposed.iloc[1]  # Use row 1 for headers
        outcome = df_transposed[2:].reset_index(drop=True)  # Skip first 2 rows

        # Fix duplicate columns by removing duplicates (keep first occurrence)
        outcome = outcome.loc[:, ~outcome.columns.duplicated()]

        return outcome

    def load_electric_cars_distribution(self) -> pd.DataFrame:
        """Load and prepare electric cars distribution data"""
        file_path = self.data_dir / self.file_paths["electric_cars"]

        # Check if file exists, if not return empty DataFrame
        if not file_path.exists():
            print(
                f"Warning: {file_path} not found. This file is generated during transport processing."
            )
            return pd.DataFrame()

        df = pd.read_csv(file_path, sep=",", index_col=0)  # Note: uses comma separator
        return df

    def create_co2_emission_factors(
        self,
        pure_gasoline: float = 3.073,
        pure_diesel: float = 3.468,
        tank_gasoline: float = 2.821,
        tank_diesel: float = 3.256,
    ) -> pd.DataFrame:
        """
        Create CO2 emission factors DataFrame for transport calculations

        Args:
            pure_gasoline: CO2 factor for pure gasoline (fossiel E0)
            pure_diesel: CO2 factor for pure diesel (fossiel B0)
            tank_gasoline: CO2 factor for tank gasoline (E10)
            tank_diesel: CO2 factor for tank diesel (B7)

        Returns:
            DataFrame with CO2 emission factors
        """

        def bio_ethanol_in_bio_fuels(
            pure_gasoline, pure_diesel, tank_gasoline, tank_diesel
        ):
            # Calculate the share of biofuel in gasoline and diesel
            share_biofuel_gasoline = 1 - (tank_gasoline / pure_gasoline)
            share_biofuel_benzine = 1 - (tank_diesel / pure_diesel)
            # Return the share of biogasoline in biofuels as a percentage
            return share_biofuel_gasoline / (
                share_biofuel_gasoline + share_biofuel_benzine
            )

        return pd.DataFrame(
            data={
                "share_bio_ethanol_in_bio_fuels": bio_ethanol_in_bio_fuels(
                    pure_gasoline, pure_diesel, tank_gasoline, tank_diesel
                )
            },
            index=["value"],
        )

    def load_all_data(
        self,
        include_miscellaneous: bool = True,
        include_etm_queries: bool = True,
        include_electric_cars: bool = True,
        include_co2_factors: bool = True,
    ) -> Dict[str, pd.DataFrame]:
        """
        Load all data sources at once

        Args:
            include_miscellaneous: Whether to load miscellaneous data
            include_etm_queries: Whether to load ETM queries
            include_electric_cars: Whether to load electric cars distribution
            include_co2_factors: Whether to create CO2 emission factors

        Returns:
            Dictionary with all loaded data
        """
        data = {}

        # Load Klimaatmonitor data
        data.update(self.load_klimaatmonitor_data())

        # Load transport data
        data["transport"] = self.load_transport_data()

        # Load optional data sources
        if include_miscellaneous:
            data["miscellaneous"] = self.load_miscellaneous_data()

        if include_etm_queries:
            data["etm_queries"] = self.load_etm_queries()

        if include_electric_cars:
            data["electric_cars"] = self.load_electric_cars_distribution()

        if include_co2_factors:
            data["co2_factors"] = self.create_co2_emission_factors()

        return data

    def combine_municipality_data(
        self,
        km_data: Optional[pd.DataFrame] = None,
        misc_data: Optional[pd.DataFrame] = None,
    ) -> Optional[pd.DataFrame]:
        """
        Combine municipality-level data sources (Transport-specific version)

        Args:
            km_data: Klimaatmonitor municipality data
            misc_data: Miscellaneous municipality data

        Returns:
            Combined municipality data or None if no data provided
        """
        if km_data is None and misc_data is None:
            return None

        if km_data is None:
            return misc_data

        if misc_data is None:
            # Clean up KM data - remove unwanted columns
            km_cleaned = km_data.drop(
                columns=["Gemeentenaam", "ProvinciecodePV", "Provincienaam"],
                errors="ignore",
            )
            return km_cleaned

        # Combine both datasets
        combined = pd.concat([km_data, misc_data], axis=1)

        # Clean up unwanted columns
        combined = combined.drop(
            columns=["Gemeentenaam", "ProvinciecodePV", "Provincienaam"],
            errors="ignore",
        )

        return combined

    def combine_national_data(
        self,
        km_nl_data: Optional[pd.DataFrame] = None,
        transport_data: Optional[pd.DataFrame] = None,
        etm_data: Optional[pd.DataFrame] = None,
        co2_data: Optional[pd.DataFrame] = None,
    ) -> Optional[pd.DataFrame]:
        """
        Combine national-level data sources (Transport-specific version)

        Args:
            km_nl_data: Klimaatmonitor national data
            transport_data: Transport data
            etm_data: ETM query data
            co2_data: CO2 emission factors data

        Returns:
            Combined national data or None if no data provided
        """
        sources = []

        if km_nl_data is not None:
            # Skip first column of KM national data
            sources.append(km_nl_data.iloc[:, 1:])

        if transport_data is not None:
            # Take only first row
            sources.append(transport_data.iloc[[0]])

        if etm_data is not None:
            # Take only first row and reset index
            etm_single_row = etm_data.iloc[[0]].reset_index(drop=True)
            sources.append(etm_single_row)

        if co2_data is not None:
            # Reset index for CO2 data
            co2_reset = co2_data.reset_index(drop=True)
            sources.append(co2_reset)

        if not sources:
            return None

        return pd.concat(sources, axis=1)

    def create_transport_input_vars(
        self,
        include_miscellaneous: bool = True,
        include_etm_queries: bool = True,
        include_co2_factors: bool = True,
    ) -> pd.DataFrame:
        """
        Create the df_input_vars DataFrame exactly as done in Transport notebook

        This replicates the complex transformation logic from the Transport notebook
        where multiple data sources are combined in a specific way.

        Returns:
            DataFrame with all input variables ready for Transport calculations
        """
        # Load all data sources
        data = self.load_all_data(
            include_miscellaneous=include_miscellaneous,
            include_etm_queries=include_etm_queries,
            include_electric_cars=False,
            include_co2_factors=include_co2_factors,
        )

        # Step 1: Combine municipality data (KM + miscellaneous)
        # This replicates the df_gm_vars logic from Transport notebook
        df_gm_vars = data["km_data"].copy()

        if include_miscellaneous and "miscellaneous" in data:
            df_gm_vars = pd.concat([df_gm_vars, data["miscellaneous"]], axis=1)

        # Clean up unwanted columns (Transport notebook pattern)
        df_gm_vars = df_gm_vars.drop(
            columns=["Gemeentenaam", "ProvinciecodePV", "Provincienaam"],
            errors="ignore",
        )

        # Step 2: Combine national data (KM_NL + transport + ETM + CO2)
        # This replicates the df_nl_vars logic from Transport notebook
        national_sources = []

        # Add KM national data (skip first column)
        if "km_nl_data" in data:
            national_sources.append(data["km_nl_data"].iloc[:, 1:])

        # Add transport research data (first row only)
        if "transport" in data:
            national_sources.append(data["transport"].iloc[[0]])

        # Add ETM queries (first row, reset index)
        if include_etm_queries and "etm_queries" in data:
            etm_single_row = data["etm_queries"].iloc[[0]].reset_index(drop=True)
            national_sources.append(etm_single_row)

        # Add CO2 factors
        if include_co2_factors and "co2_factors" in data:
            co2_reset = data["co2_factors"].reset_index(drop=True)
            national_sources.append(co2_reset)

        # Combine all national sources
        if national_sources:
            df_nl_vars = pd.concat(national_sources, axis=1)
        else:
            df_nl_vars = pd.DataFrame()

        # Step 3: Broadcast national data to all municipalities
        # This replicates the exact logic from Transport notebook
        if not df_nl_vars.empty:
            nl_vars_series = df_nl_vars.iloc[0]

            nl_vars_df = pd.DataFrame(
                [nl_vars_series.values] * len(df_gm_vars),  # repeat the numpy array
                index=df_gm_vars.index,
                columns=nl_vars_series.index,  # keep column names
            )

            # Drop overlapping columns to avoid conflicts
            nl_vars_df = nl_vars_df.drop(
                columns=set(nl_vars_df.columns) & set(df_gm_vars.columns),
                errors="ignore",
            )

            # Final concatenation
            df_input_vars = pd.concat([df_gm_vars, nl_vars_df], axis=1)
        else:
            df_input_vars = df_gm_vars

        return df_input_vars

    def get_legacy_data_objects(self) -> Dict[str, pd.DataFrame]:
        """
        Get individual data objects as they were loaded in the original Transport notebook

        This method provides backwards compatibility for notebooks that expect
        individual dataframes like df_ivar_data, df_ivar_nl_data, etc.

        Returns:
            Dictionary with individual dataframes using original naming
        """
        data = self.load_all_data(
            include_miscellaneous=True,
            include_etm_queries=True,
            include_electric_cars=True,
            include_co2_factors=True,
        )

        legacy_objects = {}

        # KM municipality data
        if "km_data" in data:
            legacy_objects["df_ivar_data"] = data["km_data"]

        # KM municipality metadata
        if "km_meta" in data:
            legacy_objects["df_ivar_meta_data"] = data["km_meta"]

        # KM national data
        if "km_nl_data" in data:
            legacy_objects["df_ivar_nl_data"] = data["km_nl_data"]

        # KM national metadata
        if "km_nl_meta" in data:
            legacy_objects["df_ivar_nl_meta_data"] = data["km_nl_meta"]

        # Transport research data
        if "transport" in data:
            legacy_objects["df_ivar_tr_data"] = data["transport"]

        # Miscellaneous data
        if "miscellaneous" in data:
            legacy_objects["df_ivar_ms_data"] = data["miscellaneous"]

        # ETM queries
        if "etm_queries" in data:
            legacy_objects["df_ivar_eq_data"] = data["etm_queries"]

        # CO2 factors
        if "co2_factors" in data:
            legacy_objects["df_ivar_CO_data"] = data["co2_factors"]

        # Electric cars distribution (if exists)
        if "electric_cars" in data and not data["electric_cars"].empty:
            legacy_objects["electric_cars_shares"] = data["electric_cars"]

        return legacy_objects

    def get_metadata(self, source: str = "km") -> pd.DataFrame:
        """
        Get metadata for a specific source

        Args:
            source: 'km' for municipality or 'km_nl' for national

        Returns:
            Metadata DataFrame
        """
        if source == "km":
            return self._load_csv("km_meta", index_col="ivar")
        elif source == "km_nl":
            return self._load_csv("km_nl_meta", index_col="ivar")
        else:
            raise ValueError(f"Unknown metadata source: {source}")

    def reload_modules(self, modules: List[str]):
        """Reload specified modules (for development)"""
        for module_name in modules:
            try:
                module = importlib.import_module(module_name)
                importlib.reload(module)
                print(f"Reloaded module: {module_name}")
            except ImportError:
                print(f"Warning: Could not reload module '{module_name}'")

    # Keep all existing methods for backwards compatibility
    def combine_all_data(
        self,
        include_miscellaneous: bool = True,
        include_etm_queries: bool = True,
        include_electric_cars: bool = True,
    ) -> pd.DataFrame:
        """
        Load and combine all data sources into a single DataFrame (Original method for backwards compatibility)

        Args:
            include_miscellaneous: Whether to include miscellaneous data
            include_etm_queries: Whether to include ETM queries
            include_electric_cars: Whether to include electric cars distribution

        Returns:
            Combined DataFrame with all data
        """
        # Load all data
        data = self.load_all_data(
            include_miscellaneous, include_etm_queries, include_electric_cars
        )

        # Combine municipality data (original method)
        municipality_data = self._combine_municipality_data_original(
            km_data=data.get("km_data"),
            misc_data=data.get("miscellaneous") if include_miscellaneous else None,
            electric_cars_data=(
                data.get("electric_cars") if include_electric_cars else None
            ),
        )

        # Combine national data (original method)
        national_data = self._combine_national_data_original(
            km_nl_data=data.get("km_nl_data"),
            transport_data=data.get("transport"),
            etm_data=data.get("etm_queries") if include_etm_queries else None,
        )

        # Merge municipality and national data (original method)
        return self._merge_municipality_and_national_original(
            municipality_data, national_data
        )

    def _combine_municipality_data_original(
        self,
        km_data: Optional[pd.DataFrame] = None,
        misc_data: Optional[pd.DataFrame] = None,
        electric_cars_data: Optional[pd.DataFrame] = None,
    ) -> Optional[pd.DataFrame]:
        """
        Combine municipality-level data sources (original method, refactored for OOP/SOLID/DRY).
        """
        sources = self._collect_municipality_sources(
            km_data, misc_data, electric_cars_data
        )
        if not sources:
            return None

        if len(sources) == 1:
            name, data = sources[0]
            return self._standardize_single_source(name, data)

        dataframes = [data for _, data in sources]
        allowed_codes = self._get_allowed_municipality_codes(dataframes)
        filtered_codes = self._get_filtered_codes(dataframes, allowed_codes)
        reindexed_dfs = self._reindex_dataframes(dataframes, filtered_codes)
        combined = pd.concat(reindexed_dfs, axis=1)
        combined = self._consolidate_name_columns(combined)
        return combined

    def _collect_municipality_sources(
        self,
        km_data: Optional[pd.DataFrame],
        misc_data: Optional[pd.DataFrame],
        electric_cars_data: Optional[pd.DataFrame],
    ) -> list:
        """Collect and rename municipality data sources to avoid column conflicts."""
        sources = []
        if km_data is not None:
            km_renamed = km_data.rename(columns={"Gemeentenaam": "Gemeentenaam_KM"})
            sources.append(("KM", km_renamed))
        if misc_data is not None:
            misc_renamed = misc_data.rename(
                columns={"Gemeentenaam": "Gemeentenaam_misc"}
            )
            sources.append(("misc", misc_renamed))
        if electric_cars_data is not None:
            sources.append(("electric_cars", electric_cars_data))
        return sources

    def _standardize_single_source(self, name: str, data: pd.DataFrame) -> pd.DataFrame:
        """Standardize single source dataframe by renaming name column if needed."""
        col_mapping = {"KM": "Gemeentenaam_KM", "misc": "Gemeentenaam_misc"}
        if name in col_mapping:
            return data.rename(columns={col_mapping[name]: "Gemeentenaam"})
        return data

    def _get_allowed_municipality_codes(self, dataframes: list) -> pd.Index:
        """Load allowed municipality codes from reference Excel, fallback to union of indices."""
        ref_path = Path("data/raw/Gemeenten alfabetisch 2023.xlsx")
        try:
            ref_df = pd.read_excel(ref_path)
            code_col = next(
                (col for col in ref_df.columns if str(col).lower() == "gemeentecodegm"),
                ref_df.columns[0],
            )
            return pd.Index(ref_df[code_col].astype(str))
        except Exception:
            allowed_codes = dataframes[0].index
            for df in dataframes[1:]:
                allowed_codes = allowed_codes.union(df.index)
            return allowed_codes

    def _get_filtered_codes(
        self, dataframes: list, allowed_codes: pd.Index
    ) -> pd.Index:
        """Get intersection of all municipality codes and allowed codes."""
        all_codes = dataframes[0].index
        for df in dataframes[1:]:
            all_codes = all_codes.union(df.index)
        return all_codes.intersection(allowed_codes)

    def _reindex_dataframes(self, dataframes: list, filtered_codes: pd.Index) -> list:
        """Reindex all dataframes to filtered codes."""
        return [df.reindex(filtered_codes) for df in dataframes]

    def _combine_national_data_original(
        self,
        km_nl_data: Optional[pd.DataFrame] = None,
        transport_data: Optional[pd.DataFrame] = None,
        etm_data: Optional[pd.DataFrame] = None,
    ) -> Optional[pd.DataFrame]:
        """
        Combine national-level data sources

        Args:
            km_nl_data: Klimaatmonitor national data
            transport_data: Transport data
            etm_data: ETM query data

        Returns:
            Combined national data or None if no data provided
        """
        sources = []

        if km_nl_data is not None:
            # Skip first column of KM national data
            sources.append(km_nl_data.iloc[:, 1:])

        if transport_data is not None:
            # Take only first row
            sources.append(transport_data.iloc[[0]])

        if etm_data is not None:
            # Take only first row and reset index
            sources.append(etm_data.iloc[[0]].reset_index(drop=True))

        if not sources:
            return None

        return pd.concat(sources, axis=1)

    def _consolidate_name_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Consolidate multiple municipality name columns into one

        Args:
            df: DataFrame with multiple name columns

        Returns:
            DataFrame with single consolidated name column
        """
        # Find all name columns
        name_cols = [col for col in df.columns if col.startswith("Gemeentenaam")]

        if not name_cols:
            return df

        # Prioritize KM data, otherwise use first available
        primary_col = (
            "Gemeentenaam_KM" if "Gemeentenaam_KM" in name_cols else name_cols[0]
        )

        # Create consolidated column
        df["Gemeentenaam"] = df[primary_col]
        for col in name_cols:
            if col != primary_col:
                df["Gemeentenaam"] = df["Gemeentenaam"].combine_first(df[col])

        # Remove temporary columns
        df = df.drop(columns=name_cols)

        # Reorder to put name first
        cols = ["Gemeentenaam"] + [col for col in df.columns if col != "Gemeentenaam"]
        return df[cols]

    def _merge_municipality_and_national_original(
        self,
        municipality_data: Optional[pd.DataFrame],
        national_data: Optional[pd.DataFrame],
    ) -> pd.DataFrame:
        """
        Merge municipality and national data

        Args:
            municipality_data: Municipality-level data
            national_data: National-level data

        Returns:
            Merged DataFrame
        """
        # Handle edge cases
        if municipality_data is None and national_data is None:
            raise ValueError("At least one data source must be provided")

        if municipality_data is None:
            return national_data

        if national_data is None:
            return municipality_data

        # Check for column conflicts
        national_cols = set(national_data.columns)
        municipality_cols = set(municipality_data.columns)
        overlapping = national_cols & municipality_cols

        if overlapping:
            print(f"Warning: Overlapping columns found: {overlapping}")

        # Broadcast national data to all municipalities
        national_values = national_data.iloc[0]
        national_broadcast = pd.DataFrame(
            [national_values] * len(municipality_data),
            index=municipality_data.index,
            columns=national_values.index,
        )

        # Combine
        return pd.concat([municipality_data, national_broadcast], axis=1)
