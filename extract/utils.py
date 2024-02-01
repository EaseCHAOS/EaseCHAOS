import pandas as pd

def save_to_excel(df: pd.DataFrame, filename: str) -> None:
    writer = pd.ExcelWriter(filename, engine="xlsxwriter")
    df.to_excel(writer, index=True, sheet_name="Sheet1")

    workbook = writer.book
    worksheet = writer.sheets["Sheet1"]
    wrap_format = workbook.add_format(
        {"text_wrap": True, "align": "center", "valign": "vcenter"}
    )

    worksheet.set_column("A:XFD", 30, wrap_format)

    for row in range(df.shape[0]):
        worksheet.set_row(row, 60)

        row_values = df.iloc[row].astype(str).str.strip().tolist()
        for col in range(df.shape[1] - 1):  # -1 is moved here to avoid checking inside the loop
            cell_value = row_values[col]
            next_cell_value = row_values[col + 1]

            if cell_value == next_cell_value and cell_value != "nan":
                worksheet.merge_range(
                    row + 1,
                    col + 1,
                    row + 1,
                    col + 2,
                    cell_value,
                    wrap_format,
                )
    worksheet.set_row(df.shape[0], 65)

    writer.close()