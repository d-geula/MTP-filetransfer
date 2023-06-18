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

        if self.is_running(self.process_name):
            self.kill_process(self.process_name)

        self.manage_storage("mount")

        overwrite_flag = "/Y" if overwrite else ""

        for src_path in src:
            dest_item_path = Path(dest) / Path(src_path).name

            if Path(src_path).is_file():
                cmd = f'xcopy "{src_path}" "{dest}" {overwrite_flag}'
                self.run_cmd(cmd)

            elif Path(src_path).is_dir():
                cmd = f'xcopy "{src_path}" "{dest_item_path}" /E /I {overwrite_flag}'
                self.run_cmd(cmd)

            else:
                raise ValueError(
                    f"Invalid path: {src_path} is neither a file nor a folder."
                )

        self.manage_storage("unmount")

    def manage_storage(self, operation: str):
        """
        Mounts or unmounts the specified storage on the device.
        """

        cmd = f'"{self.mtpmount_path}" {operation} "{self.device_name}" "{self.storage_name}" {self.drive_letter}'
        self.run_cmd(cmd)

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
