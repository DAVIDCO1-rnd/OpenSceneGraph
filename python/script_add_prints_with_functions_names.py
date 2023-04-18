from pathlib import Path
import re
import os

def get_files_list(file_path):
    with open(file_path) as file:
        files_list = [line.rstrip() for line in file]
    files_list = list(single_file for single_file in files_list if single_file)  # Non-blank lines
    return files_list



def check_if_word_in_string(words_to_search, potential_function_declaration):
    for single_word in words_to_search:
        single_pattern = r'\b' + single_word + r'\b'
        match = re.search(single_pattern, potential_function_declaration)
        if match:
            return True
    return False

def check_if_function_declaration(potential_function_declaration):
    words_to_search = ['if', 'while', 'for', 'struct', 'switch', 'case']
    is_word_in_string = check_if_word_in_string(words_to_search, potential_function_declaration)
    if is_word_in_string == True:
        return False
    if potential_function_declaration.find("||") != -1:
        return False
    if potential_function_declaration.find("#define") != -1:
        return False
    pattern_that_starts_with_plus = '^[\s]*[\+]'
    match = re.search(pattern_that_starts_with_plus, potential_function_declaration)
    if match:
        return False
    return True

def replace(single_match):
    potential_function_declaration = single_match.group(0)
    is_function_declaration = check_if_function_declaration(potential_function_declaration)
    if is_function_declaration:
        new_text = potential_function_declaration + 'PRINT_FUNCTION_NAME' + '\n'
        return new_text
    else:
        return potential_function_declaration

def change_file_content(full_file_content):
    include_line_to_add = '#include "print_function_name.h"'
    entry_counter_static_initialization = 'static int entry_counter = 0;'
    pattern_1 = '^.*,[\s]+.*\)[\s]+{'
    pattern_2 = '^.+[ \r]+.+[:]?[:]?.+\(.*\)[\s]*{'
    pattern_3 = '.*[\s]*const[\s]*{'
    pattern = pattern_1 + '|' + pattern_2 + '|' + pattern_3
    # matches_list = re.findall(pattern, full_file_content, re.MULTILINE)
    new_full_file_content = re.sub(pattern, replace, full_file_content, flags=re.MULTILINE)
    new_full_file_content = include_line_to_add + \
                            '\n' + \
                            entry_counter_static_initialization + \
                            '\n\n' + \
                            new_full_file_content
    return new_full_file_content

def add_line_at_the_beginning_of_every_function(fileFullPath):
    enc = 'iso-8859-15'
    with open(fileFullPath, 'r', encoding=enc) as f:
        full_file_content = f.read()
        new_full_file_content = change_file_content(full_file_content)
    with open(fileFullPath, 'w', encoding=enc) as f:
        f.write(new_full_file_content)

# def add_print_statements_to_files(subfolder_index, num_of_subfolders, code_folder_path, file_extension):
#     last_folder_name = os.path.basename(os.path.normpath(code_folder_path))
#     if last_folder_name == 'osgWrappers':
#         subfolders = [f.path for f in os.scandir(code_folder_path) if f.is_dir() and f.name != 'serializers']
#         files = []
#         for single_subfolder in subfolders:
#             files_of_single_subfolder = [str(path) for path in Path(single_subfolder).rglob('*.' + file_extension)]
#             files = files + files_of_single_subfolder
#     else:
#         files = [str(path) for path in Path(code_folder_path).rglob('*.' + file_extension)]
#     num_of_files = len(files)
#     for file_index, fileFullPath in enumerate(files):
#         print(f'subfolder {subfolder_index + 1} out of {num_of_subfolders}: file {file_index + 1} out of {num_of_files}. file name: {fileFullPath}')
#         add_line_at_the_beginning_of_every_function(fileFullPath)

if __name__ == "__main__":
    main_src_folder = r'../src'
    subfolders_names = [f.name for f in os.scandir(main_src_folder) if f.is_dir()]
    #code_folder = r'CODE_FOLDER'
    num_of_subfolders = len(subfolders_names)
    for subfolder_index, single_subfolder_name in enumerate(subfolders_names):
        if single_subfolder_name == 'osgPlugins' or single_subfolder_name == 'osgWrappers':
            continue
        sub_folder_info_file = os.path.join('osg_cpp_folders', single_subfolder_name, 'files_list.txt')
        files_list = get_files_list(sub_folder_info_file)
        num_of_files = len(files_list)
        for file_index, file_name in enumerate(files_list):
            fileFullPath = os.path.join(main_src_folder, single_subfolder_name, file_name)
            print(f'subfolder {subfolder_index + 1} out of {num_of_subfolders}: file {file_index + 1} out of {num_of_files}. file name: {fileFullPath}')
            add_line_at_the_beginning_of_every_function(fileFullPath)
        print()
        print()

