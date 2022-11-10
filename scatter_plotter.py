import py_compile
import numpy as np
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px
from sklearn.preprocessing import MinMaxScaler
import streamlit as st


st.set_page_config("Simple scatter plotter",":chart_with_downwards_trend:")#,layout="wide",initial_sidebar_state="expanded")

st.title('Simple scatter plotter app')
st.markdown('<p style="background-color:#f8f4f4;color:#6858c4;font-size:24px;border-radius:2%;">Just upload excel file and see great interactive plots</p>', unsafe_allow_html=True)
st.header('=================================')


st.header("How to run the app")
st.markdown("* ##### Upload excel or csv file from the button on the left side bar")
st.markdown("* ##### Click Date checkbox if the uploaded data contains DATE")
st.markdown("* ##### Choose one of the options at the left side bar")
st.markdown("* ##### All plots are shown  in the middle")

data= st.sidebar.file_uploader("Upload your excel/csv file here",type=['csv', 'xls', 'xlsx'],key='1')

if data is not None:
    try:
        df_raw = pd.read_csv(data,encoding_errors='ignore')
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
st.write(' Kindly note that all cells that are not numbers will be converted to empty cells')
try:
    df=df_raw.copy()
except:
    pass
st.sidebar.write('======================================')

if data is not None:

    k=st.sidebar.checkbox('Check this box if the data contains a DATE column')
    if k :
        date=st.sidebar.selectbox('Choose Date column',df.columns)
        df[date]=pd.to_datetime(df[date])

    choice=st.sidebar.radio('Choose one of the following options :',['One chart: Column on X axis Vs Column on Y axis','One chart: Column on X axis Vs Column on Y axis Vs 2ndry  Y axis','One chart-Auto-Scale : Column on X axis Vs many auto re-scaled on Y ','Many charts: Fixed Column on X axis Vs Many Columns on Y axis','Many charts : Fixed column on X axis Vs all other columns on Y axis'])


    if choice=='One chart: Column on X axis Vs Column on Y axis':
        X=st.sidebar.selectbox('Choose X Axis',df.columns)
        Y=st.sidebar.selectbox('Choose Y Axis',df.columns)
        if df[X].dtype== 'datetime64[ns]' and k==True :
            pass
        else:
            df[X]=pd.to_numeric(df[X],errors='coerce')
        if df[Y].dtype =='datetime64[ns]' and k==True:
            pass
        else:
            df[Y]=pd.to_numeric(df[Y],errors='coerce')
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df[X], y=df[Y],mode='markers'))
        fig.update_layout(xaxis_title=X, yaxis_title=Y)
        st.plotly_chart(fig)

    if choice=='One chart: Column on X axis Vs Column on Y axis Vs 2ndry  Y axis':
        X=st.sidebar.selectbox('Choose X Axis',df.columns)
        Y_1=st.sidebar.selectbox('Choose primary Y Axis',df.columns)
        Y_2=st.sidebar.selectbox('Choose 2ndry Y Axis',df.columns) 
        if df[X].dtype== 'datetime64[ns]' and k==True :
            pass
        else:
            df[X]=pd.to_numeric(df[X],errors='coerce')
        if df[Y_1].dtype =='datetime64[ns]' and k==True:
            pass
        else:
            df[Y_1]=pd.to_numeric(df[Y_1],errors='coerce') 
        if df[Y_2].dtype =='datetime64[ns]' and k==True:
            pass
        else:
            df[Y_2]=pd.to_numeric(df[Y_2],errors='coerce')
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(go.Scatter(x=df[X], y=df[Y_1],mode='markers', name=Y_1)) # 1st y axis
        fig.add_trace(go.Scatter(x=df[X], y=(df[Y_2]),mode='markers', name=Y_2), secondary_y=True) # 2nd y axis
        fig.update_layout(xaxis_title=X, yaxis_title=Y_1) # set name for X axis & primary Y axis
        fig.update_yaxes(title_text=Y_2, secondary_y=True) # Set name for secondry y axis and range
        st.plotly_chart(fig)

    if choice=='One chart-Auto-Scale : Column on X axis Vs many auto re-scaled on Y ':
        min = st.sidebar.number_input('input minimum number for Y re-scaling')
        max = st.sidebar.number_input('input maximum number for Y re-scaling')
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
                fig.add_trace(go.Scatter(x=df[X], y=df_transformed[column],mode='markers', name=column))
            st.plotly_chart(fig)
        except:
            pass

            

        

    if choice=='Many charts: Fixed Column on X axis Vs Many Columns on Y axis':
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
                fig.add_trace(go.Scatter(x=df[X], y=df[column],mode='markers'))
                fig.update_layout(xaxis_title=X, yaxis_title=column)
                st.plotly_chart(fig)
            except:
                st.write(f'The column {column} can not be plotted, kindly review its data')
                continue

    if choice=='Many charts : Fixed column on X axis Vs all other columns on Y axis':
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
                fig.add_trace(go.Scatter(x=df[X], y=df[column],mode='markers'))
                fig.update_layout(xaxis_title=X, yaxis_title=column)
                st.plotly_chart(fig)
            except:
                st.write(f'The column {column} can not be plotted, kindly review its data')
                continue
    st.sidebar.write('======================================')
    st.sidebar.write('======================================')
    st.sidebar.write('======================================')






    


    





    