from pathlib import Path
import sys
import mtp

# Check the current platform
if sys.platform != "win32":
    current_platform = sys.platform
    print(f"Unsupported platform: {current_platform}")
    sys.exit(1)

# Define file and destination paths
files_to_copy = [
    Path('files/test 1.jpg'),
    Path('files/test2.jpg'),
    Path('files/*.mp3')
]

dest_path = Path('V:/')

# Check if the mtpmount process is running

mtpmount_process = 'mtpmount.exe'
if mtp.is_process_running(mtpmount_process):
    mtp.terminate_process(mtpmount_process)

# Mount the device
mtp.manage_storage('MyDeviceName', 'Internal shared storage', 'v', 'mount')

# Copy the files
mtp.copy_files(files_to_copy, dest_path)

# Unmount the device
mtp.manage_storage('MyDeviceName', 'Internal shared storage', 'v', 'unmount')

# Terminate the mtpmount process
mtp.terminate_process(mtpmount_process)