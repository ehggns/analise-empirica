# app.py

import os
import pandas as pd
import numpy as np
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import dash_bootstrap_components as dbc

# Initialize the Dash app with external stylesheets
external_stylesheets = [dbc.themes.BOOTSTRAP]
app = Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "Sorting Algorithms Performance Analysis"

# Suppress callback exceptions
app.config.suppress_callback_exceptions = True

# Get list of sorting algorithms
algorithms = [
    "selection_sort",
    "insertion_sort",
    "heap_sort",
    "merge_sort",
    "quick_sort",
]
algorithm_options = [
    {"label": alg.replace("_", " ").title(), "value": alg} for alg in algorithms
]

# Metrics information
metrics_info = {
    "Execution Time Mean": "Execution Time Mean",
    "Comparisons Mean": "Comparisons Mean",
    "Exchanges Mean": "Exchanges Mean",
}
metric_options = [{"label": key, "value": value} for key, value in metrics_info.items()]

# Data types
data_types = ["random", "sorted", "reverse_sorted"]
data_type_options = [
    {"label": dt.replace("_", " ").title(), "value": dt} for dt in data_types
]

# Theoretical complexities
complexities = {
    "O(1)": lambda n: np.ones_like(n),
    "O(log n)": lambda n: np.log2(n),
    "O(n)": lambda n: n,
    "O(n log n)": lambda n: n * np.log2(n),
    "O(n^2)": lambda n: n**2,
    "O(n^3)": lambda n: n**3,
}
complexity_options = [{"label": k, "value": k} for k in complexities.keys()]


# Load data for all algorithms
def load_data():
    all_data = pd.DataFrame()
    for algorithm in algorithms:
        stats_file = os.path.join(
            "analysis", f"{algorithm}_analysis", f"{algorithm}_statistics_summary.csv"
        )
        if os.path.exists(stats_file):
            df = pd.read_csv(stats_file)
            df["Algorithm"] = algorithm.replace("_", " ").title()
            all_data = pd.concat([all_data, df], ignore_index=True)
    return all_data


# Load the data
data = load_data()

# Ensure data is not empty to avoid errors
if data.empty:
    data = pd.DataFrame(
        {
            "Size": [1],
            "Data Type": ["random"],
            "Algorithm": ["None"],
            "Execution Time Mean": [1],
            "Comparisons Mean": [1],
            "Exchanges Mean": [1],
        }
    )

# Ensure 'Size' column has no zeros or negative values
data = data[data["Size"] > 0]

# Custom CSS styles
app.layout = html.Div(
    [
        dbc.NavbarSimple(
            brand="Sorting Algorithms Performance Analysis",
            brand_href="#",
            color="primary",
            dark=True,
        ),
        dbc.Container(
            [
                dbc.Tabs(
                    [
                        dbc.Tab(
                            label="Performance Comparison",
                            tab_id="tab-comparison",
                            tab_style={"margin-left": "auto"},
                        ),
                        dbc.Tab(label="Algorithm Details", tab_id="tab-details"),
                        dbc.Tab(label="Algorithm Tree Map", tab_id="tab-treemap"),
                        dbc.Tab(label="Pie Chart", tab_id="tab-pie-chart"),
                    ],
                    id="tabs",
                    active_tab="tab-comparison",
                ),
                html.Br(),
                html.Div(id="tab-content"),
            ],
            fluid=True,
        ),
    ],
    style={"padding": "0px"},
)


# Callback to render content based on the selected tab
@app.callback(Output("tab-content", "children"), Input("tabs", "active_tab"))
def render_tab_content(active_tab):
    if active_tab == "tab-comparison":
        return render_comparison_tab()
    elif active_tab == "tab-details":
        return render_details_tab()
    elif active_tab == "tab-treemap":
        return render_treemap_tab()
    elif active_tab == "tab-pie-chart":
        return render_pie_chart_tab()
    else:
        return html.Div("Tab content not found.")


def render_comparison_tab():
    size_min = max(data["Size"].min(), 1)
    size_max = data["Size"].max()
    size_marks = {
        int(size): str(int(size))
        for size in sorted(data["Size"].unique())
        if size >= size_min
    }

    return html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.Label("Select Metric:"),
                            dcc.Dropdown(
                                id="metric-dropdown",
                                options=metric_options,
                                value="Execution Time Mean",
                            ),
                        ],
                        md=3,
                    ),
                    dbc.Col(
                        [
                            html.Label("Select Data Type:"),
                            dcc.Dropdown(
                                id="data-type-dropdown",
                                options=data_type_options,
                                value="random",
                            ),
                        ],
                        md=3,
                    ),
                    dbc.Col(
                        [
                            html.Label("Select Algorithms:"),
                            dcc.Dropdown(
                                id="algorithm-dropdown",
                                options=algorithm_options,
                                value=[alg["value"] for alg in algorithm_options],
                                multi=True,
                            ),
                        ],
                        md=3,
                    ),
                    dbc.Col(
                        [
                            html.Label("Select Theoretical Complexities:"),
                            dcc.Dropdown(
                                id="complexity-dropdown",
                                options=complexity_options,
                                value=[],
                                multi=True,
                            ),
                        ],
                        md=3,
                    ),
                ]
            ),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.Label("Adjust Input Size Range:"),
                            dcc.RangeSlider(
                                id="size-range-slider",
                                min=size_min,
                                max=size_max,
                                step=1,
                                value=[size_min, size_max],
                                marks=size_marks,
                                tooltip={"placement": "bottom", "always_visible": True},
                            ),
                        ],
                        md=12,
                    ),
                ],
                style={"margin-top": "20px"},
            ),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.Div(
                                [
                                    dbc.Checklist(
                                        options=[
                                            {
                                                "label": "Logarithmic X-axis",
                                                "value": "logx",
                                            },
                                            {
                                                "label": "Logarithmic Y-axis",
                                                "value": "logy",
                                            },
                                        ],
                                        value=[],
                                        id="log-scale-checklist",
                                        inline=True,
                                        switch=True,
                                    ),
                                ]
                            )
                        ],
                        md=12,
                    ),
                ],
                style={"margin-top": "20px"},
            ),
            dcc.Graph(id="performance-graph"),
            html.Div(id="description"),
        ]
    )


def render_details_tab():
    return html.Div(
        [
            html.H4("Algorithm Details"),
            html.P(
                "Here you can provide detailed descriptions of each algorithm, their complexities, and other relevant information."
            ),
            # Add more content as needed
        ]
    )


def render_treemap_tab():
    return html.Div(
        [
            html.H4("Algorithm Tree Map"),
            html.P(
                "Visualize the algorithms' performance metrics using a stacked Tree Map."
            ),
            html.Div(
                [
                    dbc.Row(
                        [
                            dbc.Col(
                                [
                                    html.Label("Select Metric:"),
                                    dcc.Dropdown(
                                        id="treemap-metric-dropdown",
                                        options=metric_options,
                                        value="Execution Time Mean",
                                    ),
                                ],
                                md=4,
                            ),
                            dbc.Col(
                                [
                                    html.Label("Number of Size Bins:"),
                                    dcc.Slider(
                                        id="treemap-bin-slider",
                                        min=2,
                                        max=20,
                                        step=1,
                                        value=10,
                                        marks={i: str(i) for i in range(2, 21)},
                                    ),
                                ],
                                md=4,
                            ),
                        ],
                        style={"margin-bottom": "20px"},
                    ),
                    dcc.Graph(id="treemap-graph", style={"height": "800px"}),
                ]
            ),
        ]
    )


def render_pie_chart_tab():
    return html.Div(
        [
            html.H4("Pie Chart"),
            html.P(
                "Visualize the distribution of performance metrics using a pie chart."
            ),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.Label("Select Metric:"),
                            dcc.Dropdown(
                                id="pie-metric-dropdown",
                                options=metric_options,
                                value="Execution Time Mean",
                            ),
                        ],
                        md=4,
                    ),
                    dbc.Col(
                        [
                            html.Label("Group By:"),
                            dcc.Dropdown(
                                id="pie-groupby-dropdown",
                                options=[
                                    {"label": "Algorithm", "value": "Algorithm"},
                                    {"label": "Data Type", "value": "Data Type"},
                                    {"label": "Size", "value": "Size"},
                                ],
                                value="Algorithm",
                            ),
                        ],
                        md=4,
                    ),
                ],
                style={"margin-bottom": "20px"},
            ),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.Label("Select Data Type:"),
                            dcc.Dropdown(
                                id="pie-data-type-dropdown",
                                options=data_type_options,
                                value="random",
                            ),
                        ],
                        md=6,
                    ),
                    dbc.Col(
                        [
                            html.Label("Select Algorithms:"),
                            dcc.Dropdown(
                                id="pie-algorithm-dropdown",
                                options=algorithm_options,
                                value=[alg["value"] for alg in algorithm_options],
                                multi=True,
                            ),
                        ],
                        md=6,
                    ),
                ],
                style={"margin-bottom": "20px"},
            ),
            dcc.Graph(id="pie-chart", style={"height": "600px"}),
        ]
    )


# Define callback to update the main graph
@app.callback(
    Output("performance-graph", "figure"),
    Output("description", "children"),
    Input("metric-dropdown", "value"),
    Input("data-type-dropdown", "value"),
    Input("algorithm-dropdown", "value"),
    Input("size-range-slider", "value"),
    Input("log-scale-checklist", "value"),
    Input("complexity-dropdown", "value"),
)
def update_graph(
    selected_metric,
    selected_data_type,
    selected_algorithms,
    size_range,
    log_scale_values,
    selected_complexities,
):
    # Handle case where no algorithms are selected
    if not selected_algorithms:
        description = "No algorithms selected."
        return {}, description

    # Filter data
    filtered_data = data[
        (data["Data Type"] == selected_data_type)
        & (
            data["Algorithm"]
            .str.replace(" ", "_")
            .str.lower()
            .isin(selected_algorithms)
        )
        & (data["Size"] >= size_range[0])
        & (data["Size"] <= size_range[1])
    ]

    if filtered_data.empty:
        fig = {}
        description = "No data available for the selected filters."
        return fig, description

    # Create figure
    fig = px.line(
        filtered_data,
        x="Size",
        y=selected_metric,
        color="Algorithm",
        markers=True,
        title=f"{selected_metric} vs Input Size ({selected_data_type.title()} Data)",
    )
    fig.update_layout(
        xaxis_title="Input Size", yaxis_title=selected_metric, legend_title="Algorithm"
    )

    # Add theoretical complexity curves
    if selected_complexities:
        # Ensure that size_range[0] is at least 1 to avoid log(0)
        n_min = max(size_range[0], 1)
        n_max = size_range[1]
        n_values = np.linspace(n_min, n_max, num=100)

        for complexity in selected_complexities:
            complexity_func = complexities[complexity]
            y_values = complexity_func(n_values)

            # Handle potential infinite or NaN values in y_values
            y_values = np.nan_to_num(y_values, nan=0.0, posinf=0.0, neginf=0.0)

            # Scale y_values to match the magnitude of the empirical data for better visualization
            # Find a scaling factor
            max_empirical_y = filtered_data[selected_metric].max()
            max_theoretical_y = y_values.max()
            scaling_factor = (
                max_empirical_y / max_theoretical_y if max_theoretical_y != 0 else 1
            )
            y_values_scaled = y_values * scaling_factor

            # Add the theoretical curve to the plot
            fig.add_trace(
                px.line(
                    x=n_values,
                    y=y_values_scaled,
                    labels={"x": "Size", "y": selected_metric},
                ).data[0]
            )
            # Update the trace name to show the complexity
            fig.data[-1].name = complexity
            fig.data[-1].line.update(dash="dash")
            fig.data[
                -1
            ].hovertemplate = f"Theoretical {complexity}<br>Size=%{{x}}<br>{selected_metric}=%{{y}}<extra></extra>"

    if "logx" in log_scale_values:
        fig.update_xaxes(type="log")
    if "logy" in log_scale_values:
        fig.update_yaxes(type="log")
    description = f"Displaying {selected_metric} for {selected_data_type.replace('_', ' ').title()} data across selected algorithms."
    return fig, description


# Callback to update treemap graph
@app.callback(
    Output("treemap-graph", "figure"),
    Input("treemap-metric-dropdown", "value"),
    Input("treemap-bin-slider", "value"),
)
def update_treemap(selected_metric, num_bins):
    # Prepare data for the treemap
    treemap_data = data.copy()

    # Bin sizes into ranges for better visualization
    treemap_data["Size Range"] = pd.cut(treemap_data["Size"], bins=num_bins).astype(str)

    # Create the treemap with more hierarchical levels
    fig = px.treemap(
        treemap_data,
        path=["Data Type", "Algorithm", "Size Range"],
        values=selected_metric,
        color="Algorithm",
        title=f"{selected_metric} by Data Type, Algorithm, and Size Range",
        color_discrete_sequence=px.colors.qualitative.Plotly,
    )

    # Increase figure size for better resolution
    fig.update_layout(margin=dict(t=50, l=25, r=25, b=25))

    return fig


# Callback to update pie chart
@app.callback(
    Output("pie-chart", "figure"),
    Input("pie-metric-dropdown", "value"),
    Input("pie-groupby-dropdown", "value"),
    Input("pie-data-type-dropdown", "value"),
    Input("pie-algorithm-dropdown", "value"),
)
def update_pie_chart(
    selected_metric, group_by, selected_data_type, selected_algorithms
):
    # Handle case where no algorithms are selected
    if not selected_algorithms:
        fig = {}
        return fig

    # Filter data
    filtered_data = data[
        (data["Data Type"] == selected_data_type)
        & (
            data["Algorithm"]
            .str.replace(" ", "_")
            .str.lower()
            .isin(selected_algorithms)
        )
    ]

    if filtered_data.empty:
        fig = {}
        return fig

    # Aggregate data
    pie_data = filtered_data.groupby(group_by)[selected_metric].sum().reset_index()

    # Create the pie chart
    fig = px.pie(
        pie_data,
        names=group_by,
        values=selected_metric,
        title=f"{selected_metric} Distribution by {group_by}",
        color=group_by,
        color_discrete_sequence=px.colors.qualitative.Plotly,
        hover_data=[selected_metric],
    )

    fig.update_traces(textposition="inside", textinfo="percent+label")

    return fig


# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
