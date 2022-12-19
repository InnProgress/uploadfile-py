import os
import sys
import time
import os.path

import shutil
from werkzeug.utils import secure_filename
import extractFile
import inspectStats
from tempfile import TemporaryDirectory

file_list = []
extract_list = []

passed_arguments_number = len(sys.argv)
passed_argument_for_file = []

ALLOWED_EXTENSIONS = '.tar.gz'
FILE_STATUS_SYMBOL = 's'
UPLOAD_FOLDER = r"D:\Users\Arnas\Desktop\script\upload_files"
path_of_file = r"D:\Users\Arnas\Desktop\script"


def write_file(passed_argument, new_name, dict, stat_content, stat_content_text, pstore_text, list_of_results_pstore):
    filename = new_name+'-log.txt'
    filepath = os.path.join(UPLOAD_FOLDER, new_name, filename)

    if os.path.isfile(filename):
        os.remove(filepath)

    f = open(filename, 'a')
    f.write(f"*************************************************")
    f.write(f"\n*****                                      ******")
    f.write(f"\n*****      Diagnostis file statistics      ******")
    f.write(f"\n*****                                      ******")
    f.write(f"\n*************************************************")

    f.write(f"\n\nFile name: {passed_argument}")

    f.write(f"\n\nSummary: \n")
    for x, y in dict.items():
        f.write(f"* {x} - {y}")

    f.write(f"\nHanged processes: ")
    f.write(f"\n{stat_content_text}")
    if stat_content:
        f.write("\n------------------------------------\n")
        for x in stat_content:
            f.write(f"{x}")

    f.write("\n\nPstore files:")
    f.write(f'\n{pstore_text}')
    if list_of_results_pstore:
        f.write("\n------------------------------------\n")
        for x in list_of_results_pstore:
            f.write(f"{x}")

    print('\n')
    print(f"*************************************************")
    print(f"*****                                      ******")
    print(f"*****      Diagnostis file statistics      ******")
    print(f"*****                                      ******")
    print(f"*************************************************")

    print(f"\nFile name: {passed_argument}")

    print(f"\nSummary: \n")
    for x, y in dict.items():
        print(f"* {x} - {y}")

    print(f"\nHanged processes: ")
    print(f"{stat_content_text}")
    if stat_content:
        print("------------------------------------")
        for x in stat_content:
            print(f"{x}")

    print("\n\nPstore files:")
    print(f'{pstore_text}')
    if list_of_results_pstore:
        print("------------------------------------")
        for x in list_of_results_pstore:
            print(f"{x}")
    print('\n')


def form_argument(var):
    passed_argument = ''
    for i in range(1, len(var)):
        passed_argument += var[i]
        passed_argument += ' '
    return passed_argument


def check_if_file_exists():
    passed_argument = form_argument(sys.argv)
    if os.path.isfile(passed_argument):
        file = passed_argument
        if file_list:
            file_list.clear()
        if extract_list:
            extract_list.clear()
        return file
    else:
        print(f"Passed file does not exist -> {passed_argument}")
        quit()


def upload_file():
    if passed_arguments_number > 1:
        
        file = check_if_file_exists()

        if ALLOWED_EXTENSIONS in file:
            filename = secure_filename(file)
            target = os.path.join(path_of_file, filename)
            shutil.copy(target, UPLOAD_FOLDER)

            if filename not in file_list:
                file_list.append(filename)
            
            new_name, moving_forward = extractFile.check_troubleshoot_file_existence(UPLOAD_FOLDER, file_list, file_list.index(filename), FILE_STATUS_SYMBOL)
            extract_list.append(new_name)

            if moving_forward:
                summary_dict = inspectStats.summary_dictionary(UPLOAD_FOLDER, new_name)
                stat_content, stat_content_text = inspectStats.inspect_hanged_processes(UPLOAD_FOLDER, new_name)
                pstore_text, list_of_results_pstore = inspectStats.pstore(UPLOAD_FOLDER, new_name)
                write_file(file, new_name, summary_dict, stat_content, stat_content_text, pstore_text, list_of_results_pstore)
                
        else:
            print(f"Allowed file format is {ALLOWED_EXTENSIONS}")
    else:
        print("\nNo arguments were passed.\n")


if __name__ == "__main__":
    upload_file()