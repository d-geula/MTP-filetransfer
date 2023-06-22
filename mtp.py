# Author: D.Geula
# GitHub: https://github.com/d-geula
# Date: 18-06-2023
# Description: python access for mtpmount.


import subprocess
from pathlib import Path


class MTPManager:
    """
    Initializes an instance of the MTPManager class.

    Parameters
    ----------
    mtpmount_path
        The path to the mtpmount executable.
    device_name : str
        The name of the device to mount.
    storage_name : str
        The name of the storage to mount.
    drive_letter : str
        The drive letter to assign to the mounted storage.
    """

    def __init__(
        self, mtpmount_path, device_name: str, storage_name: str, drive_letter: str
    ):
        self.mtpmount_path = Path(mtpmount_path)
        self.process_name = self.mtpmount_path.name
        self.device_name = device_name
        self.storage_name = storage_name
        self.drive_letter = drive_letter

    def copy_files(self, src: list, dest, overwrite=False):
        """
        Copies one or more files or folders to the specified destination path.

        Parameters
        ----------
        src : list
            A list of source paths to copy.
        dest
            The destination path to copy to.
        overwrite : bool, optional
            Overwrite existing files at the destination without prompting for confirmation.

        Raises
        ------
        ValueError
            If `src_path` is not a valid file or folder path.
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

    def manage_storage(self, operation: str) -> subprocess.CompletedProcess:
        """
        Mounts or unmounts the specified storage on the device.

        Parameters
        ----------
        operation : str
            The operation to perform. Must be either "mount" or "unmount".

        Returns
        -------
        subprocess.CompletedProcess
            The result of the command execution.
        """

        return self.run_cmd(
            f'"{self.mtpmount_path}" {operation} "{self.device_name}" "{self.storage_name}" {self.drive_letter}'
        )

    def kill_process(self, process_name: str):
        """
        Terminates the specified process if it is running.

        Parameters
        ----------
        process_name : str
            The name of the process to terminate.
        """

        # Check if the process is running
        cmd = f'tasklist /fi "imagename eq {process_name}"'
        process_check = subprocess.run(cmd, capture_output=True, text=True)

        # Check if the process name is found in the tasklist output
        if process_name.lower() in process_check.stdout.lower():
            self.run_cmd(f"taskkill /f /im {process_name}")

    def run_cmd(self, cmd: str) -> subprocess.CompletedProcess:
        """
        Executes the specified command.

        Parameters
        ----------
        cmd : str
            The command to execute.

        Returns
        -------
        subprocess.CompletedProcess
            The result of the command execution.
        """

        results = subprocess.run(cmd, shell=True, check=True)
        return results
