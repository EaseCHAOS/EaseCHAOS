from extract.extract_table import get_time_table
from extract.utils import save_to_excel
import streamlit as st
import pandas as pd
import io
import base64



# el_table = get_time_table("data/D3.xlsx", "RP 3")
# save_to_excel(el_table, "RP_3.xlsx")

st.set_page_config(layout="wide")

st.markdown(
    '<link href="https://cdnjs.cloudflare.com/ajax/libs/mdbootstrap/4.19.1/css/mdb.css" rel="stylesheet">',
    unsafe_allow_html=True,
)
st.markdown(
    '<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">',
    unsafe_allow_html=True,
)
st.markdown("""""", unsafe_allow_html=True)
st.markdown(
    """
    <nav class="navbar fixed-top navbar-expand-lg navbar-dark" style="background-color: Green;">
    <a class="navbar-brand" href="#" target="_blank" style="padding-left: 30px;">EaseCHAOS</a>
    </nav>
""",
    unsafe_allow_html=True,
)
hide_streamlit_style = """
            <style>
    
                header{visibility:hidden;}
                .main {
                    margin-top: -120px;
                    padding-top:10px;
                }
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}

            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)


st.header(f"EaseCHAOS")

col1, col2 = st.columns(2)

with col1:
    classes = ['EL 1', 'EL 2', 'EL 3', 'CE 1', 'CE2']
    classes = [''] + classes
    class_option = st.selectbox('Pick Class', classes,) 
      

with col2:
    col3, col4 = st.columns(2)
    with col3:
        upload = st.checkbox('Upload A Timetable')
        if upload:
            uploaded_file = st.file_uploader("Upload a Draft", type=['xlsx'])
            if uploaded_file is not None:
                df = pd.read_excel(uploaded_file)
                df.to_excel('data/Draft.xlsx', index=False)
    
    with col4:
        not_upload = st.checkbox('Extract Class Timetable')
        if not_upload:
            drafts = ['Draft 1', 'Draft 2', 'Draft 3']
            drafts = [''] + drafts
            draft_option = st.selectbox('Pick Draft', drafts)

            if class_option and draft_option:
                table = get_time_table(f"data/{draft_option}.xlsx", class_option)
                save_to_excel(table, f"output/{class_option}.xlsx")

                towrite = io.BytesIO()
                downloaded_file = table.to_excel(towrite, index=True, header=True)
                towrite.seek(0)
                b64 = base64.b64encode(towrite.read()).decode()  
                href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}">Download excel file</a> '
                st.markdown(href, unsafe_allow_html=True)
            else:
                pass
            
try:                
    if class_option and draft_option:
        st.dataframe(table)
except NameError:
    pass

    
with st.expander('About'):
    st.write('about here')
