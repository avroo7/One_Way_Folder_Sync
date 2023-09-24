# One_Way_Folder_Sync
Python script that synchronises a Source folder to a Sync folder, and maintains any changes, so that Sync is mirror of Source

# Usage :
python folder_synch.py [-h] -s SOURCE -d DESTINATION [-l LOG] [-t PERIODICITY]

  -h, --help                                             show this help message and exit
  
  -s SOURCE, --source SOURCE                             Source Folder
  
  -d DESTINATION, --destination DESTINATION              Destination/Synch folder
  
  -l LOG, --log LOG                                      Log folder (default: Current folder)
  
  -t PERIODICITY, --periodicity PERIODICITY              Periodicity of Synchronisation in minutes (default:1.0 min)
  
-s SOURCE and -d DESTINATION are required arguments

# Versions
Has two versions, one that is more efficient with synchronisation (folder_synch.py) but has less log output. And one that has more log details, but is less sync efficient (folder_synch_more_logging.py)

# folder_synch.py
For better performance, this version has reduced logging, in case of Synch folder being empty, the log will show :

    - Source_Folder - Fully Copied
instead of logging every file/folder individually.

Equally when syncing individual files, the logs will not differentiate between a new file being copied and an existing file being overwritten with a current version. Example :

    - Synch_folder/Sub_folder/file.txt -  Created/Modified


# folder_synch_more_logging.py
This version will output more info in the console, and give more log data, including logging every file/folder name, when copying to an empty synch folder.
It also differentiates between creating a file that previously did not exist, and overwriting a file with non equal checksum to the original. 
Example :

    - Synch_folder/Sub_folder/file.txt -  Created 
    (This is a new file that previously was not in the Synch folder)
    
    - Synch_folder/Sub_folder/file.txt - Modified 
    (A file with this name was in the Synch folder, but the checksum is different, as such it was modified) 
    
As a consequence this makes the actual synchronisation less efficient.
