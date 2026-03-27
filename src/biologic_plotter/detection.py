import pandas as pd


def clean_text(text):
    text = str(text).strip().lower()
    text = text.replace("_", " ")
    return text


def detect_columns(df):
    detected = {}

    for col in df.columns:
        name = clean_text(col)

        if "time" in name and "time" not in detected:
            detected["time"] = col
        elif "ewe-ece" in name and "ewe_minus_ece" not in detected:
            detected["ewe_minus_ece"] = col
        elif "ece" in name and "ece" not in detected:
            detected["ece"] = col
        elif "ewe" in name and "ewe" not in detected:
            detected["ewe"] = col
        elif "i/" in name or ("<i>" in name) or ("ma" in name and "current" in name) or name == "i":
            if "current" not in detected:
                detected["current"] = col
        elif "q charge" in name and "q_charge" not in detected:
            detected["q_charge"] = col
        elif "q discharge" in name and "q_discharge" not in detected:
            detected["q_discharge"] = col
        elif "cycle" in name and "cycle" not in detected:
            detected["cycle"] = col
        elif "efficiency" in name and "efficiency" not in detected:
            detected["efficiency"] = col
        elif "freq" in name and "freq" not in detected:
            detected["freq"] = col
        elif "re(z)" in name and "rez" not in detected:
            detected["rez"] = col
        elif "im(z)" in name and "imz" not in detected:
            detected["imz"] = col

    return detected


def to_numeric(series):
    return pd.to_numeric(
        series.astype(str).str.replace(",", ".", regex=False),
        errors="coerce",
    )


def make_clean_dataframe(df, detected):
    clean_df = pd.DataFrame()

    for key, original_col in detected.items():
        clean_df[key] = df[original_col]

    for col in clean_df.columns:
        clean_df[col] = to_numeric(clean_df[col])

    if "time" in clean_df.columns:
        clean_df["time_min"] = clean_df["time"] / 60
        clean_df["time_h"] = clean_df["time"] / 3600

    if "q_charge" in clean_df.columns and "q_discharge" in clean_df.columns:
        clean_df["calculated_ce"] = clean_df["q_discharge"] / clean_df["q_charge"] * 100

    return clean_df