import os
import shutil
import tarfile


def folderDeletion(path):

    list_dir = os.listdir(path)

    for filename in list_dir:
        file_path = os.path.join(path, filename)

        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)

        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)

    os.rmdir(path)


def extract(tempdir, troubleshootFiles, index, fileStatus):

    folderKeyValues = ['SUMMARY', 'Raw_data_dumps', 'Raw_data_files']
    counter = 0
    movingForward = False
    newName = ''

    newName = troubleshootFiles[index].replace('.tar.gz','')

    existance = os.path.isdir(tempdir + '/' + newName)

    if existance is False:
        os.chdir(os.path.join(tempdir))

        try:
            file = tarfile.open(troubleshootFiles[index])   
            file.extractall(os.path.join(tempdir))

            for i in folderKeyValues:
                arr = os.listdir(os.path.join(tempdir + '/' + 'diagnose'))
                if i in arr:
                    counter += 1

            if counter == 3:
                os.chdir(os.path.join(tempdir))

                os.rename('diagnose', newName)
                file.close()

                os.chdir(tempdir)

                if fileStatus == 's':
                    print('\nFile *** ' + troubleshootFiles[index] + ' *** uploaded successfully\n')
                movingForward = True
                return newName, movingForward

            elif counter != 3:
                os.rename('diagnose', newName)

                if len(troubleshootFiles) == 1:
                    print('\nSelected file (' + newName + ".tar.gz" + ') is not appropriate for troubleshoot diagnostics\n')
                    folderDeletion(newName)
                    tmpnewName = ''

                os.remove(newName + ".tar.gz")
                newName = tmpnewName

                return newName, movingForward

        except:
            if len(troubleshootFiles) == 1:
                print('\nSelected file (' + newName + ".tar.gz" + ') can not be opened\n')
                tmpnewName = ''

            os.remove(newName + ".tar.gz")
            newName = tmpnewName

            return newName, movingForward

    else: 

        arr = os.listdir(os.path.join(tempdir + '/' + newName))
        for i in folderKeyValues:
            if i in arr:
                counter += 1

        if counter == 3:
            movingForward = True
            return newName, movingForward

        elif counter != 3:

            if len(troubleshootFiles) == 1:
                print('\nSelected file (' + newName + ".tar.gz" + ') is not appropriate for troubleshoot diagnostics\n')

            os.remove(newName + ".tar.gz")
            folderDeletion(newName)
            newName = ''

            return newName, movingForward