from pathlib import Path
from mtp import MTPManager

dest_path = Path("V:/")
files_to_copy = [
    Path("tests/files2"),  # Folder
    Path("tests/files/test2.jpg"),  # File
    Path("tests/files/test 1.jpg"),  # File with spaces in the name
]

mtpmount_path = Path("tools/mtpmount-x64/mtpmount.exe")
device_name = "M2007J20CG"
storage_name = "Internal shared storage"
drive_letter = "v"

mtp = MTPManager(mtpmount_path, device_name, storage_name, drive_letter)

mtp.copy_files(files_to_copy, dest_path, overwrite=True)
