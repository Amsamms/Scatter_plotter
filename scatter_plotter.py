import py_compile
import numpy as np
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px
import plotly.figure_factory as ff
from sklearn.preprocessing import MinMaxScaler
import openpyxl
import streamlit as st
import scipy.stats as stats
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Simple Scatter Plotter",
    page_icon=":chart_with_downwards_trend:",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
        .app-header {
            background: linear-gradient(135deg, #5a4bdb 0%, #9b7bf0 100%);
            color: white;
            padding: 2rem 2.5rem;
            border-radius: 18px;
            box-shadow: 0 12px 35px rgba(90, 75, 219, 0.35);
            margin-bottom: 1.5rem;
        }
        .app-header h1 {
            font-size: 2.4rem;
            margin-bottom: 0.4rem;
        }
        .app-header p {
            font-size: 1.1rem;
            margin: 0;
        }
        .info-card {
            background: #ffffff;
            border-radius: 14px;
            padding: 1rem 1.2rem;
            box-shadow: 0 6px 18px rgba(99, 102, 241, 0.18);
            border: 1px solid rgba(99, 102, 241, 0.12);
            height: 100%;
        }
        .info-card h3 {
            margin-top: 0;
            color: #5a4bdb;
            font-size: 1.05rem;
            margin-bottom: 0.4rem;
        }
        .info-card p {
            margin: 0;
            color: #4b4b63;
            font-size: 0.93rem;
        }
        .sidebar-section {
            padding: 1rem 0 0.5rem;
            border-top: 1px solid rgba(90, 75, 219, 0.2);
        }
        .sidebar-section:first-child {
            border-top: none;
        }
        .data-preview > div:first-child {
            border-radius: 14px !important;
            border: 1px solid rgba(90, 75, 219, 0.15);
            box-shadow: 0 10px 24px rgba(90, 75, 219, 0.12);
        }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="app-header">
        <h1>Simple Scatter Plotter</h1>
        <p>Upload your spreadsheet and explore rich, interactive scatter visualisations with confidence.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(
        """
        <div class="info-card">
            <h3>1. Upload & preview</h3>
            <p>Drop in an Excel or CSV file and instantly review the cleaned dataset.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
with col2:
    st.markdown(
        """
        <div class="info-card">
            <h3>2. Configure the view</h3>
            <p>Select axes, scaling options, or correlation tools directly from the sidebar.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
with col3:
    st.markdown(
        """
        <div class="info-card">
            <h3>3. Interact & compare</h3>
            <p>Hover, zoom, and switch between dynamic or static charts to analyse trends.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

how_to_text = """
1. Start by uploading an Excel or CSV file via the sidebar. Make sure column headers are in the first row.
2. If the dataset includes a DATE column, enable the dedicated checkbox and choose the column.
3. Choose one of the visual modes from the sidebar: single chart, re-scaled chart, multiple charts, correlations, or column vs. top correlations.
4. Optional: remove outliers using the Standard Deviation slider for a cleaner comparison.
5. Charts appear in this main area and respond to your selections instantly.
"""

tab1, tab2, tab3 = st.tabs([
    "Main app",
    "How to run the app",
    "Video description of the app",
])

with tab2:
    st.header("How to use")
    st.markdown(how_to_text)
    st.info("All non-numeric cells are automatically converted to empty values during processing.")

with tab3:
    st.header("Walkthrough video")
    st.markdown("Refer to the demo below for a quick overview of the workflow.")
    st.video("https://youtu.be/W8CR1zD15l0")

sidebar = st.sidebar.container()
sidebar.header("Step 1 · Upload data")
data = sidebar.file_uploader(
    "Upload your Excel/CSV file",
    type=["csv", "xls", "xlsx"],
    key="1",
    help="Supported formats: CSV, XLS, or XLSX. Only one sheet per file is processed.",
)

sidebar.caption("Tip: Larger files may take a few seconds to render.")

df_raw = None
df = None

if data is None:
    sidebar.info("Please upload a valid Excel or CSV dataset to unlock the chart controls.")
else:
    try:
        df_raw = pd.read_csv(data, encoding_errors="ignore")
    except Exception:
        pass
    if df_raw is None:
        try:
            df_raw = pd.read_csv(data)
        except Exception:
            pass
    if df_raw is None:
        try:
            df_raw = pd.read_excel(data)
        except Exception:
            pass
    if df_raw is None:
        try:
            df_raw = pd.read_excel(data, engine="openpyxl")
        except Exception:
            pass

    if df_raw is not None:
        df = df_raw.copy()
    else:
        sidebar.error("The uploaded file could not be read. Please check the format and try again.")

advanced_sidebar = st.sidebar.container()

k = False
gl = False
choice = None

if df is not None:
    advanced_sidebar.header("Step 2 · Data formatting")
    k = advanced_sidebar.checkbox(
        "My data contains a DATE column",
        key="date_status",
        help="Enable this option if one of the columns should remain as a date/time axis.",
    )
    if k:
        date = advanced_sidebar.selectbox(
            "Select the DATE column",
            df.columns,
            help="Choose the column that contains date or time values.",
        )
        df[date] = pd.to_datetime(df[date])

    gl = advanced_sidebar.checkbox(
        "Optimise for very large datasets",
        key="gl",
        help="Switches to WebGL-based rendering for smoother plotting with thousands of points.",
    )

    advanced_sidebar.header("Step 3 · Visual mode")
    choice = advanced_sidebar.radio(
        "Choose what to explore",
        [
            "One chart",
            "One Chart with re-scaling",
            "Many charts",
            "Correlations",
            "Column vs Top Correlations",
        ],
        help="Select the type of analysis you would like to generate on the main canvas.",
    )

    advanced_sidebar.caption(
        "Need guidance? Switch to the 'How to run the app' tab above for a walkthrough."
    )

with tab1:
    st.header("Visual workspace")
    st.caption("Use the sidebar controls to tailor the plots below. Hover over elements for more detail.")

    if df is None:
        st.info("Upload an Excel or CSV file using the sidebar to begin exploring your data.")
    else:
        with st.expander("📊 Preview uploaded data", expanded=True):
            st.dataframe(df_raw, use_container_width=True)

        st.markdown("---")
        st.subheader("Optional data cleaning")
        st.caption(
            "Removing outliers can make long-term trends easier to spot. Adjust the slider to control the sensitivity."
        )

        if st.checkbox(
            "Remove outliers",
            help="Applies a Z-score filter to remove rows outside the selected number of standard deviations.",
        ):
            st.markdown("#### Standard Deviation")
            try:
                df_new = df.copy()
                for column in df_new.columns:
                    df_new[column] = pd.to_numeric(df_new[column], errors="coerce")
                outlier_limit = st.slider(
                    "Number of standard deviations",
                    1.0,
                    10.0,
                    4.0,
                    0.2,
                    help="Rows with values beyond this threshold are filtered out.",
                )
                st.write(f"Initial rows: {df.shape[0]}")

                def df_without_outliers(data, a=4.0):
                    df_copy = data.copy()
                    z_scores = stats.zscore(df_copy[df_copy.describe().columns], nan_policy="omit")
                    z_scores.fillna(0, inplace=True)
                    abs_z_scores = np.abs(z_scores)
                    filtered_entries = (abs_z_scores < a).all(axis=1)
                    df_without_outliers = df_copy[filtered_entries]
                    return df_without_outliers

                df_new = df_without_outliers(df_new, a=outlier_limit)
                df = df.loc[df_new.index]
                st.success(f"Rows after filtering: {df.shape[0]}")
            except Exception as e:
                st.error(f"An error occurred while filtering: {type(e).__name__} — {e}")
                st.warning("Dataset could not be filtered. Original data will be used.")

        st.markdown("---")

        style = "lines+markers" if st.session_state.get("date_status") else "markers"

        visual_descriptions = {
            "One chart": "Overlay multiple series on a single plot, with optional secondary axis handling.",
            "One Chart with re-scaling": "Compare series on different scales by re-scaling them to a shared range.",
            "Many charts": "Plot each selected series separately against a shared X axis.",
            "Correlations": "Inspect correlation matrices and heatmaps for the selected columns.",
            "Column vs Top Correlations": "Highlight the strongest correlations with focused comparison charts.",
        }

        if choice:
            st.subheader(f"Mode selected: {choice}")
            st.caption(visual_descriptions.get(choice, ""))

        if choice == "One chart":
            X = st.sidebar.selectbox(
                "X axis",
                df.columns,
                help="Choose the column that will be used on the horizontal axis.",
            )
            Y_1 = st.sidebar.multiselect(
                "Primary Y axis",
                df.columns,
                help="Pick one or more series to display on the left Y axis.",
            )
            Y_2 = st.sidebar.multiselect(
                "Secondary Y axis",
                df.columns,
                help="Optional series to display on the right Y axis.",
            )
            if df[X].dtype == "datetime64[ns]" and k:
                pass
            else:
                df[X] = pd.to_numeric(df[X], errors="coerce")
            for column in Y_1:
                if df[column].dtype == "datetime64[ns]" and k:
                    pass
                else:
                    df[column] = pd.to_numeric(df[column], errors="coerce")
            for column in Y_2:
                if df[column].dtype == "datetime64[ns]" and k:
                    pass
                else:
                    df[column] = pd.to_numeric(df[column], errors="coerce")
            fig = make_subplots(specs=[[{"secondary_y": True}]])
            try:
                for column in Y_1:
                    if gl:
                        fig.add_trace(
                            go.Scattergl(x=df[X], y=df[column], mode=style, name=column)
                        )
                    else:
                        fig.add_trace(
                            go.Scatter(x=df[X], y=df[column], mode=style, name=column)
                        )
            except Exception:
                pass
            try:
                for column in Y_2:
                    if gl:
                        fig.add_trace(
                            go.Scattergl(
                                x=df[X],
                                y=df[column],
                                mode=style,
                                name=column,
                            ),
                            secondary_y=True,
                        )
                    else:
                        fig.add_trace(
                            go.Scatter(
                                x=df[X],
                                y=df[column],
                                mode=style,
                                name=column,
                            ),
                            secondary_y=True,
                        )
            except Exception:
                pass
            st.plotly_chart(fig, use_container_width=True)

        if choice == "One Chart with re-scaling":
            auto_scale = st.sidebar.radio(
                "Column selection",
                [
                    "All columns included",
                    "All columns included except some",
                    "Manually choose included columns",
                ],
                index=2,
                key="auto_scale",
                help="Decide which columns should be included before applying scaling.",
            )
            min_val = st.sidebar.number_input(
                "Minimum value for re-scaling",
                help="Lower bound applied after Min-Max scaling.",
            )
            max_val = st.sidebar.number_input(
                "Maximum value for re-scaling",
                help="Upper bound applied after Min-Max scaling.",
            )
            if auto_scale == "Manually choose included columns":
                X = st.sidebar.selectbox(
                    "X axis",
                    df.columns,
                    help="Choose the reference column for the horizontal axis.",
                )
                if df[X].dtype == "datetime64[ns]" and k:
                    pass
                else:
                    df[X] = pd.to_numeric(df[X], errors="coerce")
                columnss = st.sidebar.multiselect(
                    "Columns to plot",
                    df.columns,
                    help="Pick the series you want to rescale and visualise together.",
                )
                fig = go.Figure()
                for column in columnss:
                    try:
                        if df[column].dtype == "datetime64[ns]" and k:
                            pass
                        else:
                            df[column] = pd.to_numeric(df[column], errors="coerce")
                    except Exception:
                        st.write(f"The column {column} cannot be plotted. Please review its data.")
                        continue
                try:
                    scaler = MinMaxScaler((min_val, max_val))
                    scaler.fit(df[columnss])
                    df_transformed = pd.DataFrame(
                        scaler.transform(df[columnss]), columns=columnss
                    )
                    for column in df_transformed.columns:
                        if gl:
                            fig.add_trace(
                                go.Scattergl(
                                    x=df[X],
                                    y=df_transformed[column],
                                    mode=style,
                                    name=column,
                                )
                            )
                        else:
                            fig.add_trace(
                                go.Scatter(
                                    x=df[X],
                                    y=df_transformed[column],
                                    mode=style,
                                    name=column,
                                )
                            )
                    st.plotly_chart(fig, use_container_width=True)
                except Exception:
                    pass
            elif auto_scale == "All columns included":
                X = st.sidebar.selectbox(
                    "X axis",
                    df.columns,
                    help="Choose the reference column for the horizontal axis.",
                )
                if df[X].dtype == "datetime64[ns]" and k:
                    pass
                else:
                    df[X] = pd.to_numeric(df[X], errors="coerce")
                columnss = df.columns.difference([X])
                fig = go.Figure()
                for column in columnss:
                    try:
                        if df[column].dtype == "datetime64[ns]" and k:
                            pass
                        else:
                            df[column] = pd.to_numeric(df[column], errors="coerce")
                    except Exception:
                        st.write(f"The column {column} cannot be plotted. Please review its data.")
                        continue
                try:
                    scaler = MinMaxScaler((min_val, max_val))
                    scaler.fit(df[columnss])
                    df_transformed = pd.DataFrame(
                        scaler.transform(df[columnss]), columns=columnss
                    )
                    for column in df_transformed.columns:
                        if gl:
                            fig.add_trace(
                                go.Scattergl(
                                    x=df[X],
                                    y=df_transformed[column],
                                    mode=style,
                                    name=column,
                                )
                            )
                        else:
                            fig.add_trace(
                                go.Scatter(
                                    x=df[X],
                                    y=df_transformed[column],
                                    mode=style,
                                    name=column,
                                )
                            )
                    st.plotly_chart(fig, use_container_width=True)
                except Exception:
                    pass
            elif auto_scale == "All columns included except some":
                X = st.sidebar.selectbox(
                    "X axis",
                    df.columns,
                    help="Choose the reference column for the horizontal axis.",
                )
                if df[X].dtype == "datetime64[ns]" and k:
                    pass
                else:
                    df[X] = pd.to_numeric(df[X], errors="coerce")
                excepted_columns = st.sidebar.multiselect(
                    "Columns to exclude",
                    df.columns,
                    help="Any column selected here will be excluded from the visualisation.",
                )
                columnss = df.drop(excepted_columns, axis=1).columns
                fig = go.Figure()
                for column in columnss:
                    try:
                        if df[column].dtype == "datetime64[ns]" and k:
                            pass
                        else:
                            df[column] = pd.to_numeric(df[column], errors="coerce")
                    except Exception:
                        st.write(f"The column {column} cannot be plotted. Please review its data.")
                        continue
                try:
                    scaler = MinMaxScaler((min_val, max_val))
                    scaler.fit(df[columnss])
                    df_transformed = pd.DataFrame(
                        scaler.transform(df[columnss]), columns=columnss
                    )
                    for column in df_transformed.columns:
                        if gl:
                            fig.add_trace(
                                go.Scattergl(
                                    x=df[X],
                                    y=df_transformed[column],
                                    mode=style,
                                    name=column,
                                )
                            )
                        else:
                            fig.add_trace(
                                go.Scatter(
                                    x=df[X],
                                    y=df_transformed[column],
                                    mode=style,
                                    name=column,
                                )
                            )
                    st.plotly_chart(fig, use_container_width=True)
                except Exception:
                    pass

        if choice == "Many charts":
            many_choices = st.sidebar.radio(
                "Column selection",
                [
                    "All columns included",
                    "All columns included except some",
                    "Manually choose included columns",
                ],
                index=2,
                key="many_choices",
                help="Decide how many series to draw side-by-side.",
            )
            if many_choices == "Manually choose included columns":
                X = st.sidebar.selectbox(
                    "Fixed X axis column",
                    df.columns,
                    help="Select the column used as the horizontal axis for every chart.",
                )
                if df[X].dtype == "datetime64[ns]" and k:
                    pass
                else:
                    df[X] = pd.to_numeric(df[X], errors="coerce")
                columns = st.sidebar.multiselect(
                    "Columns to plot",
                    df.columns,
                    help="Each selected column will be plotted against the chosen X axis.",
                )
                for column in columns:
                    try:
                        if df[column].dtype == "datetime64[ns]" and k:
                            pass
                        else:
                            df[column] = pd.to_numeric(df[column], errors="coerce")
                        fig = go.Figure()
                        if gl:
                            fig.add_trace(go.Scattergl(x=df[X], y=df[column], mode=style))
                        else:
                            fig.add_trace(go.Scatter(x=df[X], y=df[column], mode=style))
                        fig.update_layout(xaxis_title=X, yaxis_title=column)
                        st.plotly_chart(fig, use_container_width=True)
                    except Exception:
                        st.write(
                            f"The column {column} cannot be plotted. Please review its data."
                        )
                        continue
            elif many_choices == "All columns included":
                X = st.sidebar.selectbox(
                    "Fixed X axis column",
                    df.columns,
                    help="Select the column used as the horizontal axis for every chart.",
                )
                if df[X].dtype == "datetime64[ns]" and k:
                    pass
                else:
                    df[X] = pd.to_numeric(df[X], errors="coerce")
                for column in df.columns:
                    try:
                        if df[column].dtype == "datetime64[ns]" and k:
                            pass
                        else:
                            df[column] = pd.to_numeric(df[column], errors="coerce")
                        fig = go.Figure()
                        if gl:
                            fig.add_trace(go.Scattergl(x=df[X], y=df[column], mode=style))
                        else:
                            fig.add_trace(go.Scatter(x=df[X], y=df[column], mode=style))
                        fig.update_layout(xaxis_title=X, yaxis_title=column)
                        st.plotly_chart(fig, use_container_width=True)
                    except Exception:
                        st.write(
                            f"The column {column} cannot be plotted. Please review its data."
                        )
                        continue
            elif many_choices == "All columns included except some":
                X = st.sidebar.selectbox(
                    "Fixed X axis column",
                    df.columns,
                    help="Select the column used as the horizontal axis for every chart.",
                )
                if df[X].dtype == "datetime64[ns]" and k:
                    pass
                else:
                    df[X] = pd.to_numeric(df[X], errors="coerce")
                excepted_columns = st.sidebar.multiselect(
                    "Columns to exclude",
                    df.columns,
                    help="Columns selected here will be skipped when generating charts.",
                )
                columnss = df.drop(excepted_columns, axis=1).columns
                fig = go.Figure()
                for column in columnss:
                    try:
                        if df[column].dtype == "datetime64[ns]" and k:
                            pass
                        else:
                            df[column] = pd.to_numeric(df[column], errors="coerce")
                        fig = go.Figure()
                        if gl:
                            fig.add_trace(go.Scattergl(x=df[X], y=df[column], mode=style))
                        else:
                            fig.add_trace(go.Scatter(x=df[X], y=df[column], mode=style))
                        fig.update_layout(xaxis_title=X, yaxis_title=column)
                        st.plotly_chart(fig, use_container_width=True)
                    except Exception:
                        st.write(
                            f"The column {column} cannot be plotted. Please review its data."
                        )
                        continue

        if choice == "Correlations":
            correlations = st.sidebar.radio(
                "Column selection",
                [
                    "All columns included",
                    "All columns included except some",
                    "Manually choose included columns",
                ],
                index=2,
                key="correlations",
                help="Choose which columns should be included when building the correlation matrix.",
            )
            if correlations == "Manually choose included columns":
                columnss = st.sidebar.multiselect(
                    "Columns to correlate",
                    df.columns,
                    help="Pick columns that should appear in the correlation analysis.",
                )
                corr = df[columnss].corr()
                st.success("Correlation matrix ready")
                st.dataframe(corr, use_container_width=True)
                fig = go.Figure()
                fig.add_trace(go.Heatmap(x=corr.columns, y=corr.index, z=np.array(corr)))
                st.plotly_chart(fig, use_container_width=True)
            elif correlations == "All columns included":
                corr = df.corr()
                st.success("Correlation matrix ready")
                st.dataframe(corr, use_container_width=True)
                fig = go.Figure()
                fig.add_trace(go.Heatmap(x=corr.columns, y=corr.index, z=np.array(corr)))
                st.plotly_chart(fig, use_container_width=True)
            elif correlations == "All columns included except some":
                excepted_columns = st.sidebar.multiselect(
                    "Columns to exclude",
                    df.columns,
                    help="Select any columns that should be omitted from the correlation analysis.",
                )
                columnss = df.drop(excepted_columns, axis=1).columns
                corr = df[columnss].corr()
                st.success("Correlation matrix ready")
                st.dataframe(corr, use_container_width=True)
                fig = go.Figure()
                fig.add_trace(go.Heatmap(x=corr.columns, y=corr.index, z=np.array(corr)))
                st.plotly_chart(fig, use_container_width=True)

        if choice == "Column vs Top Correlations":
            st.subheader("Column vs Top Correlations Analysis")

            df_numeric = df.copy()
            for column in df_numeric.columns:
                if df_numeric[column].dtype == "datetime64[ns]" and k:
                    pass
                else:
                    df_numeric[column] = pd.to_numeric(df_numeric[column], errors="coerce")

            corr = df_numeric.corr()

            if corr.empty:
                st.error("No numeric columns found for correlation analysis.")
            else:
                X_corr = st.sidebar.selectbox(
                    "X axis for correlation plots",
                    df.columns,
                    help="This column defines the shared horizontal axis in the comparison charts.",
                )
                selected_column = st.sidebar.selectbox(
                    "Main column for correlation analysis",
                    corr.columns,
                    help="The strongest correlations with this column will be displayed below.",
                )
                num_correlations = st.sidebar.slider(
                    "Number of top correlations",
                    1,
                    min(50, len(corr.columns) - 1),
                    3,
                    help="Controls how many of the strongest correlations are shown.",
                )
                plot_type = st.sidebar.radio(
                    "Plot style",
                    ["Dynamic (Plotly)", "Static (Matplotlib)"],
                    key="plot_type_corr",
                    help="Choose between interactive Plotly charts or static Matplotlib figures.",
                )

                if df[X_corr].dtype == "datetime64[ns]" and k:
                    x_data = df[X_corr]
                else:
                    x_data = pd.to_numeric(df[X_corr], errors="coerce")

                if selected_column in corr.columns:
                    correlations = corr[selected_column].drop(labels=[selected_column]).dropna()
                    top_correlations = correlations.reindex(
                        correlations.abs().sort_values(ascending=False).index
                    ).head(num_correlations)

                    st.write(
                        f"**Top {num_correlations} correlations for '{selected_column}':**"
                    )
                    st.dataframe(
                        top_correlations.to_frame(name="Correlation"),
                        use_container_width=True,
                    )

                    for corr_column, corr_value in top_correlations.items():
                        if plot_type == "Dynamic (Plotly)":
                            fig = make_subplots(specs=[[{"secondary_y": True}]])

                            if gl:
                                fig.add_trace(
                                    go.Scattergl(
                                        x=x_data,
                                        y=df[selected_column],
                                        mode=style,
                                        name=f"{selected_column}",
                                        line=dict(color="blue"),
                                    ),
                                    secondary_y=False,
                                )

                                fig.add_trace(
                                    go.Scattergl(
                                        x=x_data,
                                        y=df[corr_column],
                                        mode=style,
                                        name=f"{corr_column}",
                                        line=dict(color="red", dash="dot"),
                                    ),
                                    secondary_y=True,
                                )
                            else:
                                fig.add_trace(
                                    go.Scatter(
                                        x=x_data,
                                        y=df[selected_column],
                                        mode=style,
                                        name=f"{selected_column}",
                                        line=dict(color="blue"),
                                    ),
                                    secondary_y=False,
                                )

                                fig.add_trace(
                                    go.Scatter(
                                        x=x_data,
                                        y=df[corr_column],
                                        mode=style,
                                        name=f"{corr_column}",
                                        line=dict(color="red", dash="dot"),
                                    ),
                                    secondary_y=True,
                                )

                            fig.update_layout(
                                title=f"{selected_column} vs {corr_column}<br>Correlation: {corr_value:.3f}",
                                legend_title="Columns",
                            )
                            fig.update_yaxes(
                                title_text=f"<b>{selected_column}</b>", secondary_y=False
                            )
                            fig.update_yaxes(
                                title_text=f"<b>{corr_column}</b>", secondary_y=True
                            )
                            fig.update_xaxes(title_text=X_corr)

                            st.plotly_chart(fig, use_container_width=True)

                        else:
                            fig, ax1 = plt.subplots(figsize=(10, 6))

                            color1 = "tab:blue"
                            ax1.set_xlabel(X_corr)
                            ax1.set_ylabel(selected_column, color=color1)

                            if style == "lines+markers":
                                ax1.plot(
                                    x_data,
                                    df[selected_column],
                                    color=color1,
                                    marker="o",
                                    linestyle="-",
                                    markersize=3,
                                    label=selected_column,
                                )
                            else:
                                ax1.scatter(
                                    x_data,
                                    df[selected_column],
                                    color=color1,
                                    s=20,
                                    label=selected_column,
                                )

                            ax1.tick_params(axis="y", labelcolor=color1)

                            ax2 = ax1.twinx()
                            color2 = "tab:red"
                            ax2.set_ylabel(corr_column, color=color2)

                            if style == "lines+markers":
                                ax2.plot(
                                    x_data,
                                    df[corr_column],
                                    color=color2,
                                    marker="s",
                                    linestyle="--",
                                    markersize=3,
                                    label=corr_column,
                                )
                            else:
                                ax2.scatter(
                                    x_data,
                                    df[corr_column],
                                    color=color2,
                                    s=20,
                                    marker="s",
                                    label=corr_column,
                                )

                            ax2.tick_params(axis="y", labelcolor=color2)

                            plt.title(
                                f"{selected_column} vs {corr_column}\nCorrelation: {corr_value:.3f}",
                                fontsize=12,
                            )

                            lines1, labels1 = ax1.get_legend_handles_labels()
                            lines2, labels2 = ax2.get_legend_handles_labels()
                            ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper right")

                            plt.tight_layout()
                            st.pyplot(fig)
                            plt.close()
                else:
                    st.error(
                        f"Column '{selected_column}' not found in the correlation matrix."
                    )

        st.markdown("---")
        st.caption("Finished exploring? Upload a new file to start over or jump to another visual mode.")
