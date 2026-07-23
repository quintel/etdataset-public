"""
Dataset-specific data fixes.

Handles special-case transformations required for certain datasets:
- NL mobile machinery reallocation (off-road → transport)
- Residual calculations for missing child categories
- Industry sector category fixes
"""

from __future__ import annotations
import pandas as pd
import re

from ..config import (
    COL_OUT_CODE,
    COL_OUT_CATEGORY,
    COL_OUT_CO2,
    COL_OUT_OTHER,
    COL_OUT_TOTAL,
    MOBILE_MACHINERY_CRT_CODES,
    MOBILE_MACHINERY_REALLOCATION_CODE,
    MOBILE_MACHINERY_CHILD_CODE,
)


def reallocate_nl_mobile_machinery(df: pd.DataFrame) -> pd.DataFrame:
    """
    Reallocate NL off-road mobile machinery emissions to 1.A.3.b and its
    child 1.A.3.b.iii, so that the sum of 1.A.3.b's children matches the
    1.A.3.b total.

    For NL datasets, off-road machinery emissions scattered across multiple
    sectors (manufacturing, commercial, residential, agriculture) are
    reallocated to road transport (1.A.3.b) for ETM modeling purposes.

    Process:
    1. Zero out source off-road codes
    2. Subtract from their parent categories
    3. Add total to 1.A.3.b and its child 1.A.3.b.iii (create if absent)
    4. Update 1.A.3 parent total

    Args:
        df: Emissions DataFrame with CRT codes

    Returns:
        Modified DataFrame (copy, not mutated)
    """
    df = df.copy()
    offroad_mask = df[COL_OUT_CODE].isin(MOBILE_MACHINERY_CRT_CODES)
    offroad_rows = df[offroad_mask]

    if offroad_rows.empty:
        return df

    amounts = (
        offroad_rows[[COL_OUT_CODE, COL_OUT_CO2, COL_OUT_OTHER]]
        .set_index(COL_OUT_CODE)[[COL_OUT_CO2, COL_OUT_OTHER]]
        .fillna(0)
    )
    co2_sum = amounts[COL_OUT_CO2].sum()
    other_sum = amounts[COL_OUT_OTHER].sum()

    def adjust(code: str, co2_delta: float, other_delta: float) -> None:
        """Add deltas to a row's emissions."""
        mask = df[COL_OUT_CODE].astype(str) == code
        if not mask.any():
            return
        idx = df.index[mask][0]
        for col, delta in [(COL_OUT_CO2, co2_delta), (COL_OUT_OTHER, other_delta)]:
            if pd.notna(df.at[idx, col]):
                df.at[idx, col] += delta
        _recalculate_total(df, idx)

    for code, ancestors in MOBILE_MACHINERY_CRT_CODES.items():
        mask = df[COL_OUT_CODE].astype(str) == code
        if not mask.any():
            continue
        df.loc[df.index[mask][0], [COL_OUT_CO2, COL_OUT_OTHER, COL_OUT_TOTAL]] = 0.0
        if code in amounts.index:
            co2, other = amounts.at[code, COL_OUT_CO2], amounts.at[code, COL_OUT_OTHER]
            for ancestor in ancestors:
                adjust(ancestor, -co2, -other)

    def add_or_create(code: str, category: str, co2_delta: float, other_delta: float) -> None:
        """Add deltas to code's row, creating it with category label if absent."""
        nonlocal df
        if (df[COL_OUT_CODE].astype(str) == code).any():
            adjust(code, co2_delta, other_delta)
        else:
            df = _create_reallocation_row(df, code, category, co2_delta, other_delta)

    # Add to target 1.A.3.b and its child 1.A.3.b.iii (so children sum to the
    # parent); create rows if absent
    add_or_create(MOBILE_MACHINERY_REALLOCATION_CODE, "Mobile machinery", co2_sum, other_sum)
    add_or_create(MOBILE_MACHINERY_CHILD_CODE, "Mobile machinery", co2_sum, other_sum)

    adjust("1.A.3", co2_sum, other_sum)

    return df


def set_child_residual(
    df: pd.DataFrame,
    parent_code: str,
    child_code: str,
) -> tuple[pd.DataFrame, float | None]:
    """
    Set child to parent − sum(other direct children).

    Used to calculate residual values for missing child categories
    (e.g., Singapore, Sweden datasets).

    Args:
        df: Emissions DataFrame
        parent_code: Parent CRT code
        child_code: Child CRT code to calculate residual for

    Returns:
        Tuple of (modified DataFrame, residual value or None)
    """
    parent_row = df[df[COL_OUT_CODE].astype(str) == parent_code]
    if parent_row.empty or pd.isna(parent_row.iloc[0][COL_OUT_CO2]):
        return df, None

    parent_val = float(parent_row.iloc[0][COL_OUT_CO2])
    siblings = _get_direct_children(df, parent_code)
    others = siblings[siblings[COL_OUT_CODE].astype(str) != child_code]
    other_sum = others[COL_OUT_CO2].fillna(0).sum()
    residual = parent_val - other_sum

    df = ensure_row(df, parent_code, child_code, residual)
    return df, residual


def ensure_row(
    df: pd.DataFrame,
    parent_code: str,
    child_code: str,
    value: float,
    category: str = "",
) -> pd.DataFrame:
    """
    Set a child row's CO2 value; insert if doesn't exist.

    Args:
        df: Emissions DataFrame
        parent_code: Parent CRT code (used for cloning metadata)
        child_code: Child CRT code
        value: CO2 value to set
        category: Category label (optional)

    Returns:
        Modified DataFrame
    """
    df = df.copy()
    mask = df[COL_OUT_CODE].astype(str) == child_code

    if mask.any():
        df.loc[mask, COL_OUT_CO2] = value
    else:
        new_row = df[df[COL_OUT_CODE].astype(str) == parent_code].iloc[0].copy()
        new_row[COL_OUT_CODE] = child_code
        new_row[COL_OUT_CO2] = value
        new_row[COL_OUT_CATEGORY] = category
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

    return df


# ── Private helpers ───────────────────────────────────────────────────────────


def _recalculate_total(df: pd.DataFrame, idx: int) -> None:
    """Recalculate total_ghg from co2 + other_ghg."""
    co2_val = df.at[idx, COL_OUT_CO2]
    other_val = df.at[idx, COL_OUT_OTHER]
    df.at[idx, COL_OUT_TOTAL] = (
        (co2_val if pd.notna(co2_val) else 0) + (other_val if pd.notna(other_val) else 0)
        if pd.notna(co2_val) or pd.notna(other_val)
        else float("nan")
    )


def _get_direct_children(df: pd.DataFrame, parent: str) -> pd.DataFrame:
    """Return rows that are direct children of parent."""
    pat = re.compile(r"^" + re.escape(parent) + r"\.[^.]+$")
    return df[df[COL_OUT_CODE].astype(str).str.match(pat)]


def _create_reallocation_row(
    df: pd.DataFrame,
    code: str,
    category: str,
    co2_sum: float,
    other_sum: float,
) -> pd.DataFrame:
    """Create new row for mobile machinery reallocation."""
    return pd.concat(
        [
            df,
            pd.DataFrame(
                [
                    {
                        COL_OUT_CODE: code,
                        COL_OUT_CATEGORY: category,
                        COL_OUT_CO2: co2_sum,
                        COL_OUT_OTHER: other_sum,
                        COL_OUT_TOTAL: co2_sum + other_sum,
                    }
                ]
            ),
        ],
        ignore_index=True,
    )
