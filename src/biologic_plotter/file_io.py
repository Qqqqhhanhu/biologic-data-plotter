from pathlib import Path
import tkinter as tk
from tkinter import filedialog
import pandas as pd


def select_files():
    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)

    file_paths = filedialog.askopenfilenames(
        title="Select BioLogic files",
        filetypes=[
            ("BioLogic files", "*.csv *.mpt"),
            ("CSV files", "*.csv"),
            ("MPT files", "*.mpt"),
            ("All files", "*.*"),
        ],
    )

    root.destroy()
    return [Path(path) for path in file_paths]


def load_csv_file(path):
    return pd.read_csv(
        path,
        sep=";",
        decimal=",",
        encoding="utf-8",
        engine="python",
    )


def load_mpt_file(path):
    header_lines = 0

    with open(path, "r", encoding="latin1", errors="ignore") as f:
        for line in f:
            if "Nb header lines" in line:
                parts = line.strip().split(":")
                if len(parts) == 2:
                    header_lines = int(parts[1].strip())
                break

    return pd.read_csv(
        path,
        sep="\t",
        skiprows=header_lines - 1,
        encoding="latin1",
        engine="python",
    )


def load_file(path):
    suffix = path.suffix.lower()

    if suffix == ".csv":
        return load_csv_file(path)
    elif suffix == ".mpt":
        return load_mpt_file(path)
    else:
        raise ValueError(f"Unsupported file type: {path.suffix}")