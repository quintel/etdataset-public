'''
This script combines seperate heating curve CSVs into one CSV and creates
boxplots for comparing 2023 with 2019 heating curves.
'''

import os
import pandas as pd
import matplotlib.pyplot as plt
import math

def combine_csv_columns(main_dir, curve_folder_name):
    """
    Combines separate heat curve CSV files for nl2023 and nl2019 to
    a single DataFrame.

    Args:
        main_dir (str): Main directory path.
        curve_folder_name (str): Folder name containing curve CSV files.

    Returns:
        pd.DataFrame: Combined DataFrame.
    """
    combined_df = pd.DataFrame()

    # Path to the target folder
    curve_folders = os.path.join(main_dir, curve_folder_name)

    # Loop through all files in curve folder
    for root, dirs, files in os.walk(curve_folders):

        for file in sorted(files):
            if file.endswith('.csv'):
                file_path = os.path.join(root, file)
                col_name = os.path.splitext(file)[0]

                # Check if file is in 2019 subfolder and add to column name
                if os.path.relpath(root, curve_folders) != '.':
                    col_name += '_2019'

                # Read single-column CSV file
                df = pd.read_csv(file_path, header=None, names=[col_name])

                # Combine into the main DataFrame
                combined_df = pd.concat([combined_df, df], axis=1)

    combined_df = combined_df.sort_index(axis=1)

    return combined_df


def save_2023_vs_2019_boxplots(main_dir, df, groupings, output_prefix="boxplots"):
    """
    Groups boxplots in categories and saves each group to its own image file.

    Args:
        main_dir (str): Main directory path.
        df (pd.DataFrame): The input DataFrame.
        groupings (list of list): Grouping of curve categories.
        output_prefix (str): Prefix for output image filenames.
    """
    output_folder = os.path.join(main_dir, 'boxplots')
    columns = df.columns.tolist()
    paired_columns = []

    # Identify column pairs
    i = 0
    while i < len(columns) - 1:
        col1 = columns[i]
        col2 = columns[i + 1]

        if col2 == col1 + "_2019":
            paired_columns.append((col1, col2))
            i += 2
        else:
            i += 1  # skip unmatched
            print(f"Skipping unmatched column: {col1}")

    # Group pairs by keyword groupings
    grouped_pairs = {tuple(group): [] for group in groupings}

    for col1, col2 in paired_columns:
        for group in groupings:
            if any(keyword in col1 for keyword in group):
                grouped_pairs[tuple(group)].append((col1, col2))
                break

    # Plot each group in its own figure
    for group, pairs in grouped_pairs.items():
        if not pairs:
            continue

        group_name = "_".join(group)
        n = len(pairs)
        ncols = 2
        nrows = math.ceil(n / ncols)

        fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=(6 * ncols, 5 * nrows))
        axes = axes.flatten()

        for idx, (col1, col2) in enumerate(pairs):
            ax = axes[idx]
            ax.boxplot([df[col1].dropna(), df[col2].dropna()], labels=["2023", "2019"])
            ax.set_title(f'{col1}')
            ax.set_ylabel('Values')
            ax.grid(True)

        # Remove unused axes
        for j in range(len(pairs), len(axes)):
            fig.delaxes(axes[j])

        plt.tight_layout()
        filename = os.path.join(output_folder, f"{output_prefix}_{group_name}.png")
        plt.savefig(filename, dpi=300)
        plt.close()
        print(f"Saved box plots for group '{group_name}' to: {filename}")


def save_sorted_boxplot_by_category(df, year="2023"):
    """
    Creates a households insulation boxplot for specified year.
    The columns are sorted by (housing_type, category) order.
    """

    housing_types = ['apartments', 'semi_detached', 'detached', 'terraced']
    categories = ['low', 'medium', 'high']
    exclude_cols = {"agriculture_heating", "buildings_heating"}

    # Filter columns by year
    if year == "2023":
        valid_cols = [
            col for col in df.columns
            if "2019" not in col and col not in exclude_cols
        ]
    elif year == "2019":
        valid_cols = [
            col for col in df.columns
            if "2019" in col and col not in exclude_cols
        ]
    else:
        raise ValueError("year must be '2023' or '2019'")

    # Sort columns by housing_type and category
    sorted_cols = []
    for h_type in housing_types:
        for cat in categories:
            for col in valid_cols:
                if h_type in col and cat in col:
                    sorted_cols.append(col)

    if not sorted_cols:
        print(f"No matching columns found for year {year}.")
        return

    # Prepare data
    data = [df[col].dropna() for col in sorted_cols]

    # Plot
    plt.figure(figsize=(max(10, len(sorted_cols) * 1.5), 6))
    labels = [col.replace("insulation_", "") for col in sorted_cols]
    plt.boxplot(data, labels=labels)
    plt.xticks(rotation=45, ha='right')
    plt.title(f"Households insulation {year}")
    plt.ylabel("Values")
    plt.grid(True)
    plt.tight_layout()

    # Save
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_folder = os.path.join(script_dir, "boxplots")
    os.makedirs(output_folder, exist_ok=True)
    output_file_name = f"households_insulation_boxplot_{year}.png"

    output_path = os.path.join(output_folder, output_file_name)
    # plt.show()
    plt.savefig(output_path, dpi=300)
    plt.close()
    print(f"Saved sorted boxplot to: {output_path}")

if __name__ == "__main__":
    main_dir = os.path.dirname(os.path.abspath(__file__))
    curve_folder_name = 'heating_curves'

    # Combine CSVs to one DataFrame
    combined_df = combine_csv_columns(main_dir,curve_folder_name)
    combined_df.to_csv(os.path.join(main_dir, 'combined_heating_curves.csv'), index=False)

    # Generate and save boxplots 2023 vs 2019 per category
    groupings = [['agriculture','buildings'], ['apartments'], ['semi_detached'], ['detached'], ['terraced']]
    save_2023_vs_2019_boxplots(main_dir,combined_df,groupings)

    # Generate households insulation boxplots per start year
    save_sorted_boxplot_by_category(combined_df, year="2023")
    save_sorted_boxplot_by_category(combined_df, year="2019")
