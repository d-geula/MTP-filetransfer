# Author: D.Geula
# GitHub: https://github.com/d-geula
# Date: 18-06-2023
# Description: python access for mtpmount.


import subprocess
from pathlib import Path


class MTPManager:
    """
    Transfers files from one or more source paths to a destination path.

    Parameters
    ----------
    mtpmount_path : str
        The path to the mtpmount executable.
    device_name : str
        The name of the device to mount.
    storage_name : str
        The name of the storage to mount.
    drive_letter : str
        The drive letter to mount the storage to.
    verbose : bool, optional
        Whether to print the output of subprocess commands.
    """

    def __init__(
        self,
        mtpmount_path: str,
        device_name: str,
        storage_name: str,
        drive_letter: str,
        verbose: bool = True,
    ):
        self.mtpmount_path = Path(mtpmount_path)
        self.process_name = self.mtpmount_path.name
        self.device_name = device_name
        self.storage_name = storage_name
        self.drive_letter = drive_letter
        self.verbose = verbose

    def copy_files(self, src, dest, overwrite=False) -> None:
        """
        Copies one or more files / folders to the specified destination path.

        Parameters
        ----------
        src
            A single path or a list of source paths to copy.
        dest
            The destination path to copy to.
        overwrite : bool, optional
            Overwrite existing files at the destination without prompting for confirmation.

        Raises
        ------
        ValueError
            If `src_path` is not a valid file or folder path.

            If the path is invalid, the user will be prompted to either skip the file/folder or cancel the operation.
            If the user chooses to skip the file/folder, the operation will continue with the remaining files/folders.
            If the user chooses to cancel the operation, the method will exit and no files/folders will be copied.
        """

        # just in case the process is still running
        self.kill_process(self.process_name)

        self.manage_storage("mount")
        overwrite_flag = "/Y" if overwrite else ""

        dest = Path(dest).resolve()
        for src_path in src:
            src_path = Path(src_path).resolve()
            dest_item_path = dest / src_path.name

            try:
                if src_path.is_file():
                    cmd = f'xcopy "{src_path}" "{dest}" {overwrite_flag}'
                    self.run_cmd(cmd, shell=True, check=True)

                elif src_path.is_dir():
                    cmd = (
                        f'xcopy "{src_path}" "{dest_item_path}" /E /I {overwrite_flag}'
                    )
                    self.run_cmd(cmd, shell=True, check=True)

                else:
                    raise ValueError(
                        f'\nInvalid path: "{src_path}" is not a valid file or folder path. '
                        "Please check the path and try again."
                    )

            except ValueError as e:
                while True:
                    response = input(
                        f"{str(e)}\nDo you want to skip this file/folder,"
                        "or cancel the operation? (Y/skip, N/cancel) "
                    )
                    if response.lower() in ["y", "n"]:
                        break
                    else:
                        print("Invalid response. Please enter either 'y' or 'n'.")

                if response.lower() == "n":
                    break
                else:
                    continue

        unmount = self.manage_storage("unmount")
        if unmount.returncode == 0:
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
            The return code of the operation, among other things.

        Raises
        ------
        SystemExit
            If the operation fails.
        """
        try:
            cmd = f'"{self.mtpmount_path}" {operation} "{self.device_name}" "{self.storage_name}" {self.drive_letter}'
            mount_operation = self.run_cmd(cmd, shell=True, check=True)
            return mount_operation

        except subprocess.CalledProcessError as e:
            print(f"\n{e}")
            self.kill_process(self.process_name)
            raise SystemExit(1)

    def kill_process(self, process_name: str) -> None:
        """
        Terminates the specified process if it is running.

        Parameters
        ----------
        process_name : str
            The name of the process to terminate.
        """

        # Check if the process is running
        cmd = f'tasklist /fi "imagename eq {process_name}"'
        process_check = self.run_cmd(cmd, capture_output=True, text=True)

        # Check if the process name is found in the tasklist output
        if process_name.lower() in process_check.stdout.lower():
            cmd = f"taskkill /f /im {process_name}"
            self.run_cmd(cmd, shell=True, check=True)

    def run_cmd(self, cmd: str, **kwargs) -> subprocess.CompletedProcess:
        """
        Executes the specified command.

        Parameters
        ----------
        cmd : str
            The command to execute.
        **kwargs
            Additional keyword arguments to pass to subprocess.run.

        Returns
        -------
        subprocess.CompletedProcess
            The return code of the command, among other things.
        """

        if not self.verbose:
            kwargs.setdefault("capture_output", True)

        return subprocess.run(cmd, **kwargs)
