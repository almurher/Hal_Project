# from bs4 import BeautifulSoup
# import pandas as pd
# install pandas,xlwt, openpyxl
import os
from multiprocessing.util import info
from vib_func import *
from file_manager import *

# Este es el principio pero por mañoso se deja al final. Requiere condicionales
# para verificar que el archivo adecuado entre...

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


    # filt = (raw_df["Measure Type"] == 'Peak Z Bins')
    # print(raw_df.loc[filt])
    # print(raw_df.groupby(['Measure Type', 'Band (G)'])['Bit Run (Mins)', 'Bit Run (count)'].sum())
    # file_name = str(soup.h1)

    df_modifier(raw_df, file_categ)
   
    reports_dic[file_categ] = pd.concat([reports_dic[file_categ],raw_df], ignore_index=True)
    #print(end_df.groupby(['Job Number', 'Vibration Tool', 'M/LWD Tool Size', 'Measure Type', 'Band (G)'])['Bit Run (Mins)'].sum())
    print(f'¡El archivo {file} se ha analizado exitosamente!')
    # pd.set_option("display.max_columns", 40)
    # pd.set_option("display.max_rows", 40)

pd.set_option("display.max_columns", 40)
pd.set_option("display.max_rows", 40)

os.makedirs(f'{folder_path}/output', exist_ok=True)

for k, v in reports_dic.items():
    if len(v.columns) == 0:
        continue
    # print(k)
    # print(v)
    temp_df = v.groupby(['Vibration Tool', 'M/LWD Tool Size', 'Measure Type', 'Band (G)'])['Bit Run (Mins)'].sum().rename('Acumulado').reset_index()
    print(temp_df)
    df_name = f'{k}.xlsx'
    with pd.ExcelWriter(f'{folder_path}/output/{df_name}') as writer:
        temp_df.to_excel(writer, index=False, header=True)