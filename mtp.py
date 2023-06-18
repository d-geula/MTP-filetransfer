import subprocess
from pathlib import Path


class MTPManager:
    def __init__(self, mtpmount_path, device_name, storage_name, drive_letter: str):
        self.mtpmount_path = Path(mtpmount_path)
        self.process_name = self.mtpmount_path.name
        self.device_name = device_name
        self.storage_name = storage_name
        self.drive_letter = drive_letter

    def __del__(self):
        self.close(self.process_name)
        self.manage_storage("unmount")

    def copy_files(self, src: list, dest, overwrite=False):
        """
        Copies one or more files or folders to the specified destination path.

        Set `overwrite` to True if you want to overwrite existing files or folders without prompting.
        """

        self.close(self.process_name)  # just in case the process is still running
        self.manage_storage("mount")

        overwrite_flag = "/Y" if overwrite else ""

        dest = Path(dest).resolve()
        for src_path in src:
            src_path = Path(src_path).resolve()
            dest_item_path = dest / src_path.name

            if src_path.is_file():
                cmd = f'xcopy "{src_path}" "{dest}" {overwrite_flag}'
                self.run_cmd(cmd)

            elif src_path.is_dir():
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

    def close(self, process_name):
        """
        Terminates the specified process if it is running.
        """
        cmd = f"taskkill /f /im {process_name}"
        self.run_cmd(cmd)

    def run_cmd(self, cmd: str):
        subprocess.run(cmd, shell=True, check=True)
