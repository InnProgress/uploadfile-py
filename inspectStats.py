import os
from os import listdir
import os

RAW_DATA_DUMPS = '/Raw_data_dumps'
PSTORE = RAW_DATA_DUMPS + '/pstore'

# funkcija summary failo perskaitymui - perskaito ir isaugo eilutes su konkreciomis reiksmemis jose
def read_summary_file(tempdir, new_name):
    os.chdir(os.path.join(tempdir + '/' + new_name))

    open_read = open('SUMMARY', 'r')
    wanted_values = ['BOARD', 'FIRMUX', 'BUILD', 'LOAD', 'RAM', 'print', 'UPTIME']
    summary_file_content = []

    for line in open_read:
        for value in wanted_values:
            if value in line:
                summary_file_content.append(line)     
    return summary_file_content


# funkcija summary failo analizei - isrenka aktualia informacija pagal raktines reiksmes
def summary_dictionary(tempdir, new_name):
    summary_file_content = read_summary_file(tempdir, new_name)
    summary_dict = {}
    
    size = len(summary_file_content)
    for i in range(size):
        partitioned_string = summary_file_content[i].partition('=')
        summary_dict[partitioned_string[0]] = partitioned_string[2]
        if partitioned_string[0] == 'LOAD':
            summary_dict['CPU LOAD'] = summary_dict.pop('LOAD')
    return summary_dict


# funkcija failo turinio informacijai perskiatyti
def get_content(tempdir, new_name):
    os.chdir(os.path.join(tempdir + '/' + new_name))
    with open("SUMMARY", "r") as f:
        content = f.read()
    return content


# funkcija ram ir cpu reiksmem grazinti
def inspect_summary(tempdir, new_name):
    summary_dict = summary_dictionary(tempdir, new_name)
    
    for j in summary_dict:
        if j == 'RAM':
            ram_kb =  summary_dict[j].partition(' ')
        if j == 'CPU LOAD':
            cpu_load = summary_dict[j].split(' ')
    
    return ram_kb, cpu_load


# funkcija uzluzusiu procesu paieskai - isrenka procesus kurie atitinka bloga statusa indikuojancias reiksmes
def inspect_hanged_processes(tempdir, new_name):

    os.chdir(os.path.join(tempdir + '/' + new_name + RAW_DATA_DUMPS))
    if os.path.isfile('ps'):
        open_read = open('ps', 'r')
        stat_content = [] 
        unwanted_states = ['D', 'X', 'T', 'Z', 't']
        common_stat_counter = 0

        for possition, line in enumerate(open_read):
            
            if possition == 0:
                stat = line.split('STAT')[0]
                command = line.split('COMMAND')[0]
                stat_content.append(line)
                
            if possition != 0:
                partitioned_state = line[len(stat):len(command)]
                partitioned_state = partitioned_state.replace(" ", "")
                for i in unwanted_states:
                    if i in partitioned_state:
                        common_stat_counter += 1
                        stat_content.append(line)

        os.chdir(os.path.join(tempdir + '/' + new_name))
        common_stat_counter += 1

        if common_stat_counter == 0:
            stat_contentText = 'No hanged processes detected'
            stat_content.pop(0)
        else:
            stat_contentText = 'Number of detected hanged processes: ' + str(common_stat_counter)
    else:
        os.chdir(os.path.join(tempdir + '/' + new_name))
        stat_contentText = 'ps file is not found'
        common_stat_counter = 0
        stat_content = []
    
    return stat_content, stat_contentText 


# funkcija pstore failo analizei - isrenka sistemos anomalijas pagal raktines reiksmes
def pstore(tempdir, new_name):
    os.chdir(os.path.join(tempdir + '/' + new_name))
    partitioned_state = ['Oops:', 'oom-killer']
    list_of_results= []
    line_number = 0
      
    if len(os.listdir(tempdir + '/' + new_name + PSTORE) ) == 0: 
        pstore_text = 'Pstore folder is empty'
    else:                  
        for filename in listdir(tempdir + '/' + new_name + PSTORE):      
            with open(tempdir + '/' + new_name + PSTORE + '/' + filename, 'r') as readObj: 
                line_number = 0
                for line in readObj:
                    line_number += 1 
                    for i in partitioned_state: 
                        if i in line:
                            list_of_results.append((line_number, line.rstrip()))
                            
                if list_of_results:
                    pstore_text = 'Anomality detected in Pstore file: ' + filename 
                else:
                    pstore_text = 'No craches or OOMs detected'

    return pstore_text, list_of_results