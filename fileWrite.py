import sys
import time
import os.path
from datetime import datetime

passed_argument = ''
passed_arguments_number = len(sys.argv)
current_directory_list = os.listdir()
passed_argument_for_file = []
now = datetime.now()

def write_file(passed_argument):
    f.write(f"\nFile name: {passed_argument}")
    f.write(f"\nFile path: {os.path.abspath(passed_argument)}")
    f.write(f"\nFile size: {os.path.getsize(passed_argument)}")
    f.write(f"\nFile creation date: {time.ctime(os.path.getctime(passed_argument))}")


if passed_arguments_number > 1:
    
    f = open("log.txt", 'a')

    for i in range(1, passed_arguments_number):
        passed_argument += sys.argv[i]
        passed_argument_for_file.append(passed_argument + '.')
        passed_argument_for_file.append(passed_argument + ' ')
        passed_argument += ' '

    file = passed_argument

    print(f"\nPassed file name: {file}")

    if os.path.isfile(file):
        write_file(file)

else:
    print("\nNo arguments were passed.\n")