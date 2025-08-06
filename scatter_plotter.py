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


st.set_page_config("Simple scatter plotter",":chart_with_downwards_trend:")#,layout="wide",initial_sidebar_state="expanded")

st.title('Simple scatter plotter app')
st.markdown('<p style="background-color:#f8f4f4;color:#6858c4;font-size:24px;border-radius:2%;">Just upload excel file and see great interactive plots</p>', unsafe_allow_html=True)
st.header('=================================')

tab1,tab2,tab3= st.tabs(["main app","How to run the app", " Video description of the app"])

with tab1:
    st.header("Display Area")

    
with tab2:
    st.header("How to use")
    st.markdown(
        """
        1. Start by uploading an Excel or CSV file. This can be done through the 'Upload your excel/csv file here' button located on the left sidebar. Ensure that your file contains a single sheet and the column names are defined in the first row.
        2. If your data contains a 'DATE' column, make sure to check the 'Check this box if the data contains a DATE column' checkbox on the left sidebar.
        3. Depending on your needs, you can choose one of the following options from the left sidebar:
            - One chart: This option allows you to plot multiple series on a single chart. You can specify the series for the primary and secondary Y axes.
            - One Chart with re-scaling: This option also plots multiple series on a single chart, but with re-scaling of data for better comparison.
            - Many charts: This option creates individual charts for each series.
            - Correlations: This option allows you to create a correlation matrix and plot a heatmap of the correlations.
            - Column vs Top Correlations: This option lets you select a specific column and find its most highly correlated columns, then creates individual plots showing the selected column against each highly correlated column.
        4. The generated plots will be displayed in the middle of the screen. If the 'Remove outliers' checkbox is selected, the application will remove outliers from the data before plotting. The threshold for outlier removal can be adjusted using the slider.
        5. If your data contains a large number of points, check the 'Check this box if the data contains a large number of points' checkbox for better performance.
        """
    )
    st.write(' Kindly note that all cells that are not numbers will be converted to empty cells')
    

with tab3:
    st.markdown(" Check the video below")
    st.video('https://youtu.be/W8CR1zD15l0')




data= st.sidebar.file_uploader("Upload your excel/csv file here",type=['csv', 'xls', 'xlsx'],key='1')

if data is not None:
    try:
        df_raw = pd.read_csv(data,encoding_errors='ignore')
    except:
        pass
    try:
        df_raw = pd.read_csv(data)
    except:
        pass

    try:
        df_raw = pd.read_excel(data)
    except:
        pass
    try:
        df_raw=pd.read_excel(data,engine='openpyxl')
    except:
        pass
else:
    st.sidebar.write('*Kindly upload valid excel or csv data with one sheet and columns names are in the first raw')
    
try: 
    st.dataframe(df_raw)
except:
    pass

try:
    df=df_raw.copy()
except:
    pass
st.sidebar.write('======================================')

if data is not None:

    k=st.sidebar.checkbox('Check this box if the data contains a DATE column',key='date_status')
    if k :
        date=st.sidebar.selectbox('Choose Date column',df.columns)
        df[date]=pd.to_datetime(df[date])
    gl=st.sidebar.checkbox('Check this box if the data contains large number of points',key='gl')
    st.sidebar.write('======================================')
    
    #outliers detection and removal
    if st.checkbox('Remove outliers'):
        st.markdown('#### Standard Deviation')
        try:
            df_new=df.copy()
            for column in df_new.columns:
                # Check if the column is numeric
                df_new[column] = pd.to_numeric(df_new[column], errors='coerce')
            #outlier function that is used in machine learning app   
            outlier_limit=st.slider('Number of Standard deviations data will be filtered upon',1.0,10.0,4.0,0.2)
            st.write(f'data initial raws are {df.shape[0]}')
            def df_without_outliers (data,a=4.0):
                df=data.copy()    
                z_scores = stats.zscore(df[df.describe().columns],nan_policy='omit')
                z_scores.fillna(0,inplace=True)   # in case one column is filled with nan values
                abs_z_scores = np.abs(z_scores)
                filtered_entries = (abs_z_scores < a).all(axis=1)
                df_without_outliers = df[filtered_entries]
                return df_without_outliers
            df_new = df_without_outliers(df_new, a= outlier_limit)
            df=df.loc[df_new.index]
            st.write(f'data new raws are {df.shape[0]}')
        except Exception as e:
            st.write(f"An error occurred: {type(e).__name__}")
            st.write(f"Error message: {e}")
            st.write('dataset could not be outliers removed')
            pass
        
    choice=st.sidebar.radio('Choose one of the following options :',['One chart','One Chart with re-scaling','Many charts','Correlations','Column vs Top Correlations'])
    st.sidebar.write('======================================')
    if st.session_state['date_status']:
        style='lines+markers'
    else:
        style='markers'

    if choice=='One chart':
        X=st.sidebar.selectbox('Choose X Axis',df.columns)
        Y_1=st.sidebar.multiselect('Choose primary Y Axis',df.columns)
        Y_2=st.sidebar.multiselect('Choose 2ndry Y Axis',df.columns) 
        if df[X].dtype== 'datetime64[ns]' and k==True :
            pass
        else:
            df[X]=pd.to_numeric(df[X],errors='coerce')
        for column in df[Y_1].columns:    
            if df[column].dtype =='datetime64[ns]' and k==True:
                pass
            else:
                df[column]=pd.to_numeric(df[column],errors='coerce') 
        for column in df[Y_2].columns:    
            if df[column].dtype =='datetime64[ns]' and k==True:
                pass
            else:
                df[column]=pd.to_numeric(df[column],errors='coerce') 
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        try:
            for column in df[Y_1].columns:
                if gl==True:
                    fig.add_trace(go.Scattergl(x=df[X], y=df[column],mode=style, name=column)) # 1st y axis
                else:    
                    fig.add_trace(go.Scatter(x=df[X], y=df[column],mode=style, name=column)) # 1st y axis
        except:
            pass
        try:
            for column in df[Y_2].columns:
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
            # User inputs
            selected_column = st.sidebar.selectbox('Choose the main column for correlation analysis:', df_numeric.columns)
            num_correlations = st.sidebar.slider('Number of top correlations to show:', 1, min(50, len(corr.columns)-1), 10)
            
            if selected_column in corr.columns:
                # Find top correlations (excluding the column itself)
                correlations = corr[selected_column].drop(labels=[selected_column]).dropna()
                # Sort by absolute value to get strongest correlations (positive or negative)
                top_correlations = correlations.reindex(correlations.abs().sort_values(ascending=False).index).head(num_correlations)
                
                st.write(f"**Top {num_correlations} correlations for '{selected_column}':**")
                st.dataframe(top_correlations.to_frame(name='Correlation'))
                
                # Create individual plots
                for i, (corr_column, corr_value) in enumerate(top_correlations.items()):
                    fig = make_subplots(specs=[[{"secondary_y": True}]])
                    
                    # Add main column (primary y-axis)
                    if gl==True:
                        fig.add_trace(go.Scattergl(
                            x=df[X] if 'X' in locals() and X in df.columns else range(len(df)),
                            y=df[selected_column],
                            mode=style,
                            name=f'{selected_column}',
                            line=dict(color='blue')
                        ), secondary_y=False)
                        
                        # Add correlated column (secondary y-axis)
                        fig.add_trace(go.Scattergl(
                            x=df[X] if 'X' in locals() and X in df.columns else range(len(df)),
                            y=df[corr_column],
                            mode=style,
                            name=f'{corr_column}',
                            line=dict(color='red', dash='dot')
                        ), secondary_y=True)
                    else:
                        fig.add_trace(go.Scatter(
                            x=df[X] if 'X' in locals() and X in df.columns else range(len(df)),
                            y=df[selected_column],
                            mode=style,
                            name=f'{selected_column}',
                            line=dict(color='blue')
                        ), secondary_y=False)
                        
                        # Add correlated column (secondary y-axis)
                        fig.add_trace(go.Scatter(
                            x=df[X] if 'X' in locals() and X in df.columns else range(len(df)),
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
                    
                    if 'X' in locals() and X in df.columns:
                        fig.update_xaxes(title_text=X)
                    else:
                        fig.update_xaxes(title_text="Index")
                    
                    st.plotly_chart(fig)
            else:
                st.error(f"Column '{selected_column}' not found in correlation matrix.")


    st.sidebar.write('======================================')
    st.sidebar.write('=======================================')
    