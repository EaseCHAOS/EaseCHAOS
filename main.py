import os
import io
import base64

import pandas as pd

from extract.extract_table import get_time_table
import streamlit as st

from streamlit_js_eval import streamlit_js_eval

@st.cache_data(show_spinner=False)
def catched_get_table(*args, **kwargs):
    with st.spinner('Extracting time table...'):
        return get_time_table(*args, **kwargs)


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
    <a class="navbar-brand" href="#" style="padding-left: 30px;">EaseCHAOS</a>
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

#st.header(f"EaseCHAOS")

upload_source = st.toggle('Upload a general timetable')

file_col, class_col = st.columns((2, 3))

with file_col:
    if upload_source:
        raw_file = st.file_uploader("Upload a general timetable", type=['xlsx'])
    else:
        existing_drafts = os.listdir('existing_drafts')
        raw_file = st.selectbox('Pick a general timetable', existing_drafts)
        raw_file = 'existing_drafts/' + raw_file

with class_col:
    programs = ['Choose a program', 'EL', 'CE', 'RP', 'ME', 'MA', 'PG', 'NG', 'LT', 'LA', 'MC','SD', 'CY', 'MN', 'RN', 'GM', 'GL', 'ES', 'PE', 'IS', 'CH', 'EC']
    levels = ['Choose a level', '100', '200', '300', '400']

    program_col, level_col = st.columns(2)
    with program_col:
        program = st.selectbox('Pick a program', programs)
    with level_col:
        level = st.selectbox('Pick a level', levels)

if program == 'Choose a program':
    st.info('Please select a program')
    st.stop()
if level == 'Choose a level':
    st.info('Please select a level')
    st.stop()
if raw_file is None:
    st.info('Please upload a general timetable')
    st.stop()

class_to_extract_for = program + ' ' + level[0]
try:
    table = catched_get_table(raw_file, class_to_extract_for)
    table_in_memory = io.BytesIO()

    st.title(f"{class_to_extract_for} time table")
    if streamlit_js_eval(js_expressions='screen.width', key = 'SCR') > 768:
        html_table = table.to_html().replace("\\n","<br>").replace("NaN", "")
        st.write(html_table, unsafe_allow_html=True)
    else:
        st.dataframe(table)


    with pd.ExcelWriter(table_in_memory, engine='xlsxwriter') as writer:
        workbook = writer.book
        if class_to_extract_for not in workbook.sheetnames:
            workbook.add_worksheet(class_to_extract_for)
        worksheet = writer.sheets[class_to_extract_for]

        wrap_format = workbook.add_format({'text_wrap': True, 'align': 'center'})
        worksheet.set_column('A:XFD', 30, wrap_format)

        for row in range(table.shape[0]):
            worksheet.set_row(row, 60)

            for col in range(table.shape[1] - 1):  # -1 is moved here to avoid checking inside the loop
                cell_value = str(table.iloc[row, col]).strip()
                next_cell_value = str(table.iloc[row, col + 1]).strip()

                if cell_value == next_cell_value and cell_value != "nan":
                    worksheet.merge_range(
                        row + 1,
                        col + 1,
                        row + 1,
                        col + 2,
                        cell_value,
                        wrap_format,
                    )
        worksheet.set_row(table.shape[0], 65)

        table.to_excel(writer, index=True, header=True, sheet_name=class_to_extract_for)

    

    b64 = base64.b64encode(table_in_memory.getvalue()).decode()
    href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="{class_to_extract_for}_timetable.xlsx">Download {class_to_extract_for} timetable</a>'
    st.write()
    st.markdown(href, unsafe_allow_html=True)

except Exception as e:
    st.error(f"An error occurred: {e}")
    if upload_source:
        st.info('Please be sure the uploaded file is a valid excel file in the format of the general timetable! \n Contact the developers if the error persist.')
    st.stop()
    
with st.expander('About'):
    info = """
    - This app extracts the time table for a particular class for all days.
    - You can upload a general timetable or pick a general timetable from the dropdown.
    - After which, choose a program and level. The app will then extract the time table for you.
    - You can download the time table as an excel file.
    - If you have any questions, please contact the developers at neilohene@gmail.com | kekelidompeh@gmail.com | aarononto909@gmail.com.
    """
    st.markdown(info)
