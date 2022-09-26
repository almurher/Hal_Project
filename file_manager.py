import os

def folder_opener():

    user_folder = input("Por favor agregue la ruta de su carpeta de trabajo: ")
    # user_folder = "c:/Users/Aldairo/hal_project/data"
    
    os.chdir(user_folder)
    dir_list = os.listdir()
    return allow_format(dir_list)

def allow_format(directory_list):

    # Checks if the file format is one of the allowed ones and avoids duplicated files
    # with different formats. Also ignores folders
    allowed_formats = ['xls', 'html', 'txt', 'xlsx']
    final_list = []
    unique_file_list = []

    for file in directory_list:
        dot_index = None
        
        for i in range(len(file)):
            if file[i] == ".":
                dot_index = i

        if dot_index is None:
            continue

        file_name = file[:dot_index]
        file_format = file[dot_index + 1:]
        
        if file_name not in unique_file_list and file_format in allowed_formats:
            unique_file_list.append(file_name)
            final_list.append(file)

    return final_list

