"""
----------
compdir.py
----------

This module provides a class used to probe two directories for a specific
file type, and compare those directories.

The unique files for the specific file type from each directory
are recorded in log files.

Classes:
    CompareDir: Recursively searches two provided directories for specific
        file type, then compares each directory to find unique files from each.
"""
import os

class CompareDir:
    """Compare directories recursively for a specific file type.
    
    Attributes:
        file_ext (str): File extension to search for.
        dir1 (str): First directory to look for files.
        dir2 (str): Second directory to look for files.
        log_path (str): The directory path to save log output.
    """

    def __init__(self, file_ext: str, dir1: str, dir2: str, log_path: str):
        """Initialize instance attributes.

        Returns:
            None.

        """
        self.file_ext = file_ext
        self.dir1 = dir1
        self.dir2 = dir2
        self.log_path = log_path

    def get_files(self, directory: str):
        """Walk through a directory recursively and return paths for files.
        
        Args:
            directory (str): The directory to recursively walk through and 
                find files with the extension 'file_ext'.

        Returns:
            all_files (set): A Python set containing strings representing the 
                paths for each file found with the desired file extension.
        """
        all_files = set()
        # os.walk yields a tuple: (curr_dir, list_subdirs, list_files)
        for dirpath, dirnames, filenames in os.walk(directory):
            for filename in filenames:
                if filename.endswith(self.file_ext):
                    all_files.add(filename)
        return all_files
    
    def compare_files(self, verbose: bool=True):
        """Compares two directories for unique files.
        
        Compares files with the file extension chosen
        during class initialization. Saves txt files with the
        unique files from each directory into log_path.

        Args:
            verbose (bool, optional): Choose whether to print the unqiue
                files from each directory within the shell. Defaults to True.

        Returns:
            None.
        """
        db_files1 = self.get_files(self.dir1)
        db_files2 = self.get_files(self.dir2)
    
        only_in_dir1 = db_files1 - db_files2
        only_in_dir2 = db_files2 - db_files1
        
        with open(self.log_path + r"\dir1_uniq_files.txt", "w") as f:
            for item in sorted(list(only_in_dir1)):
                f.write(str(item) + "\n")
                
        with open(self.log_path + r"\dir2_uniq_files.txt", "w") as f:
            for item in sorted(list(only_in_dir2)):
                f.write(str(item) + "\n")
        
        if verbose:
            if only_in_dir1:
                print(f"files found only in '{self.dir1}':")
                for item in only_in_dir1:
                    print(f"- {item}")
            else:
                print(f"No unique files in '{self.dir1}'")
            
            if only_in_dir2:
                print(f"files found only in '{self.dir2}':")
                for item in only_in_dir2:
                    print(f"- {item}")
            else:
                print(f"No unique files in '{self.dir2}'")