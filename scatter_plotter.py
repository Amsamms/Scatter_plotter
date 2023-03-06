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


st.set_page_config("Simple scatter plotter",":chart_with_downwards_trend:")#,layout="wide",initial_sidebar_state="expanded")

st.title('Simple scatter plotter app')
st.markdown('<p style="background-color:#f8f4f4;color:#6858c4;font-size:24px;border-radius:2%;">Just upload excel file and see great interactive plots</p>', unsafe_allow_html=True)
st.header('=================================')

tab1,tab2= st.tabs(["How to run the app", " Video description of the app"])

with tab1:
    st.header("How to run the app")
    st.markdown("* ##### Upload excel or csv file from the button on the left side bar")
    st.markdown("* ##### Click Date checkbox if the uploaded data contains DATE")
    st.markdown("* ##### Choose one of the options at the left side bar")
    st.markdown("* ##### All plots are shown  in the middle")

with tab2:
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
st.write(' Kindly note that all cells that are not numbers will be converted to empty cells')
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

    choice=st.sidebar.radio('Choose one of the following options :',['One chart','One Chart with re-scaling','Many charts','Correlations'])
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


    st.sidebar.write('======================================')
    st.sidebar.write('======================================')
    