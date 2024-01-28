from extract.extract_table import get_time_table
from extract.utils import save_to_excel


el_table = get_time_table("data/data1.xlsx", "EL 3")
save_to_excel(el_table, "EL_3.xlsx")
