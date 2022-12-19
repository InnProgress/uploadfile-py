import os
import sys
import time
import os.path

import shutil
from werkzeug.utils import secure_filename
import extractFile
import inspectStats
from tempfile import TemporaryDirectory

fileList = []
extractList = []

passed_arguments_number = len(sys.argv)
passed_argument_for_file = []

ALLOWED_EXTENSIONS = '.tar.gz'
UPLOAD_FOLDER = r"D:\Users\Arnas\Desktop\script\upload_files"
path_of_file = r"D:\Users\Arnas\Desktop\script"


def write_file(passed_argument, newName, dict, statContent, statContentText, pstore_text, list_of_results_pstore):
    filename = newName+'-log.txt'
    filepath = os.path.join(UPLOAD_FOLDER, newName, filename)

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
    f.write(f"\n{statContentText}")
    if statContent:
        f.write("\n------------------------------------\n")
        for x in statContent:
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
    print(f"{statContentText}")
    if statContent:
        print("------------------------------------")
        for x in statContent:
            print(f"{x}")

    print("\n\nPstore files:")
    print(f'{pstore_text}')
    if list_of_results_pstore:
        print("------------------------------------")
        for x in list_of_results_pstore:
            print(f"{x}")
    print('\n')


def upload_file():

    if passed_arguments_number > 1:

        passed_argument = ''
    
        for i in range(1, passed_arguments_number):
            passed_argument += sys.argv[i]
            passed_argument_for_file.append(passed_argument + '.')
            passed_argument_for_file.append(passed_argument + ' ')
            passed_argument += ' '

        if os.path.isfile(passed_argument):
            file = passed_argument

        if fileList:
            fileList.clear()

        if extractList:
            extractList.clear()


        if ALLOWED_EXTENSIONS in file:
            filename = secure_filename(file)
            target = os.path.join(path_of_file, filename)
            shutil.copy(target, UPLOAD_FOLDER)

            if filename not in fileList:
                fileList.append(filename)
            
            fileStatus = 's'
            newName, movingForward = extractFile.extract(UPLOAD_FOLDER, fileList, fileList.index(filename), fileStatus)
            extractList.append(newName)

            if movingForward:

                dict, ramKB, cpuLoad, content = inspectStats.inspectSummary(UPLOAD_FOLDER, newName)
                statContent, statContentText = inspectStats.inspectHangedProcesses(UPLOAD_FOLDER, newName)
                pstore_text, list_of_results_pstore = inspectStats.pstore(UPLOAD_FOLDER, newName)

                write_file(file, newName, dict, statContent, statContentText, pstore_text, list_of_results_pstore)
                
              
        else:
            print('Allowed file format is .tar.gz')

    else:
        print("\nNo arguments were passed.\n")


if __name__ == "__main__":
    upload_file()
