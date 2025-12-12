"""
-------------
nspec_sync.py
-------------

This script initiates the file sync specifically for the nSpec tool.

First, it finds which database files are unique between the
tool's local hard drive and the LAN folder. The file paths are saved to
a location on the LAN drive. Subsequent data pipelining will use this info
to only parse new database files copied over.

Then, the script performs the file sync between the local and LAN drives.
"""

from fsu import folsync as fs
from fsu import compdir as cd

# First we will find the unique database files in each directory.
# We will then know which database files are entirely new in the sync.
# This info will be used for data pipelining.
dir_a = "D:\\Scans"
dir_b = "\\\\cam-vpnap-nas1\\nSpec\\Scans"
file_ext = ".db"
log_path = "\\\\cam-vpnap-nas1\\nSpec\\File Sync Utility\\Unique Databases"
comp_inst = cd.CompareDir(file_ext, dir_a, dir_b, log_path)
comp_inst.compare_files(verbose=False)

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
sync_inst = fs.FolderSync(folderpaths, log_path, True)
sync_inst.perform_sync()