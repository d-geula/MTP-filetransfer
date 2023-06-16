import subprocess
from pathlib import Path


def manage_storage(device_name, storage_name, drive_letter, operation):
    """
    Mounts or unmounts the specified storage on the device.

    Args:
        device_name (str): The name of the device.
        storage_name (str): The name of the storage to be managed.
        drive_letter (str): The drive letter to assign to the mounted storage.
        operation (str): The operation to perform. Possible values: "mount" or "unmount".
    """

    mtpmount_dir = Path("tools/mtpmount-x64")
    mtpmount_cmd = f'mtpmount {operation} {device_name} "{storage_name}" {drive_letter}'
    subprocess.run(mtpmount_cmd, shell=True, cwd=mtpmount_dir)


def copy_files(file_paths, destination_path):
    """
    Copies one or more files to the specified destination path. Either full path(s) or wildcard(s).
    
    Args:
        file_paths (str or list): The path(s) of the file(s) to be copied.
            Can be a single file path as a string or a list of file paths. Wildcards are supported.

        destination_path (str): The destination path where the file(s) will be copied to.
    """

    if isinstance(file_paths, str):
        file_paths = [file_paths]  # Convert a single path to a list with one element

    for file_path in file_paths:
        command = ["copy", file_path, destination_path]
        subprocess.run(command, shell=True)


def is_process_running(process_name):
    """
    Checks if a process with the specified name is running.

    Args:
        process_name (str): The name of the process to check.

    Returns:
        bool: True if the process is running, False otherwise.
    """

    # Check if the process is running
    process_check_cmd = ['tasklist', '/fi', f'imagename eq {process_name}']
    process_check = subprocess.run(process_check_cmd, capture_output=True, text=True)

    # Check if the process name is found in the tasklist output
    if process_name.lower() in process_check.stdout.lower():
        return True
    else:
        return False
    

def terminate_process(process_name):
    """
    Terminates a process with the specified name.

    Args:
        process_name (str): The name of the process to terminate.
    """
    subprocess.run(['taskkill', '/f', '/im', process_name])
