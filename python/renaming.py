from pathlib import Path
import pandas as pd
import re
import os #for renaming files
from enum import Enum

class ReplacementType(Enum):
    SEARCH_PATTERN_CASE_SENSITIVE = 1
    SEARCH_SENTENCE = 2

class RenamingType(Enum):
    RENAME_CODE = 1
    RENAME_DB = 2

class RenamingCodeType(Enum):
    RENAME_FILES_NAMES = 1
    RENAME_FILES_CONTENT= 2


def replace_string(fileFullPath, old_string, new_string, replacement_type):
    # Safely read the input fileFullPath using 'with'
    #enc = 'utf-8'
    enc = 'iso-8859-15'
    with open(fileFullPath, 'r', encoding=enc) as f:
        full_file_content = f.read()
        if old_string not in full_file_content:
            #print('"{old_string}" not found in {fileFullPath}.'.format(**locals()))
            return
    #time.sleep(1)

    # Safely write the changed content, if found in the file
    with open(fileFullPath, 'w', encoding=enc) as f:
        print('Changing "{old_string}" to "{new_string}" in {fileFullPath}'.format(**locals()))
        if replacement_type == ReplacementType.SEARCH_PATTERN_CASE_SENSITIVE:
            pattern = r'\b' + old_string + r'\b';
            pat = re.compile(pattern)
            new_file_content = pat.sub(new_string, full_file_content)
            f.write(new_file_content)
        else:
            ttt = re.escape(old_string)
            new_file_content = re.sub(ttt, new_string, full_file_content, re.M)
            f.write(new_file_content)

def unclassify_data(excel_file_path, excel_sheet_name, folder_to_rename, file_extension, old_strings_column_header, new_strings_column_header):
    files = [str(path) for path in Path(folder_to_rename).rglob('*.' + file_extension)]
    excel_data = pd.read_excel(excel_file_path, sheet_name=excel_sheet_name)
    old_strings = excel_data[old_strings_column_header].tolist()
    new_strings_with_nan = excel_data[new_strings_column_header].tolist()
    new_strings = ['' if pd.isnull(x) else x for x in new_strings_with_nan]
    if excel_sheet_name=="content renaming sentences":
        replacement_type = ReplacementType.SEARCH_SENTENCE
    else:
        replacement_type = ReplacementType.SEARCH_PATTERN_CASE_SENSITIVE
    for fileFullPath in files:
        for i in range(0, len(old_strings)):
            current_old_string = old_strings[i]
            current_new_string = new_strings[i]
            replace_string(fileFullPath, current_old_string, current_new_string, replacement_type)

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

    if rename_type == RenamingType.RENAME_CODE:
        folder_to_rename = r'CODE_FOLDER'
        excel_sheet_names = ['content renaming']
        files_extensions = ['c', 'txt']
        if rename_code_type == RenamingCodeType.RENAME_FILES_NAMES:
            rename_files(folder_to_rename, excel_file_path, 'files renaming')
        elif rename_code_type == RenamingCodeType.RENAME_FILES_CONTENT:
            for excel_sheet_name in excel_sheet_names:
                for files_extension in files_extensions:
                    unclassify_data(excel_file_path, excel_sheet_name, folder_to_rename, files_extension, old_strings_column_header, new_strings_column_header)
    elif rename_type == RenamingType.RENAME_DB:
        folder_to_rename = r'DATA_FOLDER'
        excel_sheet_names = ['content renaming']
        for excel_sheet_name in excel_sheet_names:
            unclassify_data(excel_file_path, excel_sheet_name, folder_to_rename, 'txt',
                            old_strings_column_header, new_strings_column_header)
