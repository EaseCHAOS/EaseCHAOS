from extract.extract_table import get_time_table
from extract.utils import save_to_excel


el_table = get_time_table("../data/data1.xlsx", "CE 1")
save_to_excel(el_table, "CE_1.xlsx")
