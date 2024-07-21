import streamlit as st
import pandas as pd
import pickle

st.set_page_config(
    page_title="Student score Prediction App",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

if 'df_input' not in st.session_state:
    st.session_state['df_input'] = pd.DataFrame()
if 'result' not in st.session_state:
    st.session_state['result'] = pd.DataFrame()

path='model/Student_score_model.sav'
model=pickle.load(open(path, 'rb'))
result=pd.DataFrame()


def convert_to_csv(df):
    return df.to_csv(index=False, encoding='utf-8')
@st.cache_data()
def predict_score(df_input):
    df=df_input.copy()
    df.columns=df.columns.str.lower().str.replace(' ','_')
    df['extracurricular_activities']=df['extracurricular_activities'].apply(lambda x: 1 if x.lower()=='yes' else 0)
    if len(df.columns)==5:
        pred=pd.Series(model.predict(df))
        df['result']=pred.apply(lambda x: 100.0 if round(x,0)>100 else 0.0 if round(x,0)<0 else round(x,0))
        return df
    elif len(df.columns)==6:
        df.drop(columns='performance_index', inplace=True)
        pred=pd.Series(model.predict(df))
        df['result']=pred.apply(lambda x: 100.0 if round(x,0)>100 else 0.0 if round(x,0)<0 else round(x,0))
        return df
    else:
        return pd.DataFrame()

with st.sidebar:
    st.title("enter data")
    tab1,tab2=st.tabs(['upload file','enter data'])
    with tab1:
        file=st.file_uploader("Upload your file(csv,xlsx)",type=['csv','xlsx'])
        if file:
            st.session_state['df_input']=pd.read_csv(file)
        button=st.button("predict",type='primary',key='tab1')
        if button:
            if not st.session_state['df_input'].empty:
                st.session_state['result']=predict_score(st.session_state['df_input'])
            else:
                st.write("No data")
    with tab2:

        hours_studied=st.number_input('hours studied',min_value=1)
        pre_score=st.number_input('previous score',min_value=1, max_value=100)
        extr_act=st.selectbox('extracurricular activities',['yes','no'])
        sleep_hours=st.number_input('sleep hours',min_value=1)
        test_practised=st.number_input('sample question papers practiced',min_value=0)
        l=[hours_studied,pre_score,extr_act,sleep_hours,test_practised]
        signal=[1 if i is not None else 0 for i in l]
        if 0 not in signal:
            tab2_button=st.button('predict',type='primary',key='tab2')
        if tab2_button:
            st.session_state['df_input']=pd.DataFrame({
                    'hours_studied': hours_studied,
                    'previous_scores': pre_score,
                    'extracurricular_activities': extr_act,
                    'sleep_hours': sleep_hours,
                    'sample_question_papers_practiced': test_practised,
                }, index=[0])
            st.session_state['result']=predict_score(st.session_state['df_input'])

if not st.session_state['result'].empty:
    st.write(st.session_state['result'])
    res_risky_csv = convert_to_csv(st.session_state['result'])
    st.download_button(
        label="Download result",
        data=res_risky_csv,
        file_name='student_score.csv',
        mime='text/csv',
    )
else:
    st.write("u havent given data or ur data isnt supported")

