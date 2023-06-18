import subprocess
from pathlib import Path


class MTPManager:
    def __init__(self, mtpmount_path, device_name, storage_name, drive_letter: str):
        self.mtpmount_path = Path(mtpmount_path)
        self.process_name = self.mtpmount_path.name
        self.device_name = device_name
        self.storage_name = storage_name
        self.drive_letter = drive_letter

    def copy_files(self, src: list, dest, overwrite=False):
        """
        Copies one or more files or folders to the specified destination path.

        Set `overwrite` to True if you want to overwrite existing files or folders without prompting.
        """

        mount = self.manage_storage("mount")
        if mount.returncode == 0:
            print("Storage mounted")

            unmount = self.manage_storage("unmount")
            if unmount.returncode == 0:
                print("Storage unmounted")
                self.kill_process(self.process_name)
                print("Process killed")
            else:
                print("Storage unmount failed")
                self.kill_process(self.process_name)
                print("Process killed")
        else:
            print("Storage mount failed")
            self.kill_process(self.process_name)
            print("Process killed")

    def manage_storage(self, operation: str):
        """
        Mounts or unmounts the specified storage on the device.
        """

        cmd = f'"{self.mtpmount_path}" {operation} "{self.device_name}" "{self.storage_name}" {self.drive_letter}'
        result = subprocess.run(cmd, shell=True, check=True)
        return result

    def run_cmd(self, cmd: str):
        subprocess.run(cmd, shell=True, check=True)

    def is_running(self, process_name: str) -> bool:
        """
        Check if the specified process is running.
        """

        # Check if the process is running
        cmd = f'tasklist /fi "imagename eq {process_name}"'
        process_check = subprocess.run(cmd, capture_output=True, text=True)

        # Check if the process name is found in the tasklist output
        if process_name.lower() in process_check.stdout.lower():
            return True
        else:
            return False

    def kill_process(self, process_name: str):
        """
        Terminates the specified process.
        """

        cmd = f"taskkill /f /im {process_name}"
        self.run_cmd(cmd)
