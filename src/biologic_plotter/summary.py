import pandas as pd


def get_cycle_summary(clean_df):
    if "cycle" not in clean_df.columns:
        raise ValueError("No cycle column found.")

    df = clean_df.copy()
    df = df.dropna(subset=["cycle"])
    df["cycle"] = df["cycle"].astype(int)

    summary_rows = []

    for cycle_number, group in df.groupby("cycle"):
        row = {"cycle": cycle_number}

        if "q_charge" in group.columns:
            row["charge_capacity"] = group["q_charge"].max()

        if "q_discharge" in group.columns:
            row["discharge_capacity"] = group["q_discharge"].max()

        if "efficiency" in group.columns:
            row["ce"] = group["efficiency"].dropna().iloc[-1] if not group["efficiency"].dropna().empty else None
        elif "calculated_ce" in group.columns:
            row["ce"] = group["calculated_ce"].dropna().iloc[-1] if not group["calculated_ce"].dropna().empty else None

        summary_rows.append(row)

    summary_df = pd.DataFrame(summary_rows)

    if "discharge_capacity" in summary_df.columns:
        first_value = summary_df["discharge_capacity"].dropna()
        if not first_value.empty and first_value.iloc[0] != 0:
            reference = first_value.iloc[0]
            summary_df["capacity_retention"] = summary_df["discharge_capacity"] / reference * 100

    return summary_df