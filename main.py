import os
import io
import base64

import pandas as pd

import pyarrow as pa

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
    <a class="navbar-brand" href="/" style="padding-left: 30px;">EaseCHAOS</a>
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


file_col, class_col = st.columns((2, 3))

with file_col:
    existing_drafts = os.listdir('existing_drafts')
    raw_file = st.selectbox('Pick a general timetable', existing_drafts)
    raw_file = os.path.join('existing_drafts', raw_file)

with class_col:
    programs = ['Choose a program', 'EL', 'CE', 'RP', 'ME', 'MA', 'PG', 'NG', 'LT', 'LA', 'MC','SD', 'CY', 'MN', 'RN', 'GM', 'GL', 'ES', 'PE', 'IS', 'CH', 'MR', 'EC']
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
    screen_width = streamlit_js_eval(js_expressions='screen.width', key = 'SCR')
    if screen_width is not None and screen_width > 768:
        html_table = table.to_html().replace("\\n","<br>").replace("NaN", "")
        st.write(html_table, unsafe_allow_html=True)
    else:
        st.spinner('Extracting time table...')
        st.dataframe(table)


    with pd.ExcelWriter(table_in_memory, engine='xlsxwriter') as writer:
        workbook = writer.book
        if class_to_extract_for not in workbook.sheetnames:
            workbook.add_worksheet(class_to_extract_for)
        worksheet = writer.sheets[class_to_extract_for]

        format = workbook.add_format({ 'border': 1, 'text_wrap': True, 'align': 'center', 'valign': 'vcenter', 'font_size': 12, 'font': 'Monaco'})
        header_format = workbook.add_format({'bold': True, 'align': 'center', 'valign': 'vcenter', 'font_size': 14, 'border': 1, 'font': 'Monaco'})
        no_border_format = workbook.add_format()  

        # Apply the no_border_format to the entire worksheet
        worksheet.set_column('A:P', 44, no_border_format)

        # Write the column headers with the header_format
        for col_num, value in enumerate(table.columns.values):
            worksheet.write(0, col_num + 1, value, header_format)
        worksheet.write(0, 0, table.index.name, header_format)  # Write the name of the index

        # Write the row headers with the header_format
        for row_num, value in enumerate(table.index.values):
            worksheet.write(row_num + 1, 0, value, header_format)  # Write the values of the index

        # Write the DataFrame to the Excel file
        for row in range(table.shape[0]):
            # Increase the height of the rows
            worksheet.set_row(row + 1, 75, format)

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
                        format,
                    )
                elif cell_value != "nan":
                    worksheet.write(row + 1, col + 1, cell_value, format)

            # Handle the last column separately
            last_col_value = str(table.iloc[row, table.shape[1] - 1]).strip()
            if last_col_value != "nan":
                worksheet.write(row + 1, table.shape[1], last_col_value, format)

        # Write the DataFrame to the Excel file without the headers and index
        table.to_excel(writer, startrow=1, startcol=1, index=False, header=False, sheet_name=class_to_extract_for)
   
   
    # with pd.ExcelWriter(table_in_memory, engine='xlsxwriter') as writer:
    #     workbook = writer.book
    #     if class_to_extract_for not in workbook.sheetnames:
    #         workbook.add_worksheet(class_to_extract_for)
    #     worksheet = writer.sheets[class_to_extract_for]

    #     wrap_format = workbook.add_format({'text_wrap': True, 'align': 'center', 'valign': 'vcenter', 'font_size': 13})
    #     header_format = workbook.add_format({'bold': True, 'align': 'center', 'valign': 'vcenter', 'font_size': 14, 'border': 1})

    #     # Increase the width of the columns and apply the wrap_format
    #     worksheet.set_column('A:P', 44, wrap_format)

    #     # Write the column headers with the header_format
    #     for col_num, value in enumerate(table.columns.values):
    #         worksheet.write(0, col_num + 1, value, header_format)
    #     worksheet.write(0, 0, table.index.name, header_format)  # Write the name of the index

    #     # Write the row headers with the header_format
    #     for row_num, value in enumerate(table.index.values):
    #         worksheet.write(row_num + 1, 0, value, header_format)  # Write the values of the index

    #     # Write the DataFrame to the Excel file
    #     for row in range(table.shape[0]):
    #         # Increase the height of the rows
    #         worksheet.set_row(row + 1, 70, wrap_format)

    #         for col in range(table.shape[1] - 1):  # -1 is moved here to avoid checking inside the loop
    #             cell_value = str(table.iloc[row, col]).strip()
    #             next_cell_value = str(table.iloc[row, col + 1]).strip()

    #             if cell_value == next_cell_value and cell_value != "nan":
    #                 worksheet.merge_range(
    #                     row + 1,
    #                     col + 1,
    #                     row + 1,
    #                     col + 2,
    #                     cell_value,
    #                     wrap_format,
    #                 )
    #     # Increase the height of the last row
    #     worksheet.set_row(table.shape[0] + 1, 75, wrap_format)

    #     # Write the DataFrame to the Excel file without the headers and index
    #     table.to_excel(writer, startrow=1, startcol=1, index=False, header=False, sheet_name=class_to_extract_for)

    # with pd.ExcelWriter(table_in_memory, engine='xlsxwriter') as writer:
    #     workbook = writer.book
    #     if class_to_extract_for not in workbook.sheetnames:
    #         workbook.add_worksheet(class_to_extract_for)
    #     worksheet = writer.sheets[class_to_extract_for]

    #     wrap_format = workbook.add_format({'text_wrap': True, 'align': 'center'})
    #     worksheet.set_column('A:XFD', 40, wrap_format)

    #     for row in range(table.shape[0]):
    #         worksheet.set_row(row, 60)

    #         for col in range(table.shape[1] - 1):  # -1 is moved here to avoid checking inside the loop
    #             cell_value = str(table.iloc[row, col]).strip()
    #             next_cell_value = str(table.iloc[row, col + 1]).strip()

    #             if cell_value == next_cell_value and cell_value != "nan":
    #                 worksheet.merge_range(
    #                     row + 1,
    #                     col + 1,
    #                     row + 1,
    #                     col + 2,
    #                     cell_value,
    #                     wrap_format,
    #                 )
    #     worksheet.set_row(table.shape[0], 65)

    #     table.to_excel(writer, index=True, header=True, sheet_name=class_to_extract_for)

    

    b64 = base64.b64encode(table_in_memory.getvalue()).decode()
    href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="{class_to_extract_for}_timetable.xlsx">Download {class_to_extract_for} timetable</a>'
    st.write()
    st.markdown(href, unsafe_allow_html=True)

except Exception as e:
    st.error(f"An error occurred: {e}")
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
