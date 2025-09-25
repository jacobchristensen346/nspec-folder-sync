import subprocess
import os
import time
from datetime import datetime

""" 
This script is used to initiate synchronization between the nSpec tool local hard drive and LAN archive folder
Any new/modified files in the local hard drive will be copied to the LAN folder
The sync is one-way only, meaning any changes made directly to the LAN folder will not be reflected in the local hard drive
This allows the LAN folder to contain all data ever recorded by the nSpec tool, even when the local hard drive is purged

"""

start = time.perf_counter()

output_file = open("\\\\cam-vpnap-nas1\\nSpec\\File Sync Utility\\Log Files\\placeholder.txt", "w") # create text file to capture output

# list of all source and destination paths to perform copying
list_of_dir = [["D:\\Alignments\\", "\\\\cam-vpnap-nas1\\nSpec\\Alignments\\"], 
	["D:\\Layouts\\", "\\\\cam-vpnap-nas1\\nSpec\\Layouts\\"],
	["D:\\Scans\\", "\\\\cam-vpnap-nas1\\nSpec\\Scans\\"],
	["D:\\Templates\\", "\\\\cam-vpnap-nas1\\nSpec\\Templates\\"],
	["D:\\Scripts\\", "\\\\cam-vpnap-nas1\\nSpec\\Scripts\\"],
	["D:\\Masks\\", "\\\\cam-vpnap-nas1\\nSpec\\Masks\\"]]

# iterate through each source and destination
for dir in list_of_dir:

	print("CURRENT SOURCE: " + dir[0])
	print("CURRENT DESTINATION: " + dir[1])

	process = subprocess.Popen(["xcopy", dir[0], dir[1], "/f", "/e", "/d", "/c", "/y"], 
		stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell = True, text = True)

	output_file.write("CURRENT SOURCE: " + dir[0] + "\n") # list current source and destination in log file
	output_file.write("CURRENT DESTINATION: " + dir[1] + "\n")

	# stream output in real-time
	for line in process.stdout:
    		print(line, end="")
    		output_file.write(line) # write each line to text file
	
	output_file.write("\n")
	print("\n")

end = time.perf_counter()

print(f"Elapsed time: {end - start:.6f} seconds")
output_file.write(f"Elapsed time: {end - start:.6f} seconds\n")

current_datetime = ((datetime.now()).strftime("%Y-%m-%d %H:%M:%S")) # get the date and time when sync was performed
rename_datetime = ((datetime.now()).strftime("%Y-%m-%d %H-%M-%S")).replace(" ", "_")
output_file.write("Sync finished --> " + current_datetime + "\n")

# rename text file to current date and time
output_file.close()
os.replace("\\\\cam-vpnap-nas1\\nSpec\\File Sync Utility\\Log Files\\placeholder.txt", "\\\\cam-vpnap-nas1\\nSpec\\File Sync Utility\\Log Files\\" + str(rename_datetime) + ".txt")

print('Results log saved to \\\\cam-vpnap-nas1\\nSpec\\File Sync Utility\\Log Files\\' + str(rename_datetime) + '.txt')

input('Press Enter to exit...')
