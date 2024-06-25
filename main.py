import streamlit as st
import pandas as pd
from io import StringIO
import chardet
import datetime


# Deploy, 설정 버튼 제거
st.set_page_config(page_title="시험 결과2", page_icon="🧊" )


st.markdown("""
    <style>
        .reportview-container {
            margin-top: 0em;
        }
        #MainMenu, header {visibility: hidden;}
        .stDeployButton {display:none;}
        footer {visibility: hidden;}
        #stDecoration {display:none;}
        .block-container {
            padding-top: 0rem;
            padding-bottom: 0rem;
            padding-left: 5rem;
            padding-right: 5rem;
        }

        [data-testid='stDownloadButton'] {
            position: relative;
            margin: 0;
            position: absolute;
            top: 50%;
            left: 50%;
            -ms-transform: translate(-50%, -50%);
            transform: translate(-50%, -50%);
            text-align: center;
        }
            
        [data-testid='stDataFrame'] {
            position: relative;
            margin: 0;
            width: 100%;
            text-align: center;
        }
        
            
    </style>
""", unsafe_allow_html=True)



st.header('LFC', divider='rainbow')
# st.header('dfa')
st.title('Data Summary')
# st.subheader('파일을 선택하세요')
# st.write('popopo')

# accept_multiple_files=True일때 업로드된 파일이 없으면 false 반환
uploaded_files = st.file_uploader(label='Upload Your Files', accept_multiple_files=True,  type=(["csv","txt"]))


# col_upload = st.columns([3, 1])

# if col_upload[1].button('Clear', type='secondary'):
#     st.rerun()

st.write('  ')
st.divider()
st.write('  ')

if uploaded_files:
    # Start Row Selector
    st.subheader('Select Start Row')
    startRow = st.slider('', 1, 100)

    st.write('  ')
    st.write('  ')
    
    
    file = uploaded_files[0]
    df = pd.read_csv(file, sep=',', on_bad_lines='warn', skiprows=startRow-1)  # read a CSV file inside the 'data" folder next to 'app.py'
    df.style.hide(axis='index')

    col = st.columns([1,0.1,2])
    col[0].subheader('Column')
    col[2].subheader('Upload Data')
    col[2].dataframe(df.head(10), hide_index = True)

    cnt = 0
    option = []
    columnName = []
    for i in df.columns:
        columnName.append(i)
        option.append(col[0].selectbox(i, ("max", "min", "mean", "count")))



    # Data 가공
    result_data = []

    ## 필드명 추가

    result_df = pd.DataFrame()
    
    # row_Header = 'File Name'
    result_df['File Name'] = []
    for i in range(len(option)):
        result_df[df.columns[i] + '_' + option[i]] = []
    # result_data.append(row_Header)


    ## 각 파일에서 데이터 추출
    for f in uploaded_files:
        print('h')
        f.seek(0)  ## uploaded_file에서 파일 위치를 잊는 경우가 있어서 꼭 해줘야함
        

        result = chardet.detect(f.readline())
        


        # st.write(f.name + ' ::::::::::::')

        
        fd = pd.read_csv(f, sep=',', on_bad_lines='warn', skiprows=startRow-1, encoding=result['encoding'])
        fd.style.hide(axis='index')

        # file_data = pd.read_csv(uploaded_files[0], sep=',', on_bad_lines='warn', skiprows=startRow-1)
        dd_fd = fd.describe()


        temp = []
        temp.append(f.name)
        for j in range(len(option)):
            # st.write(option[j], ' :: ', df.columns[j])
            if(len(df.columns) == len(fd.columns)):
                if(df.columns[j] == fd.columns[j]):
                    temp.append(round(dd_fd.at[option[j], df.columns[j]], 2))
                else:
                    temp.append('error')
            else:
                temp.append('error')

        result_df.loc[len(result_df)] = temp



    # st.write(StringIO('\n'.join(result_data)))

    # result_df = pd.read_csv(StringIO('\n'.join(result_data)), sep=',')
        
    st.write('  ')
    st.divider()
    st.subheader('Result')
    result_df.style.hide(axis='index')
    st.dataframe(result_df, hide_index = True)



    # Download button
    now = datetime.datetime.now()
    formatted_date = now.strftime("%y%m%d_%H%M%S")

    print("포맷팅된 날짜:", formatted_date)

    st.write(' ')
    st.write(' ')
    st.download_button('Download', df.to_csv(), file_name='LFC_Summary_' + str(formatted_date) + '.csv')



    st.write(' ')
    st.write(' ')
    st.write(' ')
    st.write(' ')