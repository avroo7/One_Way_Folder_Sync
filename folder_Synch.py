## Folder Synch, with reduced logging ##

# For better performance, this version has reduced logging, in case of Synch folder being empty, the log will show :
    # Source_Folder - Fully Copied
# instead of logging every file/folder individually

# Equally when syncing individual files, the logs will not differentiate between a new file being copied and 
# an existing file being overwritten with a current version. Example :
    # Synch_folder/Sub_folder/file.txt -  Created/Modified

import os
import shutil
import filecmp
import time, datetime
import argparse
    


# Function to log the operation into a file and print to console
def log_to_file_print_to_console (log_file_path, log_data):
    with open(log_file_path, 'a+') as log_file:
        log_file.write(log_data)
        log_file.write('\n')
    print (log_data) 
    

#Synchronisation function.
def synchronise_folder (source, synch, log):
    
    # Check if Source folder exists, gets list of items 
    try:
        source_list = os.listdir(source) 
    except FileNotFoundError:
        # Give error if it does not exist
        print('Source folder does not exist') 
        return
    
    # Creates an empty Synch folder, does not overwrite existing 
    os.makedirs(synch, exist_ok=True) 
    
    # Get list of items in Synch folder
    synch_list = os.listdir(synch) 
    
    # If Synch folder empty and Source is not empty, copy everything from Source
    if not synch_list and source_list: 
        shutil.copytree(source, synch,dirs_exist_ok=True)
        
        # Logs the copying of a Source folder
        log_to_file_print_to_console(log, source + ' - Copied' )

        
    else:
############################# Compare and synch files ############################# 
        
        # Filter list of items to only files
        synch_files = [f for f in synch_list if os.path.isfile(os.path.join(synch, f))] 
        source_files = [f for f in source_list if os.path.isfile(os.path.join(source, f))]
        
        # Loop through Synch files and compare with files in Source
        for synch_item in synch_files:
            synch_full_path=os.path.join(synch, synch_item)
            
            # If files with same name in Source and Synch, checksum
            if (synch_item in source_files):
                source_full_path=os.path.join(source, synch_item)
                
                # If checksum is the same, then remove file name from Source list
                if filecmp.cmp(source_full_path, synch_full_path, shallow=False):
                    source_files.remove(synch_item)
                    
                    
            # If file in Synch and not in Source, remove file
            else:
                log_to_file_print_to_console(log,synch_full_path + ' - Removed')
                os.remove(synch_full_path)
                
        #Loop through remaining Source files and copy/replace them to/in Synch
        for source_item in source_files:
            source_full_path=os.path.join(source, source_item)
            synch_full_path=os.path.join(synch, source_item)
            
            #Logs creation of a Source file
            log_to_file_print_to_console(log,synch_full_path + ' - Created/Modified')
            shutil.copy2(source_full_path,synch_full_path)

#############################  Compare and re-call functions for folders ############################# 
        
        # Filter list of items to only folders
        synch_folders = [d for d in synch_list  if os.path.isdir(os.path.join(synch, d))]
        source_folders = [d for d in source_list  if os.path.isdir(os.path.join(source, d))]
        
        # Loop through Synch folders
        for synch_folder_item in synch_folders:
            
            #If folder in Synch and not Source remove it
            if not (synch_folder_item in source_folders):
                synch_folder_full_path=os.path.join(synch,synch_folder_item)
                
                #Logs removal of folder present only in Synch
                log_to_file_print_to_console(log,synch_folder_full_path + ' - Removed')
                shutil.rmtree(os.path.join(synch,synch_folder_item))
                
        #Loop through list of folders in Source, and call synchronise_folder (itself), to synchronise files/folders
        for source_folder_item in source_folders:
            synchronise_folder(os.path.join(source,source_folder_item),os.path.join(synch,source_folder_item), log)



#Parser to get better input control, and prevent unintended arguments
parser = argparse.ArgumentParser(description='A script to periodically perform one-way synchronisation between Source, and Synch Folders, logs operations to log.txt.')

#Two required arguments, path to Source, and path to Synch
parser.add_argument('-s', '--source', type=str, required=True, help='Source Folder')
parser.add_argument('-d', '--destination', type=str, required=True, help='Destination/Synch folder')

#Two optional arguments with default values, path to log file, and periodicity of synchronisation
parser.add_argument('-l', '--log', type=str, default=os.getcwd(), help='Log folder (default: Current folder)')
parser.add_argument('-t', '--periodicity', type=float, default=1.0, help='Periodicity of Synchronisation in minutes (default: 1.0 min)')


#Inside a try to prevent unintended arguments, outputs the help when arguments missing
try:
    args = parser.parse_args()
    source_path=args.source
    synch_path=args.destination
    
    #Log path inside an if-statement in case of path to existing file 
    if os.path.isfile(args.log):
        log_path=args.log
        
    #path to folder where to create a log.txt
    elif os.path.isdir(args.log):
        log_path=os.path.join(args.log,'log.txt')
        
    #and in case of invalid folder/file, to use current folder and log.txt
    else:
        log_path='log.txt'
        print ("Invalid/non-existing folder/file introduced, logs will be saved to current directory, %s." %(os.path.join(os.getcwd(),log_path)))
    
    #To achieve periodicity, sleep was used, in order avoid using non-standard python libraries that require extra installation
    sleep_timer=args.periodicity*60
    while True:
        
        #Time of each Synch is also logged
        data=str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        log_to_file_print_to_console(log_path, data)
        synchronise_folder(source_path,synch_path,log_path)
        
        #Program never end on its own, but can be manually stopped with Keyboard Interrupt
        time.sleep(sleep_timer)

except SystemExit:
    parser.print_help()



