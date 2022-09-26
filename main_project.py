# from bs4 import BeautifulSoup
# import pandas as pd
# install pandas,xlwt, openpyxl
import os
from multiprocessing.util import info
from vib_func import *
from file_manager import *

# This dictionary stores the final dataframes for each correspinding
# report. 
report_catgs = report_types()
reports_dic = {v: pd.DataFrame() for v in report_catgs}

files = folder_opener()
cwd = os.getcwd()
folder_path = f'{cwd}'.replace('\\', '/')

for file in files:
    fixed_name = f'{folder_path}/{file}'
    try:
        with open(fixed_name) as html_file:
            soup = BeautifulSoup(html_file, 'html.parser')
    except:
        print(f"El archivo {file} no puede ser leído.")
        continue

    file_categ_ind = report_categ_ind(soup)
    file_categ = report_catgs[file_categ_ind]
    well_info = info_parser(soup, 0)

    vols_info = info_parser(soup, 1)

    values_dct = vol_summary_extr(soup, file_categ_ind)
    values_df_dict = vib_val_df(values_dct)
    raw_df = final_merger_df(well_info, vols_info, values_df_dict)

    df_modifier(raw_df, file_categ, file)
   
    reports_dic[file_categ] = pd.concat([reports_dic[file_categ],raw_df], ignore_index=True)
    print(f'¡El archivo {file} se ha analizado exitosamente!')

pd.set_option("display.max_columns", 40)
pd.set_option("display.max_rows", 200)

os.makedirs(f'{folder_path}/output', exist_ok=True)

for df_key, df_value in reports_dic.items():
    if len(df_value.columns) == 0:
        continue

    # Generates a modified dataframe and calculates values for it.
    temp_df = df_adapter(df_value)
    # Use it to show on the graphic user interface
    sum_gui_df = sum_data_filter(temp_df)
    print(sum_gui_df)
    # Final list with rows which overcame operating limits.
    surpassed_limits_list = surpass_op_lim(sum_gui_df)
    print(surpassed_limits_list)
    # Exports to excel files from either raw and calculated sum dataframes. 
    export_xls(df_value, f'{df_key} - final', folder_path)
    export_xls(sum_gui_df.reset_index(), f'{df_key} - accumulated', folder_path)
    
    # Tools available
    tools = available_tools(temp_df)
    print(tools)