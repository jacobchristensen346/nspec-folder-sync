"""
--------------
folder_sync.py
--------------

This module is used to initiate synchronization between two separate folders.
It uses the Windows 'xcopy' command to perform the sync, so the module
must be used in a Windows environment to work properly.

Initially, it was coded specifically to perform file sync between the nSpec 
tool local hard drive and the nSpec shared LAN archive folder.
This version has been generalized and can receive user arguments.
If ran as a script, the default behavior is to perform the nSpec folder
synchronization. Arguments can be passed if imported as a module.

Users provide a list of paired directories representing source and destination
folders. Any new/modified files in the source folders will be copied to the 
corresponding destination folders.

The sync is one-way only, meaning any changes made directly to the destination
folder will not be reflected in the local hard drive.
This allows the destination folder to contain all data ever recorded,
even when the source folder has been purged.
"""

import subprocess
import os
import time
from datetime import datetime


class FolderSync:
    
    def __init__(self, folderpaths, log_path, skip_verify=False):
        """Initialize the filepaths variables.
        
        Args:
            filepaths (list): List of paired folderpaths. Expects an input
                in the form of '[..., [[src, dest]], ...]', where each
                'src' and 'dest' are the source and destination folder
                paths, respectively, and are strings.
            log_path (str): Represents the folder to save a log file into
                recording all files which were synced.
            skip_verify (bool, optional): If set to to True, the program
                will not ask for user verification via keyboard input
                before the filesync is initiated. The default is False.

        Returns:
            None.
        """
        self.list_of_dir = folderpaths
        self.log_path = log_path
        self.skip_verify = skip_verify
        
    def perform_sync(self):
        """Performs the file sync between the source and destination folders.

        Returns:
            None.
        """
        
        if not self.skip_verify:
            print("Please review the source and destination folders...\n")
            for idx, dir in enumerate(self.list_of_dir):
                print("SOURCE " + str(idx + 1) + ": " + dir[0])
                print("DESTINATION " + str(idx + 1) + ": " + dir[1])
            usrcon = input("\nType 'Yes' and press Enter "
                           + "to confirm initiation of folder sync: ")
            if usrcon == "Yes":
                print("\nProceeding with the folder sync...\n")
            else:
                print("\nAborting the folder sync!")
                return
            
        start = time.perf_counter()  # Track total time elapsed
        
        # Create a text file to capture log output.
        output_file = open(self.log_path + "placeholder.txt", "w")
        
        # Iterate through each source and destination.
        for dir in self.list_of_dir:
        
        	print("CURRENT SOURCE: " + dir[0])
        	print("CURRENT DESTINATION: " + dir[1])
        
            # Create the sync process using the xcopy command.
        	process = subprocess.Popen(
                ["xcopy", dir[0], dir[1], "/f", "/e", "/d", "/c", "/y"], 
        		stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                shell = True, text = True)
        
            # List current source and destination in log file.
        	output_file.write("CURRENT SOURCE: " + dir[0] + "\n")
        	output_file.write("CURRENT DESTINATION: " + dir[1] + "\n")
        
        	# Stream the sync output in real-time.
        	for line in process.stdout:
            		print(line, end="")
            		output_file.write(line) # Write each line to text file
        	
        	output_file.write("\n")
        	print("\n")
        
        end = time.perf_counter()  # Track total time elapsed
        
        print(f"Elapsed time: {end - start:.6f} seconds")
        output_file.write(f"Elapsed time: {end - start:.6f} seconds\n")
        
        # Get the date and time when sync was performed.
        current_datetime = ((datetime.now()).strftime("%Y-%m-%d %H:%M:%S"))
        rename_datetime = current_datetime.replace(" ", "_").replace(":", "-")
        output_file.write("Sync finished --> " + current_datetime + "\n")
        
        # Rename text file to current date and time.
        output_file.close()
        rename_log = self.log_path + str(rename_datetime) + ".txt"
        os.replace(self.log_path + "placeholder.txt", rename_log)
        
        print("Results log saved to " + rename_log)
        
        input("Press Enter to exit...")
        
if __name__ == "__main__":
    # List of all source and destination paths to perform copying.
    # This is specifically for the nSpec local folders -> LAN folders.
    folderpaths = [
        ["D:\\Alignments\\", "\\\\cam-vpnap-nas1\\nSpec\\Alignments\\"], 
    	["D:\\Layouts\\", "\\\\cam-vpnap-nas1\\nSpec\\Layouts\\"],
    	["D:\\Scans\\", "\\\\cam-vpnap-nas1\\nSpec\\Scans\\"],
    	["D:\\Templates\\", "\\\\cam-vpnap-nas1\\nSpec\\Templates\\"],
    	["D:\\Scripts\\", "\\\\cam-vpnap-nas1\\nSpec\\Scripts\\"],
    	["D:\\Masks\\", "\\\\cam-vpnap-nas1\\nSpec\\Masks\\"]]
    # The location for saving the log file.
    log_path = "\\\\cam-vpnap-nas1\\nSpec\\File Sync Utility\\Log Files\\"
    sync_inst = FolderSync(folderpaths, log_path, True)
    sync_inst.perform_sync()