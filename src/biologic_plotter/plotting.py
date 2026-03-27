import matplotlib.pyplot as plt
import pandas as pd


def ask_yes_no(question, default="y"):
    answer = input(f"{question} [y/n, default {default}]: ").strip().lower()

    if answer == "":
        answer = default

    return answer == "y"


def choose_column(columns, message):
    print(f"\n{message}")
    for i, col in enumerate(columns, 1):
        print(f"{i}. {col}")

    while True:
        choice = input("Enter a number: ").strip()

        if choice.isdigit():
            choice = int(choice)
            if 1 <= choice <= len(columns):
                return columns[choice - 1]

        print("Invalid choice. Try again.")


def plot_data(dataframes, labels, x_col, y_col, output_path):
    plt.figure(figsize=(8, 5))

    for df, label in zip(dataframes, labels):
        if x_col in df.columns and y_col in df.columns:
            plot_df = df[[x_col, y_col]].dropna()
            plt.plot(plot_df[x_col], plot_df[y_col], label=label)

    plt.xlabel(x_col)
    plt.ylabel(y_col)
    plt.title(f"{y_col} vs {x_col}")
    plt.grid(True)

    if len(dataframes) > 1:
        plt.legend()

    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.show()