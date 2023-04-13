from pathlib import Path
import pandas as pd
import re
import os #for renaming files
from enum import Enum
import re

class ReplacementType(Enum):
    SEARCH_PATTERN_CASE_SENSITIVE = 1
    SEARCH_SENTENCE = 2

class RenamingType(Enum):
    RENAME_CODE = 1
    RENAME_DB = 2

class RenamingCodeType(Enum):
    RENAME_FILES_NAMES = 1
    RENAME_FILES_CONTENT= 2


def add_line_at_the_beginning_of_every_function(fileFullPath):
    functions = []
    f = open(fileFullPath)
    for line in f:
        match = re.search(r'([\w]+)\s+([\S]+)\(([\w+\s+\w+])+\)', line)
        if line.find("\\fn") < 0:
            if match:
                returntype = match.group(1)
                funcname = match.group(2)
                print('/********************************************************************')
                print("  \\fn " + match.group())
                print('')
                print('  \\brief')
                print('    Function description for ' + funcname)
                print('')
                if len(match.groups()) > 2:
                    params = []
                    count = len(match.groups()) - 2
                    while count > 0:
                        matchingstring = match.group(count + 2)
                        if matchingstring.find("void") < 0:
                            params.append(matchingstring)
                        count -= 1
                    for parameter in params:
                        print("  \\param " + parameter)
                        print('    Description of ' + parameter)
                        print('')
                print('  \\return')
                print('    ' + returntype)
                print('********************************************************************/')
                print('')



    # # Safely read the input fileFullPath using 'with'
    # #enc = 'utf-8'
    # enc = 'iso-8859-15'
    # with open(fileFullPath, 'r', encoding=enc) as f:
    #     full_file_content = f.read()
    #     if old_string not in full_file_content:
    #         #print('"{old_string}" not found in {fileFullPath}.'.format(**locals()))
    #         return
    # #time.sleep(1)
    #
    # # Safely write the changed content, if found in the file
    # with open(fileFullPath, 'w', encoding=enc) as f:
    #     pattern = "(^.*\(.*\).*\n{)\n(.*)"
    #     pat = re.compile(pattern)
    #     new_file_content = pat.sub(new_string, full_file_content)
    #     f.write(new_file_content)

def unclassify_data(code_folder, file_extension):
    files = [str(path) for path in Path(code_folder).rglob('*.' + file_extension)]
    for fileFullPath in files:
        add_line_at_the_beginning_of_every_function(fileFullPath)

def rename_files(folder_path, excel_file_path, excel_sheet_name):
    excel_data = pd.read_excel(excel_file_path, sheet_name=excel_sheet_name)
    old_files_names = excel_data[old_strings_column_header].tolist()
    new_files_names = excel_data[new_strings_column_header].tolist()
    numOfFiles = len(old_files_names)
    if (numOfFiles > 0):
        print('Renaming files')
    for i in range(0, numOfFiles):
        current_old_relative_file_path = old_files_names[i]
        current_new_relative_file_path = new_files_names[i]
        current_old_full_path = os.path.join(folder_path, current_old_relative_file_path)
        current_new_full_path = os.path.join(folder_path, current_new_relative_file_path)
        os.rename(current_old_full_path, current_new_full_path)
    if (numOfFiles > 0):
        print('Finished renaming files')


if __name__ == "__main__":
    rename_type = RenamingType.RENAME_DB
    excel_file_path = r'renaming.xlsx'
    old_strings_column_header = 'old'
    new_strings_column_header = 'new'
    rename_code_type = RenamingCodeType.RENAME_FILES_CONTENT

    code_folder = r'CODE_FOLDER'
    files_extensions = ['cpp']
    for file_extension in files_extensions:
        unclassify_data(code_folder, file_extension)

