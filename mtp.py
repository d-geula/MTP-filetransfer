import subprocess
from pathlib import Path


def manage_storage(
    device_name: str, storage_name: str, drive_letter: str, operation: str
):
    """
    Mounts or unmounts the specified storage on the device.
    """

    mtpmount_dir = Path("tools/mtpmount-x64")
    cmd = f'mtpmount {operation} {device_name} "{storage_name}" {drive_letter}'
    subprocess.run(cmd, shell=True, cwd=mtpmount_dir)


def copy_files(src: list, dest, overwrite=False):
    """
    Copies one or more files or folders to the specified destination path.

    Set `overwrite` to True if you want to overwrite existing files or folders without prompting.
    """
    overwrite_flag = "/Y" if overwrite else ""

    for src_path in src:
        dest_item_path = Path(dest) / Path(src_path).name

        if Path(src_path).is_file():
            cmd = f'xcopy "{src_path}" "{dest}" {overwrite_flag}'
            subprocess.run(cmd, shell=True, check=True)

        elif Path(src_path).is_dir():
            cmd = f'xcopy "{src_path}" "{dest_item_path}" /E /I {overwrite_flag}'
            subprocess.run(cmd, shell=True, check=True)

        else:
            raise ValueError(
                f"Invalid path: {src_path} is neither a file nor a folder."
            )


def is_process_running(process_name: str) -> bool:
    """
    Checks if a process with the specified name is running.
    """

    # Check if the process is running
    process_check_cmd = ["tasklist", "/fi", f"imagename eq {process_name}"]
    process_check = subprocess.run(process_check_cmd, capture_output=True, text=True)

    # Check if the process name is found in the tasklist output
    if process_name.lower() in process_check.stdout.lower():
        return True
    else:
        return False


def terminate_process(process_name: str):
    """
    Terminates a process with the specified name.
    """
    subprocess.run(["taskkill", "/f", "/im", process_name])
