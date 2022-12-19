import os
from os import listdir
import os

def readSummaryFile(tempdir, newName):
    os.chdir(os.path.join(tempdir + '/' + newName))

    openRead = open('SUMMARY', 'r')
    wantedValues = ['BOARD', 'FIRMUX', 'BUILD', 'LOAD', 'RAM', 'print', 'UPTIME']
    summaryFileContent = []

    for line in openRead:
        for value in wantedValues:
            if value in line:
                summaryFileContent.append(line)     
    return summaryFileContent

def summaryDictionary(tempDir, newName):
    summaryFileContent = readSummaryFile(tempDir, newName)
    summaryDict = {}
    
    size = len(summaryFileContent)
    for i in range(size):
        partitionedString = summaryFileContent[i].partition('=')
        summaryDict[partitionedString[0]] = partitionedString[2]
        if partitionedString[0] == 'LOAD':
            summaryDict['CPU LOAD'] = summaryDict.pop('LOAD')
    return summaryDict

def getContent(tempDir, newName):
    os.chdir(os.path.join(tempDir + '/' + newName))
    with open("SUMMARY", "r") as f:
        content = f.read()
    return content

def inspectSummary(tempDir, newName):
    summaryDict = summaryDictionary(tempDir, newName)
    
    for j in summaryDict:
        if j == 'RAM':
            ramKB =  summaryDict[j].partition(' ')
        if j == 'CPU LOAD':
            cpuLoad = summaryDict[j].split(' ')
    
    return ramKB, cpuLoad

def inspectHangedProcesses(tempDir, newName):
    os.chdir(os.path.join(tempDir + '/' + newName + '/Raw_data_dumps'))
    if os.path.isfile('ps'):
        openRead = open('ps', 'r')
        statContent = [] 
        unwantedStates = ['D', 'X', 'T', 'Z', 't']
        commonStatCounter = 0

        for possition, line in enumerate(openRead):
            if possition == 0:
                stat = line.split('STAT')[0]
                command = line.split('COMMAND')[0]
                statContent.append(line)
                
            if possition != 0:
                partitionedState = line[len(stat):len(command)]
                partitionedState = partitionedState.replace(" ", "")
                for i in unwantedStates:
                    if i in partitionedState:
                        
                        commonStatCounter += 1
                        statContent.append(line)

        os.chdir(os.path.join(tempDir + '/' + newName))

        commonStatCounter += 1

        if commonStatCounter == 0:
            statContentText='No hanged processes detected'
            statContent.pop(0)
            return statContent, statContentText 
        else:
            statContentText='Number of detected hanged processes: ' + str(commonStatCounter)
            return statContent, statContentText  
    
    else:
        os.chdir(os.path.join(tempDir + '/' + newName))
        statContentText='ps file is not found'
        commonStatCounter = 0
        statContent = []
        return statContent, statContentText 

def pstore(tempDir, newName):
    
    os.chdir(os.path.join(tempDir + '/' + newName))
    searchValues = ['Oops:', 'oom-killer']
    listOfResults = []
    lineNumber = 0
      
    if len(os.listdir(tempDir + '/' + newName + '/Raw_data_dumps/pstore') ) == 0: 
        pstoreText = "Pstore folder is empty"

    else:       
        for filename in listdir(tempDir + '/' + newName + '/Raw_data_dumps/pstore'): 
            with open(tempDir + '/' + newName + '/Raw_data_dumps/pstore' + '/' + filename, 'r') as read_obj: 
                lineNumber = 0
                for line in read_obj:
                    lineNumber += 1 
                    for i in searchValues: 
                        if i in line:
                            listOfResults.append((lineNumber, line.rstrip()))
                            
                if listOfResults:
                    pstoreText = 'Anomality detected in Pstore file: ' + filename 
                else:
                    pstoreText="No craches or OOMs detected"

    return pstoreText, listOfResults