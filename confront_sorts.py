# confront_sorts.py

import os
import pandas as pd
import plotly.express as px

# Create the "confront_sorts" folder if it doesn't exist
os.makedirs("confront_sorts", exist_ok=True)

# List of sorting algorithms
algorithms = [
    "selection_sort",
    "insertion_sort",
    "heap_sort",
    "merge_sort",
    "quick_sort",
]

# List of metrics and their corresponding columns
metrics_info = {
    "Execution Time Mean": {
        "column": "Execution Time Mean",
        "ylabel": "Execution Time (sec)",
        "filename": "execution_time_mean_comparison.html",
    },
    "Comparisons Mean": {
        "column": "Comparisons Mean",
        "ylabel": "Comparisons",
        "filename": "comparisons_mean_comparison.html",
    },
    "Exchanges Mean": {
        "column": "Exchanges Mean",
        "ylabel": "Exchanges",
        "filename": "exchanges_mean_comparison.html",
    },
}

# Initialize a dictionary to hold data for each algorithm
algorithm_data = {}

# Read the statistics_summary.csv files for each algorithm
for algorithm in algorithms:
    stats_file = os.path.join(
        "analysis", f"{algorithm}_analysis", f"{algorithm}_statistics_summary.csv"
    )
    if os.path.exists(stats_file):
        df = pd.read_csv(stats_file)
        df["Algorithm"] = algorithm.replace("_", " ").title()
        algorithm_data[algorithm] = df
    else:
        print(f"Statistics file for {algorithm} not found at {stats_file}")

# Combine data from all algorithms
combined_data = pd.DataFrame()
for df in algorithm_data.values():
    combined_data = pd.concat([combined_data, df], ignore_index=True)

# List of data types
data_types = combined_data["Data Type"].unique()

# Generate plots for each metric and data type
for metric_name, metric_info in metrics_info.items():
    for data_type in data_types:
        # Filter data for the current data type
        data = combined_data[combined_data["Data Type"] == data_type]

        # Create the plot
        fig = px.line(
            data,
            x="Size",
            y=metric_info["column"],
            color="Algorithm",
            title=f"{metric_name} vs Size ({data_type.title()} Data)",
            labels={
                "Size": "Input Size",
                metric_info["column"]: metric_info["ylabel"],
                "Algorithm": "Sorting Algorithm",
            },
        )

        # Update layout for better readability
        fig.update_layout(
            legend_title="Algorithm",
            xaxis_title="Input Size",
            yaxis_title=metric_info["ylabel"],
        )

        # Generate a filename
        filename = f"{metric_info['filename'].split('.')[0]}_{data_type}.html"
        fig.write_html(os.path.join("confront_sorts", filename))

print("Comparison plots have been generated and saved in the 'confront_sorts' folder.")
