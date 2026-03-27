from pathlib import Path
import pandas as pd

from biologic_plotter.file_io import select_files, load_file
from biologic_plotter.detection import detect_columns, make_clean_dataframe
from biologic_plotter.summary import get_cycle_summary
from biologic_plotter.plotting import ask_yes_no, choose_column, plot_data


def save_excel_report(clean_df, summary_df, output_path):
    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
        clean_df.to_excel(writer, sheet_name="cleaned_data", index=False)

        if summary_df is not None:
            summary_df.to_excel(writer, sheet_name="cycle_summary", index=False)


def main():
    print("BioLogic Data Tool")

    file_paths = select_files()

    if not file_paths:
        print("No files selected.")
        return

    export_cleaned = ask_yes_no("Export cleaned data?", "y")
    make_summary = ask_yes_no("Create cycle summary?", "y")
    make_plot = ask_yes_no("Create plot?", "y")

    cleaned_data_list = []
    labels = []

    for path in file_paths:
        print(f"\nProcessing file: {path.name}")

        try:
            df = load_file(path)
        except Exception as e:
            print(f"Could not load file: {e}")
            continue

        detected = detect_columns(df)

        print("Detected parameters:")
        for key, value in detected.items():
            print(f"{key}: {value}")

        clean_df = make_clean_dataframe(df, detected)
        cleaned_data_list.append(clean_df)
        labels.append(path.stem)

        summary_df = None
        if make_summary:
            try:
                summary_df = get_cycle_summary(clean_df)
                print("Summary created.")
            except Exception as e:
                print(f"Could not create summary: {e}")

        if export_cleaned:
            output_file = path.with_name(path.stem + "_report.xlsx")
            try:
                save_excel_report(clean_df, summary_df, output_file)
                print(f"Saved: {output_file.name}")
            except Exception as e:
                print(f"Could not save Excel report: {e}")

    if make_plot and cleaned_data_list:
        all_columns = set()

        for df in cleaned_data_list:
            for col in df.columns:
                all_columns.add(col)

        all_columns = sorted(list(all_columns))

        x_col = choose_column(all_columns, "Choose x-axis column")
        y_col = choose_column(all_columns, "Choose y-axis column")

        output_name = input("Enter output image name [default: plot.png]: ").strip()
        if output_name == "":
            output_name = "plot.png"

        output_path = file_paths[0].parent / output_name
        plot_data(cleaned_data_list, labels, x_col, y_col, output_path)

        print(f"Plot saved as: {output_path.name}")


if __name__ == "__main__":
    main()