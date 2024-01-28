import pandas as pd
import xlsxwriter


def save_to_excel(df: pd.DataFrame, filename: str) -> None:
    """
    Save the dataframe to an excel file.

    Parameters
    ----------
    df : pandas.DataFrame
        The dataframe to save.
    filename : str
        The filename to save the dataframe to.
    """
    
    writer = pd.ExcelWriter(filename, engine='xlsxwriter')
    df.to_excel(writer, index=True, sheet_name='Sheet1')
    
    workbook = writer.book
    worksheet = writer.sheets['Sheet1']
    wrap_format = workbook.add_format({'text_wrap': True, 'align': 'center'})

    worksheet.set_column('A:XFD', 30, wrap_format)

    for row in range(df.shape[0] + 1):
        worksheet.set_row(row, 60)

    
    writer.close()
