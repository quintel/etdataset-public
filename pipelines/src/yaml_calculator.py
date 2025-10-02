import pandas as pd
import yaml
from typing import Any, Dict, Optional, List


class YamlCalculator:
    """
    Class to calculate ETLocal keys based on YAML definitions and a pandas DataFrame of base variables.
    This version recognizes:
    1. String or numeric constants (e.g., "0", 0).
    2. Columns in the DataFrame (always converting them to float).
    3. Nested definitions down to the leaf level where a column exists in df or is a constant.
    """

    def __init__(self, yaml_definitions: Dict[str, Any], debug: bool = False):
        self.yaml_definitions = yaml_definitions
        self.debug = debug
        self.intermediate_results: Dict[str, Dict[Any, Any]] = {}
        self.error_messages: Dict[Any, str] = {}

    def calculate(self, df: pd.DataFrame, target_variable: str) -> pd.DataFrame:
        """
        Compute the target variable for each row in df.
        Returns a DataFrame with:
          - The column target_variable (calculated values or pd.NA).
          - If debug=True: additional columns for each intermediate variable.
          - An 'error_message' column indicating the first missing-variable error.
        """
        # Reset previous run data
        self.intermediate_results = {}
        self.error_messages = {}

        # Apply _evaluate to each row
        result_series = df.apply(lambda row: self._evaluate(target_variable, row), axis=1)
        result_df = pd.DataFrame(result_series, columns=[target_variable])

        # Add debug columns if enabled
        if self.debug:
            for var, values in self.intermediate_results.items():
                result_df[var] = pd.Series(values)

        # Add the error_message column
        result_df["error_message"] = pd.Series(self.error_messages)
        return result_df

    def _evaluate(self, variable: Any, row: pd.Series) -> Optional[float]:
        """
        Recursively evaluate 'variable' for a single row.
        - If 'variable' is an int or float: treat as constant.
        - If 'variable' is a string matching a DataFrame column: parse to float.
        - Otherwise: look up in yaml_definitions and process recursively.
        """

        # 1) Numeric constant (int or float)
        if isinstance(variable, (int, float)):
            return float(variable)
        # If string representing a number, try to cast
        if isinstance(variable, str):
            try:
                return float(variable)
            except:
                pass

        # 2) DataFrame column: retrieve and convert to float
        if isinstance(variable, str) and variable in row:
            raw = row.get(variable)
            try:
                val = float(raw)
            except:
                # Non-convertible (e.g., "?") treated as missing
                return self._record_error(row.name, f"{variable} missing")
            return val

        # 3) Look up YAML definition
        definition = self.yaml_definitions.get(variable)
        if not definition:
            # Cannot proceed without a definition
            return self._record_error(row.name, f"Definition for '{variable}' not found")

        # 4) Alias case: "variable: <other_var>" in YAML
        if "variable" in definition:
            return self._evaluate(definition["variable"], row)

        # 5) Otherwise, expect 'expression' and 'components'
        expression = definition.get("expression")
        components = definition.get("components", [])

        evaluated: List[float] = []
        for comp in components:
            if isinstance(comp, dict) and "variable" in comp:
                # Direct variable reference
                sub_var = comp["variable"]
                value = self._evaluate(sub_var, row)
                label = sub_var
            elif isinstance(comp, dict):
                # Nested (anonymous) expression
                value = self._evaluate_anonymous(comp, row)
                label = str(comp)
            else:
                # Should be a constant: cast to float
                try:
                    value = float(comp)
                except:
                    return self._record_error(row.name, f"Unknown component '{comp}'")
                label = str(comp)

            # If any component is missing, stop with error
            if pd.isna(value):
                return self._record_error(row.name, f"{label} missing")

            evaluated.append(value)

        # 6) Apply the operator
        result = self._apply_operator(expression, evaluated)

        # Store intermediate result for debug
        if self.debug:
            self._store_intermediate(variable, row.name, result)

        return result

    def _evaluate_anonymous(self, expr: Dict[str, Any], row: pd.Series) -> Optional[float]:
        """
        Evaluate an anonymous (nested) expression with 'expression' and 'components'.
        Recurses until only pure variable references or constants remain.
        """
        expression = expr.get("expression")
        components = expr.get("components", [])

        evaluated: List[float] = []
        for comp in components:
            if isinstance(comp, dict) and "variable" in comp:
                sub_var = comp["variable"]
                value = self._evaluate(sub_var, row)
                label = sub_var
            else:
                # Deeper nested expression
                value = self._evaluate_anonymous(comp, row)
                label = str(comp)

            if pd.isna(value):
                return self._record_error(row.name, f"{label} missing")
            evaluated.append(value)

        return self._apply_operator(expression, evaluated)

    def _apply_operator(self, op: str, values: List[float]) -> Optional[float]:
        """
        Perform the operation 'op' on the list of floats in 'values'.
        Supported operators:
          - 'sum'      : sum of all values
          - 'minus'    : values[0] minus sum(values[1:])
          - 'multiply' : product of all values
          - 'divide'   : values[0] divided by each subsequent value
        Returns pd.NA on error (e.g., division by zero).
        """
        try:
            if op == "sum":
                return sum(values)
            elif op == "minus":
                return values[0] - sum(values[1:])
            elif op == "multiply":
                prod = 1.0
                for v in values:
                    prod *= v
                return prod
            elif op == "divide":
                quot = values[0]
                for v in values[1:]:
                    if v == 0:
                        return 0.0  # Division by zero returns zero
                    quot /= v
                return quot
            elif op == "max":
                return max(values)
            elif op == "min":
                return min(values)
        except:
            return pd.NA

    def _store_intermediate(self, var: str, index: Any, value: Any):
        """
        Store an intermediate calculation result for debugging (per row index).
        """
        if var not in self.intermediate_results:
            self.intermediate_results[var] = {}
        self.intermediate_results[var][index] = value

    def _record_error(self, index: Any, message: str) -> Optional[float]:
        """
        Record the first missing-variable or constant error for a row index.
        Always returns pd.NA to halt calculation.
        """
        if index not in self.error_messages:
            self.error_messages[index] = message
        return pd.NA


# # ---------------------------------------------------------------
# # Voorbeeldgebruik van de YamlCalculator:
# # ---------------------------------------------------------------
# import pandas as pd
# import yaml

# # 1) Laad de bron‐data voor de berekening
# df = pd.read_csv('km_source_data_converted.csv', index_col=0)

# # 2) Laad YAML in
# etlocal_key = "input_households_final_demand_steam_hot_water_demand"
# yaml_name = f"{etlocal_key}_dependency.yaml"
# with open(yaml_name, 'r') as file:
#     yaml_defs = yaml.safe_load(file)
# print(yaml_defs)

# # 3) Initialiseer en bereken
# calc = YamlCalculator(yaml_defs, debug=True)
# result_df = calc.calculate(df, etlocal_key)

# # 4) Toon enkele resultaten
# result_df