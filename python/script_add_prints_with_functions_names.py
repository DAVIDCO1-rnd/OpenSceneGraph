from pathlib import Path
import re
import os



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
    new_include_to_add = '#include "print_function_name.h"'
    pattern_1 = '^.*,[\s]+.*\)[\s]+{'
    pattern_2 = '^.+[ \r]+.+[:]?[:]?.+\(.*\)[\s]*{'
    pattern_3 = '.*[\s]*const[\s]*{'
    pattern = pattern_1 + '|' + pattern_2 + '|' + pattern_3
    # matches_list = re.findall(pattern, full_file_content, re.MULTILINE)
    new_full_file_content = re.sub(pattern, replace, full_file_content, flags=re.MULTILINE)
    new_full_file_content = new_include_to_add + '\n\n' + new_full_file_content
    return new_full_file_content

def add_line_at_the_beginning_of_every_function(fileFullPath):
    enc = 'iso-8859-15'
    with open(fileFullPath, 'r', encoding=enc) as f:
        full_file_content = f.read()
        new_full_file_content = change_file_content(full_file_content)
    with open(fileFullPath, 'w', encoding=enc) as f:
        f.write(new_full_file_content)

def add_print_statements_to_files(subfolder_index, num_of_subfolders, code_folder, file_extension):
    files = [str(path) for path in Path(code_folder).rglob('*.' + file_extension)]
    num_of_files = len(files)
    for file_index, fileFullPath in enumerate(files):
        print(f'subfolder {subfolder_index + 1} out of {num_of_subfolders}: file {file_index + 1} out of {num_of_files}. file name: {fileFullPath}')
        add_line_at_the_beginning_of_every_function(fileFullPath)

if __name__ == "__main__":
    main_src_folder = r'../src'
    subfolders = [f.path for f in os.scandir(main_src_folder) if f.is_dir()]
    #code_folder = r'CODE_FOLDER'
    files_extensions = ['cpp']
    num_of_subfolders = len(subfolders)
    for subfolder_index, single_subfolder in enumerate(subfolders):
        for file_extension in files_extensions:
            add_print_statements_to_files(subfolder_index, num_of_subfolders, single_subfolder, file_extension)
            print()
        print()

