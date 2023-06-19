# Author: D.Geula
# GitHub: https://github.com/d-geula
# Date: 18-06-2023
# Description: python access for mtpmount


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

        # just in case the process is still running
        self.kill_process(self.process_name)

        try:
            self.manage_storage("mount")
            overwrite_flag = "/Y" if overwrite else ""

            dest = Path(dest).resolve()
            for src_path in src:
                src_path = Path(src_path).resolve()
                dest_item_path = dest / src_path.name

                if src_path.is_file():
                    self.run_cmd(f'xcopy "{src_path}" "{dest}" {overwrite_flag}')

                elif src_path.is_dir():
                    self.run_cmd(
                        f'xcopy "{src_path}" "{dest_item_path}" /E /I {overwrite_flag}'
                    )

                else:
                    raise ValueError(
                        f"Invalid path: {src_path} is neither a file nor a folder."
                    )

            unmount = self.manage_storage("unmount")
            if unmount.returncode == 0:
                self.kill_process(self.process_name)

        except Exception as e:
            print(e)
            self.kill_process(self.process_name)

    def manage_storage(self, operation: str):
        """
        Mounts or unmounts the specified storage on the device.
        """

        return self.run_cmd(
            f'"{self.mtpmount_path}" {operation} "{self.device_name}" "{self.storage_name}" {self.drive_letter}'
        )

    def kill_process(self, process_name):
        """
        Terminates the specified process if it is running.
        """

        # Check if the process is running
        cmd = f'tasklist /fi "imagename eq {process_name}"'
        process_check = subprocess.run(cmd, capture_output=True, text=True)

        # Check if the process name is found in the tasklist output
        if process_name.lower() in process_check.stdout.lower():
            # Terminate the process
            self.run_cmd(f"taskkill /f /im {process_name}")

    def run_cmd(self, cmd):
        results = subprocess.run(cmd, shell=True, check=True)
        return results
