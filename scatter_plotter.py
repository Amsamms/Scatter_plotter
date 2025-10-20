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


# Enhanced Page Configuration
st.set_page_config(
    page_title="📊 Advanced Scatter Plot Studio",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for stunning visuals
st.markdown("""
<style>
    /* Main app styling */
    .main > div {
        padding-top: 2rem;
    }

    /* Header styling */
    .header-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
    }

    .header-title {
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }

    .header-subtitle {
        font-size: 1.2rem;
        opacity: 0.9;
        font-weight: 300;
    }

    /* Card styling */
    .info-card {
        background: linear-gradient(145deg, #f0f4f8, #e2e8f0);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 5px solid #667eea;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }

    /* Status indicators */
    .status-indicator {
        display: inline-flex;
        align-items: center;
        padding: 0.5rem 1rem;
        border-radius: 25px;
        font-weight: 600;
        margin: 0.25rem;
    }

    .status-success {
        background-color: #d4edda;
        color: #155724;
        border: 1px solid #c3e6cb;
    }

    .status-warning {
        background-color: #fff3cd;
        color: #856404;
        border: 1px solid #ffeaa7;
    }

    .status-info {
        background-color: #d1ecf1;
        color: #0c5460;
        border: 1px solid #bee5eb;
    }

    /* Feature highlights */
    .feature-highlight {
        background: linear-gradient(45deg, #ff6b6b, #feca57);
        background-clip: text;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
        font-size: 1.1rem;
    }

    /* Step indicators */
    .step-container {
        display: flex;
        align-items: center;
        margin: 1rem 0;
        padding: 1rem;
        border-radius: 10px;
        background: white;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }

    .step-number {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        width: 40px;
        height: 40px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        margin-right: 1rem;
        flex-shrink: 0;
    }

    .step-content {
        flex: 1;
    }

    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #f8fafc 0%, #e2e8f0 100%);
    }

    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.5rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.3);
    }

    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: transparent;
    }

    .stTabs [data-baseweb="tab"] {
        background: linear-gradient(135deg, #e2e8f0, #cbd5e0);
        border-radius: 25px;
        color: #4a5568;
        font-weight: 600;
        border: none;
        padding: 0.75rem 1.5rem;
        transition: all 0.3s ease;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }

    /* Metric styling */
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        border-top: 4px solid #667eea;
        text-align: center;
        margin: 0.5rem 0;
    }

    /* Error/Warning styling */
    .stAlert {
        border-radius: 10px;
        border: none;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }

    /* Data frame styling */
    .dataframe {
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }

    /* Progress indicator */
    .progress-container {
        background: #f1f5f9;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
    }

    /* Custom selectbox and multiselect styling */
    .stSelectbox > div > div {
        border-radius: 10px;
        border: 2px solid #e2e8f0;
        transition: all 0.3s ease;
    }

    .stSelectbox > div > div:focus-within {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }

    .stMultiSelect > div > div {
        border-radius: 10px;
        border: 2px solid #e2e8f0;
    }

    .stMultiSelect > div > div:focus-within {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
</style>
""", unsafe_allow_html=True)

# Enhanced Header
st.markdown("""
<div class="header-container">
    <h1 class="header-title">📊 Advanced Scatter Plot Studio</h1>
    <p class="header-subtitle">Transform your data into stunning interactive visualizations with just a few clicks</p>
</div>
""", unsafe_allow_html=True)

# Enhanced Tabs with Icons
tab1, tab2, tab3 = st.tabs(["🎯 Main App", "📋 Step-by-Step Guide", "🎥 Video Tutorial"])

with tab1:
    st.markdown("""
    <div class="info-card">
        <h2>🎨 Visualization Workspace</h2>
        <p>Upload your data and create stunning interactive plots in seconds!</p>
    </div>
    """, unsafe_allow_html=True)

with tab2:
    st.markdown("""
    <div class="info-card">
        <h2>🚀 Quick Start Guide</h2>
        <p>Follow these simple steps to create amazing visualizations</p>
    </div>
    """, unsafe_allow_html=True)

    # Step-by-step guide with visual indicators
    steps = [
        {
            "number": "1",
            "title": "📁 Upload Your Data",
            "content": "Click the 'Upload your excel/csv file here' button in the sidebar. Make sure your file has column names in the first row and contains a single sheet.",
            "tip": "Supported formats: Excel (.xlsx, .xls) and CSV files"
        },
        {
            "number": "2",
            "title": "📅 Configure Date Settings",
            "content": "If your data contains date columns, check the 'DATE column' checkbox and select which column contains dates.",
            "tip": "This ensures proper time-series visualization"
        },
        {
            "number": "3",
            "title": "🎯 Choose Your Visualization Type",
            "content": "Select from 5 powerful chart types:",
            "options": [
                "📈 **One Chart**: Multiple series on single chart with dual Y-axes",
                "📊 **Re-scaling Chart**: Normalized data for easy comparison",
                "📋 **Multiple Charts**: Individual charts for each data series",
                "🔥 **Correlation Heatmap**: Discover data relationships",
                "⚡ **Top Correlations**: Find strongest correlations for any column"
            ]
        },
        {
            "number": "4",
            "title": "🔧 Fine-tune Your Analysis",
            "content": "Customize your visualization with advanced options:",
            "options": [
                "🎯 Remove outliers with adjustable thresholds",
                "⚡ Optimize for large datasets",
                "🎨 Choose columns and axes"
            ]
        },
        {
            "number": "5",
            "title": "✨ View Your Results",
            "content": "Your beautiful, interactive charts will appear in the main area. Hover, zoom, and explore your data!",
            "tip": "All visualizations are fully interactive with Plotly"
        }
    ]

    for step in steps:
        st.markdown(f"""
        <div class="step-container">
            <div class="step-number">{step['number']}</div>
            <div class="step-content">
                <h3 style="margin: 0 0 0.5rem 0; color: #2d3748;">{step['title']}</h3>
                <p style="margin: 0 0 0.5rem 0; color: #4a5568;">{step['content']}</p>
                {"".join([f"<p style='margin: 0.25rem 0; color: #718096; font-size: 0.9rem;'>• {option}</p>" for option in step.get('options', [])])}
                {f"<p style='margin-top: 0.5rem; padding: 0.5rem; background: #f7fafc; border-radius: 5px; color: #2b6cb0; font-size: 0.85rem;'><strong>💡 Tip:</strong> {step['tip']}</p>" if 'tip' in step else ""}
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class="info-card">
        <h3>⚠️ Important Notes</h3>
        <ul>
            <li>📊 Non-numeric cells will be automatically converted to empty cells</li>
            <li>📈 Date columns require proper formatting for time-series plots</li>
            <li>⚡ For large datasets (>10k points), enable the large data option for better performance</li>
            <li>🎯 Outlier removal uses statistical Z-score filtering</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with tab3:
    st.markdown("""
    <div class="info-card">
        <h2>🎥 Video Tutorial</h2>
        <p>Watch this comprehensive walkthrough to master all features</p>
    </div>
    """, unsafe_allow_html=True)
    st.video('https://youtu.be/W8CR1zD15l0')




# Enhanced Sidebar
st.sidebar.markdown("""
<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
           padding: 1.5rem; margin: -1rem -1rem 2rem -1rem;
           border-radius: 0 0 15px 15px; color: white; text-align: center;">
    <h2 style="margin: 0; font-size: 1.5rem; font-weight: 700;">🎛️ Control Panel</h2>
    <p style="margin: 0.5rem 0 0 0; opacity: 0.9;">Configure your visualization</p>
</div>
""", unsafe_allow_html=True)

# Enhanced file upload section
st.sidebar.markdown("### 📁 Data Upload")
data = st.sidebar.file_uploader(
    "Choose your file",
    type=['csv', 'xls', 'xlsx'],
    key='1',
    help="Upload Excel (.xlsx, .xls) or CSV files. Make sure column names are in the first row."
)

# File processing with enhanced status indicators
if data is not None:
    with st.spinner('🔄 Processing your file...'):
        try:
            df_raw = pd.read_csv(data, encoding_errors='ignore')
        except:
            try:
                df_raw = pd.read_csv(data)
            except:
                try:
                    df_raw = pd.read_excel(data)
                except:
                    try:
                        df_raw = pd.read_excel(data, engine='openpyxl')
                    except:
                        st.sidebar.error("❌ Error reading file. Please check the format.")

    if 'df_raw' in locals():
        st.sidebar.markdown("""
        <div class="status-indicator status-success">
            ✅ File loaded successfully!
        </div>
        """, unsafe_allow_html=True)

        # Display data summary
        st.sidebar.markdown("### 📊 Data Summary")
        st.sidebar.markdown(f"""
        <div class="metric-card">
            <h4 style="margin: 0; color: #667eea;">Dataset Info</h4>
            <p style="margin: 0.5rem 0 0 0;"><strong>Rows:</strong> {df_raw.shape[0]:,}</p>
            <p style="margin: 0.25rem 0 0 0;"><strong>Columns:</strong> {df_raw.shape[1]}</p>
        </div>
        """, unsafe_allow_html=True)
else:
    st.sidebar.markdown("""
    <div class="status-indicator status-warning">
        ⚠️ Please upload a file to get started
    </div>
    """, unsafe_allow_html=True)

    st.sidebar.markdown("""
    <div class="info-card">
        <h4>📋 Requirements</h4>
        <ul style="font-size: 0.9rem; margin: 0; padding-left: 1.2rem;">
            <li>Excel (.xlsx, .xls) or CSV files</li>
            <li>Single sheet only</li>
            <li>Column names in first row</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
# Enhanced data display
if 'df_raw' in locals():
    with tab1:
        st.markdown("### 📋 Your Data Preview")
        with st.container():
            # Show column info
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("📊 Total Rows", f"{df_raw.shape[0]:,}")
            with col2:
                st.metric("🏗️ Columns", df_raw.shape[1])
            with col3:
                st.metric("💾 Data Types", df_raw.dtypes.nunique())

            # Enhanced dataframe display
            st.markdown("#### 🔍 Data Sample")
            try:
                st.dataframe(df_raw, height=400)
            except:
                pass

try:
    df = df_raw.copy()
except:
    pass

# Enhanced configuration section
if data is not None:
    st.sidebar.markdown("---")
    st.sidebar.markdown("### ⚙️ Data Configuration")

    # Date column configuration with enhanced UI
    k = st.sidebar.checkbox(
        '📅 My data contains DATE columns',
        key='date_status',
        help="Enable this if your data has date/time columns for time-series plots"
    )

    if k:
        st.sidebar.markdown("**Select Date Column:**")
        date = st.sidebar.selectbox(
            'Choose the date column',
            df.columns,
            help="This column will be used for time-series visualization"
        )
        df[date] = pd.to_datetime(df[date])

        st.sidebar.markdown("""
        <div class="status-indicator status-info">
            📅 Date column configured
        </div>
        """, unsafe_allow_html=True)

    # Large dataset optimization
    gl = st.sidebar.checkbox(
        '⚡ Optimize for large datasets',
        key='gl',
        help="Enable this for datasets with >10,000 points for better performance"
    )

    if gl:
        st.sidebar.markdown("""
        <div class="status-indicator status-info">
            ⚡ Large data optimization enabled
        </div>
        """, unsafe_allow_html=True)

    st.sidebar.markdown("---")
    
    # Enhanced outliers detection and removal
    with tab1:
        st.markdown("### 🔧 Data Preprocessing")
        remove_outliers = st.checkbox(
            '🎯 Remove outliers from data',
            help="Filter out statistical outliers using Z-score analysis"
        )

        if remove_outliers:
            st.markdown("#### 📊 Outlier Removal Configuration")

            col1, col2 = st.columns([2, 1])
            with col1:
                outlier_limit = st.slider(
                    'Standard deviation threshold',
                    min_value=1.0,
                    max_value=10.0,
                    value=4.0,
                    step=0.2,
                    help="Data points beyond this many standard deviations will be removed"
                )

            try:
                df_new = df.copy()
                for column in df_new.columns:
                    df_new[column] = pd.to_numeric(df_new[column], errors='coerce')

                with col2:
                    st.markdown("**Before filtering:**")
                    st.metric("📊 Rows", f"{df.shape[0]:,}")

                def df_without_outliers(data, a=4.0):
                    df = data.copy()
                    z_scores = stats.zscore(df[df.describe().columns], nan_policy='omit')
                    z_scores.fillna(0, inplace=True)
                    abs_z_scores = np.abs(z_scores)
                    filtered_entries = (abs_z_scores < a).all(axis=1)
                    df_without_outliers = df[filtered_entries]
                    return df_without_outliers

                df_new = df_without_outliers(df_new, a=outlier_limit)
                df = df.loc[df_new.index]

                with col2:
                    st.markdown("**After filtering:**")
                    st.metric(
                        "📊 Rows",
                        f"{df.shape[0]:,}",
                        delta=f"{df.shape[0] - df_raw.shape[0]:,}"
                    )

                # Show filtering effectiveness
                removed_count = df_raw.shape[0] - df.shape[0]
                removal_pct = (removed_count / df_raw.shape[0]) * 100

                if removed_count > 0:
                    st.success(f"✅ Successfully removed {removed_count:,} outliers ({removal_pct:.1f}%)")
                else:
                    st.info("ℹ️ No outliers detected with current threshold")

            except Exception as e:
                st.error(f"❌ Error during outlier removal: {str(e)}")
                st.warning("⚠️ Proceeding with original dataset")

        st.markdown("---")
        
    # Enhanced chart type selection
    st.sidebar.markdown("### 📈 Visualization Type")

    # Chart type descriptions
    chart_descriptions = {
        'One chart': '📈 Multiple series on a single chart with dual Y-axes',
        'One Chart with re-scaling': '📊 Normalized data for easy comparison across different scales',
        'Many charts': '📋 Individual charts for each data series',
        'Correlations': '🔥 Interactive correlation heatmap to discover relationships',
        'Column vs Top Correlations': '⚡ Find and visualize strongest correlations for any column'
    }

    choice = st.sidebar.radio(
        'Select visualization type:',
        options=list(chart_descriptions.keys()),
        format_func=lambda x: chart_descriptions[x],
        help="Choose the type of visualization that best fits your analysis needs"
    )

    # Display selected choice info
    st.sidebar.markdown(f"""
    <div class="info-card">
        <h4>Selected: {choice}</h4>
        <p style="font-size: 0.9rem; margin: 0;">{chart_descriptions[choice]}</p>
    </div>
    """, unsafe_allow_html=True)

    st.sidebar.markdown("---")

    # Determine plot style based on date status
    if st.session_state['date_status']:
        style = 'lines+markers'
        st.sidebar.markdown("""
        <div class="status-indicator status-info">
            📈 Time-series mode (lines + markers)
        </div>
        """, unsafe_allow_html=True)
    else:
        style = 'markers'
        st.sidebar.markdown("""
        <div class="status-indicator status-info">
            📊 Scatter plot mode (markers only)
        </div>
        """, unsafe_allow_html=True)

    if choice=='One chart':
        X=st.sidebar.selectbox('Choose X Axis',df.columns)
        Y_1=st.sidebar.multiselect('Choose primary Y Axis',df.columns)
        Y_2=st.sidebar.multiselect('Choose 2ndry Y Axis',df.columns)
        if df[X].dtype== 'datetime64[ns]' and k==True :
            pass
        else:
            df[X]=pd.to_numeric(df[X],errors='coerce')
        for column in Y_1:
            if df[column].dtype =='datetime64[ns]' and k==True:
                pass
            else:
                df[column]=pd.to_numeric(df[column],errors='coerce')
        for column in Y_2:
            if df[column].dtype =='datetime64[ns]' and k==True:
                pass
            else:
                df[column]=pd.to_numeric(df[column],errors='coerce')
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        try:
            for column in Y_1:
                if gl==True:
                    fig.add_trace(go.Scattergl(x=df[X], y=df[column],mode=style, name=column)) # 1st y axis
                else:
                    fig.add_trace(go.Scatter(x=df[X], y=df[column],mode=style, name=column)) # 1st y axis
        except:
            pass
        try:
            for column in Y_2:
                if gl==True:
                    fig.add_trace(go.Scattergl(x=df[X], y=(df[column]),mode=style, name=column), secondary_y=True) # 2nd y axis
                else:
                    fig.add_trace(go.Scatter(x=df[X], y=(df[column]),mode=style, name=column), secondary_y=True) # 2nd y axis
        except:
            pass
        #fig.update_layout(xaxis_title=X, yaxis_title=Y_1) # set name for X axis & primary Y axis
        #fig.update_yaxes(title_text=Y_2, secondary_y=True) # Set name for secondry y axis and range
        st.plotly_chart(fig)
        
    if choice=='One Chart with re-scaling':
        auto_scale=st.sidebar.radio(label="choose",options=['All columns included','All columns included except some','Manually choose included columns'],index=2,key='auto_scale')
        min = st.sidebar.number_input('input minimum number for Y re-scaling')
        max = st.sidebar.number_input('input maximum number for Y re-scaling')
        if auto_scale=='Manually choose included columns':            
            X=st.sidebar.selectbox('Choose  X axis',df.columns)
            if df[X].dtype== 'datetime64[ns]' and k==True :
                pass
            else:
                df[X]=pd.to_numeric(df[X],errors='coerce')
            columnss= st.sidebar.multiselect('Choose the list of columns to be plotted on Y',df.columns)
            fig = go.Figure()
            for column in columnss:
                try:
                    if df[column].dtype=='datetime64[ns]' and k==True:
                        pass
                    else:
                        df[column]=pd.to_numeric(df[column],errors='coerce')
                except:
                    st.write(f'The column {column} can not be plotted, kindly review its data')
                    continue
            try:
                scaler = MinMaxScaler((min,max))
                scaler.fit(df[columnss])
                df_transformed=pd.DataFrame(scaler.transform(df[columnss]),columns=columnss)
                for column in df_transformed.columns:
                    if gl==True:
                        fig.add_trace(go.Scattergl(x=df[X], y=df_transformed[column],mode=style, name=column))
                    else:
                        fig.add_trace(go.Scatter(x=df[X], y=df_transformed[column],mode=style, name=column))
                st.plotly_chart(fig)
            except:
                pass
        elif auto_scale=='All columns included':
            X=st.sidebar.selectbox('Choose  X axis',df.columns)
            if df[X].dtype== 'datetime64[ns]' and k==True :
                pass
            else:
                df[X]=pd.to_numeric(df[X],errors='coerce')
            columnss= df.columns.difference([X])
            fig = go.Figure()
            for column in columnss:
                try:
                    if df[column].dtype=='datetime64[ns]' and k==True:
                        pass
                    else:
                        df[column]=pd.to_numeric(df[column],errors='coerce')
                except:
                    st.write(f'The column {column} can not be plotted, kindly review its data')
                    continue
            try:
                scaler = MinMaxScaler((min,max))
                scaler.fit(df[columnss])
                df_transformed=pd.DataFrame(scaler.transform(df[columnss]),columns=columnss)
                for column in df_transformed.columns:
                    if gl==True:
                        fig.add_trace(go.Scattergl(x=df[X], y=df_transformed[column],mode=style, name=column))
                    else:
                        fig.add_trace(go.Scatter(x=df[X], y=df_transformed[column],mode=style, name=column))
                st.plotly_chart(fig)
            except:
                pass
        elif auto_scale=='All columns included except some':
            X=st.sidebar.selectbox('Choose  X axis',df.columns)
            if df[X].dtype== 'datetime64[ns]' and k==True :
                pass
            else:
                df[X]=pd.to_numeric(df[X],errors='coerce')
            excepted_columns= st.sidebar.multiselect('Choose the list of columns to be execluded, all other columns will be plotted on Y',df.columns)    
            columnss= df.drop(excepted_columns,axis=1).columns
            fig = go.Figure()
            for column in columnss:
                try:
                    if df[column].dtype=='datetime64[ns]' and k==True:
                        pass
                    else:
                        df[column]=pd.to_numeric(df[column],errors='coerce')
                except:
                    st.write(f'The column {column} can not be plotted, kindly review its data')
                    continue
            try:
                scaler = MinMaxScaler((min,max))
                scaler.fit(df[columnss])
                df_transformed=pd.DataFrame(scaler.transform(df[columnss]),columns=columnss)
                for column in df_transformed.columns:
                    if gl==True:
                        fig.add_trace(go.Scattergl(x=df[X], y=df_transformed[column],mode=style, name=column))
                    else:
                        fig.add_trace(go.Scatter(x=df[X], y=df_transformed[column],mode=style, name=column))
                st.plotly_chart(fig)
            except:
                pass    
  

    if choice=='Many charts':
        many_choices=st.sidebar.radio(label="choose",options=['All columns included','All columns included except some','Manually choose included columns'],index=2,key='many_choices')
        if many_choices=='Manually choose included columns':
            X=st.sidebar.selectbox('Choose the fixed column on X',df.columns)
            if df[X].dtype== 'datetime64[ns]' and k==True :
                pass
            else:
                df[X]=pd.to_numeric(df[X],errors='coerce')
            columns= st.sidebar.multiselect('choose the list of columns to be plotted on Y',df.columns)
            for column in columns:
                try:
                    if df[column].dtype=='datetime64[ns]' and k==True:
                        pass
                    else:
                        df[column]=pd.to_numeric(df[column],errors='coerce')
                    fig = go.Figure()
                    if gl==True:
                        fig.add_trace(go.Scattergl(x=df[X], y=df[column],mode=style))
                    else:    
                        fig.add_trace(go.Scatter(x=df[X], y=df[column],mode=style))
                    fig.update_layout(xaxis_title=X, yaxis_title=column)
                    st.plotly_chart(fig)
                except:
                    st.write(f'The column {column} can not be plotted, kindly review its data')
                    continue

        elif many_choices=='All columns included':
            X=st.sidebar.selectbox('Choose the fixed column on X',df.columns)
            if df[X].dtype== 'datetime64[ns]' and k==True :
                pass
            else:
                df[X]=pd.to_numeric(df[X],errors='coerce')  
            for column in df.columns:
                try:
                    if df[column].dtype=='datetime64[ns]' and k==True:
                        pass
                    else:
                        df[column]=pd.to_numeric(df[column],errors='coerce')
                    fig = go.Figure()
                    if gl==True:
                        fig.add_trace(go.Scattergl(x=df[X], y=df[column],mode=style))
                    else:
                        fig.add_trace(go.Scatter(x=df[X], y=df[column],mode=style))
                    fig.update_layout(xaxis_title=X, yaxis_title=column)
                    st.plotly_chart(fig)
                except:
                    st.write(f'The column {column} can not be plotted, kindly review its data')
                    continue
                
        elif many_choices=='All columns included except some':
            X=st.sidebar.selectbox('Choose the fixed column on X',df.columns)
            if df[X].dtype== 'datetime64[ns]' and k==True :
                pass
            else:
                df[X]=pd.to_numeric(df[X],errors='coerce')
            excepted_columns= st.sidebar.multiselect('Choose the list of columns to be execluded, all other columns will be plotted',df.columns)    
            columnss= df.drop(excepted_columns,axis=1).columns
            fig = go.Figure()
            for column in columnss:
                try:
                    if df[column].dtype=='datetime64[ns]' and k==True:
                        pass
                    else:
                        df[column]=pd.to_numeric(df[column],errors='coerce')
                    fig = go.Figure()
                    if gl==True:
                        fig.add_trace(go.Scattergl(x=df[X], y=df[column],mode=style))
                    else:
                        fig.add_trace(go.Scatter(x=df[X], y=df[column],mode=style))
                    fig.update_layout(xaxis_title=X, yaxis_title=column)
                    st.plotly_chart(fig)
                except:
                    st.write(f'The column {column} can not be plotted, kindly review its data')
                    continue 
            

    if choice=='Correlations':
        correlations=st.sidebar.radio(label="choose",options=['All columns included','All columns included except some','Manually choose included columns'],index=2,key='correlations')
        if correlations=='Manually choose included columns':            
            columnss= st.sidebar.multiselect('Choose the list of columns to be correlated',df.columns)
            corr=df[columnss].corr()
            st.write('********************************************')
            st.write('correlation Matrix :')
            st.write(corr)
            fig = go.Figure()
            fig.add_trace(go.Heatmap(x = corr.columns,y = corr.index,z = np.array(corr)))
            #x = list(corr.columns)
            #y = list(corr.index)
            #z = np.array(corr)
            #fig = ff.create_annotated_heatmap(z,x = x,y = y ,annotation_text = np.around(z, decimals=2),hoverinfo='z',colorscale='Viridis')
            st.plotly_chart(fig)


        elif correlations=='All columns included':
            corr=df.corr()
            st.write('********************************************')
            st.write('correlation Matrix :')
            st.write(corr)
            fig = go.Figure()
            fig.add_trace(go.Heatmap(x = corr.columns,y = corr.index,z = np.array(corr)))
            st.plotly_chart(fig)
            #x = list(corr.columns)
            #y = list(corr.index)
            #z = np.array(corr)
            #fig = ff.create_annotated_heatmap(z,x = x,y = y ,annotation_text = np.around(z, decimals=2),hoverinfo='z',colorscale='Viridis')
            

        elif correlations=='All columns included except some':
            excepted_columns= st.sidebar.multiselect('Choose the list of columns to be execluded, all other columns will be correlated',df.columns)    
            columnss= df.drop(excepted_columns,axis=1).columns
            corr=df[columnss].corr()
            st.write('********************************************')
            st.write('correlation Matrix :')
            st.write(corr)
            fig = go.Figure()
            fig.add_trace(go.Heatmap(x = corr.columns,y = corr.index,z = np.array(corr)))
            st.plotly_chart(fig)


    if choice=='Column vs Top Correlations':
        st.subheader('Column vs Top Correlations Analysis')
        
        # Create correlation matrix for all numeric columns
        df_numeric = df.copy()
        for column in df_numeric.columns:
            if df_numeric[column].dtype == 'datetime64[ns]' and k==True:
                pass
            else:
                df_numeric[column] = pd.to_numeric(df_numeric[column], errors='coerce')
        
        # Calculate correlation matrix
        corr = df_numeric.corr()
        
        if corr.empty:
            st.error("No numeric columns found for correlation analysis.")
        else:
            # User inputs - X axis can be from original df (including dates), correlation analysis from numeric df
            X_corr = st.sidebar.selectbox('Choose X Axis for correlation plots:', df.columns)
            selected_column = st.sidebar.selectbox('Choose the main column for correlation analysis:', corr.columns)
            num_correlations = st.sidebar.slider('Number of top correlations to show:', 1, min(50, len(corr.columns)-1), 3)
            plot_type = st.sidebar.radio('Choose plot type:', ['Dynamic (Plotly)', 'Static (Matplotlib)'], key='plot_type_corr')
            
            # Handle X axis data type conversion (from original df)
            if df[X_corr].dtype == 'datetime64[ns]' and k==True:
                x_data = df[X_corr]
            else:
                x_data = pd.to_numeric(df[X_corr], errors='coerce')
            
            if selected_column in corr.columns:
                # Find top correlations (excluding the column itself)
                correlations = corr[selected_column].drop(labels=[selected_column]).dropna()
                # Sort by absolute value to get strongest correlations (positive or negative)
                top_correlations = correlations.reindex(correlations.abs().sort_values(ascending=False).index).head(num_correlations)
                
                st.write(f"**Top {num_correlations} correlations for '{selected_column}':**")
                st.dataframe(top_correlations.to_frame(name='Correlation'))
                
                # Create individual plots using original df for plotting
                for i, (corr_column, corr_value) in enumerate(top_correlations.items()):
                    
                    if plot_type == 'Dynamic (Plotly)':
                        # Plotly plots (existing code)
                        fig = make_subplots(specs=[[{"secondary_y": True}]])
                        
                        # Add main column (primary y-axis) - from original df
                        if gl==True:
                            fig.add_trace(go.Scattergl(
                                x=x_data,
                                y=df[selected_column],
                                mode=style,
                                name=f'{selected_column}',
                                line=dict(color='blue')
                            ), secondary_y=False)
                            
                            # Add correlated column (secondary y-axis) - from original df
                            fig.add_trace(go.Scattergl(
                                x=x_data,
                                y=df[corr_column],
                                mode=style,
                                name=f'{corr_column}',
                                line=dict(color='red', dash='dot')
                            ), secondary_y=True)
                        else:
                            fig.add_trace(go.Scatter(
                                x=x_data,
                                y=df[selected_column],
                                mode=style,
                                name=f'{selected_column}',
                                line=dict(color='blue')
                            ), secondary_y=False)
                            
                            # Add correlated column (secondary y-axis) - from original df
                            fig.add_trace(go.Scatter(
                                x=x_data,
                                y=df[corr_column],
                                mode=style,
                                name=f'{corr_column}',
                                line=dict(color='red', dash='dot')
                            ), secondary_y=True)
                        
                        # Update layout
                        fig.update_layout(
                            title=f'{selected_column} vs {corr_column}<br>Correlation: {corr_value:.3f}',
                            legend_title="Columns"
                        )
                        fig.update_yaxes(title_text=f"<b>{selected_column}</b>", secondary_y=False)
                        fig.update_yaxes(title_text=f"<b>{corr_column}</b>", secondary_y=True)
                        fig.update_xaxes(title_text=X_corr)
                        
                        st.plotly_chart(fig)
                    
                    else:  # Static (Matplotlib)
                        # Matplotlib plots
                        fig, ax1 = plt.subplots(figsize=(10, 6))
                        
                        # Plot main column on primary y-axis
                        color1 = 'tab:blue'
                        ax1.set_xlabel(X_corr)
                        ax1.set_ylabel(selected_column, color=color1)
                        
                        if style == 'lines+markers':
                            ax1.plot(x_data, df[selected_column], color=color1, marker='o', linestyle='-', markersize=3, label=selected_column)
                        else:
                            ax1.scatter(x_data, df[selected_column], color=color1, s=20, label=selected_column)
                        
                        ax1.tick_params(axis='y', labelcolor=color1)
                        
                        # Create secondary y-axis for correlated column
                        ax2 = ax1.twinx()
                        color2 = 'tab:red'
                        ax2.set_ylabel(corr_column, color=color2)
                        
                        if style == 'lines+markers':
                            ax2.plot(x_data, df[corr_column], color=color2, marker='s', linestyle='--', markersize=3, label=corr_column)
                        else:
                            ax2.scatter(x_data, df[corr_column], color=color2, s=20, marker='s', label=corr_column)
                        
                        ax2.tick_params(axis='y', labelcolor=color2)
                        
                        # Title and layout
                        plt.title(f'{selected_column} vs {corr_column}\nCorrelation: {corr_value:.3f}', fontsize=12)
                        
                        # Add legends
                        lines1, labels1 = ax1.get_legend_handles_labels()
                        lines2, labels2 = ax2.get_legend_handles_labels()
                        ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper right')
                        
                        plt.tight_layout()
                        st.pyplot(fig)
                        plt.close()  # Close figure to free memory
            else:
                st.error(f"Column '{selected_column}' not found in correlation matrix.")


    st.sidebar.write('======================================')
    st.sidebar.write('=======================================')
    
