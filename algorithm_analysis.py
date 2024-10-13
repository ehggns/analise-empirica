# analysis.py

import os
import pandas as pd
import numpy as np
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler

# Ensure compatibility with the latest versions
sns.set_theme(style="whitegrid")
plt.rcParams.update({"figure.max_open_warning": 0})

# Create the "analysis" folder if it doesn't exist
os.makedirs("analysis", exist_ok=True)

# Get list of metrics files in the "metrics" folder
metrics_folder = "metrics"
metrics_files = [f for f in os.listdir(metrics_folder) if f.endswith("_metrics.csv")]

# List of metrics and their corresponding columns in the stats_df
metrics_info = {
    "Execution Time": {"column": "Execution Time (sec)", "suffix": "execution_time"},
    "Comparisons": {"column": "Comparisons", "suffix": "comparisons"},
    "Exchanges": {"column": "Exchanges", "suffix": "exchanges"},
}

# Statistics to compute
statistics = ["Mean", "Median", "Std", "Var"]

# Process each metrics file
for metrics_file in metrics_files:
    # Get algorithm name from filename
    algorithm_name = metrics_file.replace("_metrics.csv", "")  # e.g., 'selection_sort'
    algorithm_analysis_folder = os.path.join("analysis", f"{algorithm_name}_analysis")
    os.makedirs(algorithm_analysis_folder, exist_ok=True)

    # Read the metrics CSV file
    metrics_path = os.path.join(metrics_folder, metrics_file)
    metrics_df = pd.read_csv(metrics_path)

    # Perform statistical analysis
    grouped = metrics_df.groupby(["Size", "Data Type"])

    # Initialize lists to store statistical results
    stats_list = []

    # Iterate over each group
    for name, group in grouped:
        size, data_type = name
        stats_entry = {"Size": size, "Data Type": data_type}
        for metric_name, metric_info in metrics_info.items():
            metric_values = group[metric_info["column"]]
            # Compute statistics
            stats_entry[f"{metric_name} Mean"] = metric_values.mean()
            stats_entry[f"{metric_name} Median"] = metric_values.median()
            stats_entry[f"{metric_name} Std"] = metric_values.std()
            stats_entry[f"{metric_name} Var"] = metric_values.var()
        stats_list.append(stats_entry)

    # Create a DataFrame from the statistics
    stats_df = pd.DataFrame(stats_list)

    # Save the statistical results to a CSV file in the algorithm's analysis folder
    stats_df.to_csv(
        os.path.join(
            algorithm_analysis_folder, f"{algorithm_name}_statistics_summary.csv"
        ),
        index=False,
    )

    # Now, for each metric, create plots for Mean, Median, Std, and Var vs Size
    for metric_name, metric_info in metrics_info.items():
        for stat_name in statistics:
            y_column = f"{metric_name} {stat_name}"
            # Plot with Plotly
            fig = px.line(
                stats_df,
                x="Size",
                y=y_column,
                color="Data Type",
                title=f"{metric_name} {stat_name} vs Size by Data Type ({algorithm_name})",
                labels={"Size": "Input Size", y_column: f"{metric_name} {stat_name}"},
            )
            # Create a filename, including the algorithm name
            filename = (
                f"{metric_info['suffix']}_{stat_name.lower()}_{algorithm_name}.html"
            )
            fig.write_html(os.path.join(algorithm_analysis_folder, filename))

            # Additional plotting with Seaborn and Matplotlib
            plt.figure(figsize=(10, 6))
            sns.lineplot(
                data=stats_df, x="Size", y=y_column, hue="Data Type", marker="o"
            )
            plt.title(
                f"{metric_name} {stat_name} vs Size by Data Type ({algorithm_name})"
            )
            plt.xlabel("Input Size")
            plt.ylabel(f"{metric_name} {stat_name}")
            plt.legend(title="Data Type")
            plt.tight_layout()
            image_filename = (
                f"{metric_info['suffix']}_{stat_name.lower()}_{algorithm_name}.png"
            )
            plt.savefig(os.path.join(algorithm_analysis_folder, image_filename))
            plt.close()

        # Scaling and plotting using scikit-learn's MinMaxScaler
        scaler = MinMaxScaler()
        scaled_stats_df = stats_df.copy()
        scaled_stats_df[["Size"]] = scaler.fit_transform(scaled_stats_df[["Size"]])

        # Plot scaled data
        for stat_name in statistics:
            y_column = f"{metric_name} {stat_name}"
            plt.figure(figsize=(10, 6))
            sns.lineplot(
                data=scaled_stats_df, x="Size", y=y_column, hue="Data Type", marker="o"
            )
            plt.title(
                f"Scaled {metric_name} {stat_name} vs Scaled Size ({algorithm_name})"
            )
            plt.xlabel("Scaled Input Size")
            plt.ylabel(f"Scaled {metric_name} {stat_name}")
            plt.legend(title="Data Type")
            plt.tight_layout()
            scaled_image_filename = f"scaled_{metric_info['suffix']}_{stat_name.lower()}_{algorithm_name}.png"
            plt.savefig(os.path.join(algorithm_analysis_folder, scaled_image_filename))
            plt.close()

    print(
        f"Analysis for {algorithm_name} completed. Results are saved in '{algorithm_analysis_folder}'."
    )

# Print a completion message
print("All analyses completed. Results and plots are saved in the 'analysis' folder.")
