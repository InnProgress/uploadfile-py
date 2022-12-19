import os
import shutil
import tarfile

THRESHOLD_ENTRIES = 10000
THRESHOLD_SIZE = 1000000000
THRESHOLD_RATIO = 10
totalSizeArchive = 0;
totalEntryArchive = 0;

FOLDER_KEY_COUNT = 3
FILE_STATUS_SYMBOL = 's'
FOLDER_KEY_VALUES = ['SUMMARY', 'Raw_data_dumps', 'Raw_data_files']
MESSAGE_CONSTANT = '\nSelected file ('
FILE_FORMAT = '.tar.gz'


# funkcija direktoriju trynimui
def folder_deletion(path):
    listDir = os.listdir(path)
    for filename in listDir:
        filePath = os.path.join(path, filename)
        if os.path.isfile(filePath) or os.path.islink(filePath):
            os.unlink(filePath)
        elif os.path.isdir(filePath):
            shutil.rmtree(filePath)
    os.rmdir(path)


# funkcija .tar.gz failo dydziui patikrinti
def check_tar_file_safe(filename, totalSizeArchive, totalEntryArchive):
    tfile = tarfile.open(filename)
    for entry in tfile:
        tarinfo = tfile.extractfile(entry)
        totalEntryArchive += 1
        sizeEntry = 0
        result = b''
        while True:
            sizeEntry += 1024
            totalSizeArchive += 1024
            print(entry.size)
            ratio = sizeEntry / entry.size
            if ratio > THRESHOLD_RATIO:
                # ratio between compressed and uncompressed data is highly suspicious, looks like a Zip Bomb Attack
                break
            chunk = tarinfo.read(1024)
            if not chunk:
                break
            result += chunk
        if totalEntryArchive > THRESHOLD_ENTRIES:
            # too much entries in this archive, can lead to inodes exhaustion of the system
            break
        if totalSizeArchive > THRESHOLD_SIZE:
            # the uncompressed data size is too much for the application resource capacity
            break
    tfile.close()


# funkcija .tar.gz failu ikelimui
def troubleshoot_file_extraction(tempdir, troubleshoot_files, index, file_status):
    extract_element_counter = 0
    moving_forward = False
    new_name = ''
    new_name = troubleshoot_files[index].replace(FILE_FORMAT,'')
    check_tar_file_safe(troubleshoot_files[index], totalSizeArchive, totalEntryArchive)
    file = tarfile.open(troubleshoot_files[index])   
    file.extractall(os.path.join(tempdir))

    for i in FOLDER_KEY_VALUES:
        arr = os.listdir(os.path.join(tempdir + '/' + 'diagnose'))
        if i in arr:
            extract_element_counter += 1

    os.rename('diagnose', new_name)

    if extract_element_counter == FOLDER_KEY_COUNT:
        os.chdir(os.path.join(tempdir))
        file.close()
        os.chdir(tempdir)
        if file_status == FILE_STATUS_SYMBOL:
            print(f"\nFile ***  {troubleshoot_files[index]} *** uploaded successfully\n")
        moving_forward = True
    
    elif extract_element_counter != FOLDER_KEY_COUNT:
        new_name, moving_forward = bad_file(new_name, troubleshoot_files, moving_forward)

    return new_name, moving_forward


# funkcija patiktrinti failo struktura
def bad_file(new_name, troubleshoot_files, moving_forward):
    if len(troubleshoot_files) == 1:
        print(f"{MESSAGE_CONSTANT} {new_name}{FILE_FORMAT}) is not appropriate for troubleshoot diagnostics\n")
    os.remove(new_name + FILE_FORMAT)
    folder_deletion(new_name)
    new_name = ''
    return new_name, moving_forward


# funkcija .tar.gz failu extractinimui ir pervadinimui
def check_troubleshoot_file_existence(tempdir, troubleshoot_files, index, file_status):
    extract_element_counter = 0
    new_name = ''
    new_name = troubleshoot_files[index].replace(FILE_FORMAT,'')

    if (os.path.isdir(tempdir + '/' + new_name)) is False:
        os.chdir(os.path.join(tempdir))

        try:
             new_name, moving_forward = troubleshoot_file_extraction(tempdir, troubleshoot_files, index, file_status)
        except:
            if len(troubleshoot_files) == 1:
                print(f"{MESSAGE_CONSTANT} {new_name}{FILE_FORMAT}) can not be opened\n")
                quit()
            os.remove(new_name + FILE_FORMAT)
            new_name = ''
            
    else: 
        arr = os.listdir(os.path.join(tempdir + '/' + new_name))
        for i in FOLDER_KEY_VALUES:
            if i in arr:
                extract_element_counter += 1

        if extract_element_counter == FOLDER_KEY_COUNT:
            moving_forward = True

        elif extract_element_counter != FOLDER_KEY_COUNT:
            new_name, moving_forward = bad_file(new_name, troubleshoot_files, moving_forward)

    return new_name, moving_forward