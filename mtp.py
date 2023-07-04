# Author: D.Geula
# GitHub: https://github.com/d-geula
# Date: 18-06-2023
# Description: Provides simple a python interface for the mtpmount command line tool.

import re
import sys
import subprocess
from pathlib import Path
from typing import Optional


class MTPManager:
    """
    Provides simple a python interface for the mtpmount command line tool.

    Parameters
    ----------
    mtpmount_path : path_like
        The path to the mtpmount executable.
    device_name : str
        The name of the device to mount.
    storage_name : str
        The name of the storage to mount.
    drive_letter : str
        A valid drive letter (D-Z) that is not already in use to mount the storage to.
    verbose : bool, default=True
        Whether to print the output of subprocess commands.

    Raises
    ------
    FileNotFoundError
        If `mtpmount_path` is not a valid file path.
    ValueError
        If `drive_letter` is not a valid drive letter (D-Z).
    """

    def __init__(
        self,
        mtpmount_path,
        device_name: str,
        storage_name: str,
        drive_letter: str,
        verbose: Optional[bool] = True,
    ):
        if not Path(mtpmount_path).is_file():
            raise FileNotFoundError(
                f'the mtpmount path "{mtpmount_path}" does not exist.'
            )
        else:
            self.mtpmount_path = Path(mtpmount_path)
            self.process_name = self.mtpmount_path.name

        self.device_name = device_name
        self.storage_name = storage_name

        if not re.match(r"^[D-Zd-z]$", drive_letter):
            raise ValueError(f'"{drive_letter}" is not a valid drive letter (D-Z).')
        else:
            self.drive_letter = drive_letter

        self.verbose = verbose

    def copy(self, src, dest, overwrite: Optional[bool] = False) -> None:
        """
        Copies one or more source paths to a destination path on the MTP device.

        This method uses the xcopy command to copy files and folders,
        as well as automatically handle the mounting and unmounting of the MTP device.

        Parameters
        ----------
        src : path_like or list of path_like
            A single path or a list of source paths to copy.
        dest : path_like
            The destination path to copy to.
        overwrite : bool, default=False
            Adds the '/Y' flag to the xcopy command to overwrite files without prompting.

        Raises
        ------
        ValueError
            If `dest` does not match the drive letter of the MTP device.
        ValueError
            If `dest` is not a valid drive path format (e.g. X:/).
        """

        if not dest.lower().startswith(self.drive_letter.lower()):
            raise ValueError(
                f"destination path does not match the drive letter of the "
                'MTP device ("{self.drive_letter}").'
            )

        if not re.match(r"^[A-Za-z]:/", dest):
            raise ValueError("invalid drive path format (e.g. X:/)")

        # just in case the process is still running
        self.kill_process(self.process_name)

        self.manage_storage("mount")
        overwrite_flag = "/Y"

        if not isinstance(src, list):
            src = [src]

        dest = Path(dest).resolve()
        src = [Path(src_path).resolve() for src_path in src]

        for src_path in src:
            try:
                if src_path.is_file():
                    cmd = ["xcopy", str(src_path), str(dest)]
                    if overwrite:
                        cmd.append(overwrite_flag)
                    self.run_cmd(cmd, check=True)

                elif src_path.is_dir():
                    dest_dir_path = dest / src_path.name
                    cmd = ["xcopy", str(src_path), str(dest_dir_path), "/E", "/I"]
                    if overwrite:
                        cmd.append(overwrite_flag)
                    self.run_cmd(cmd, check=True)

                else:
                    raise ValueError(f'the path "{src_path}" does not exist.')

            # user can skip the current item or cancel the entire operation
            except ValueError as e:
                while True:
                    response = input(
                        f"{e}\nDo you want to skip this item, or cancel the operation? "
                        "Y (skip), N (cancel): "
                    )
                    if response.lower() in ["y", "n"]:
                        break

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
            The operation to perform (mount or unmount).

        Returns
        -------
        subprocess.CompletedProcess
            Used to check the return code of the mount operation.
        """
        try:
            cmd = [
                str(self.mtpmount_path),
                operation,
                self.device_name,
                self.storage_name,
                self.drive_letter,
            ]
            mount_operation = self.run_cmd(cmd, check=True)
            return mount_operation

        except subprocess.CalledProcessError as e:
            if not self.verbose:
                print(
                    f"\nFailed to {operation} storage: {e}\n"
                    "Check that the device is connected and the details are correct."
                )
            self.kill_process(self.process_name)
            sys.exit(1)

    def kill_process(self, process_name: str) -> None:
        """
        Terminates the specified process if it is running.

        Parameters
        ----------
        process_name : str
            The executable name of the process to terminate.
        """

        # Check if the process is running
        cmd = ["tasklist", "/fi", f"imagename eq {process_name}"]
        process_check = self.run_cmd(cmd, capture_output=True, text=True)

        # Check if the process name is found in the tasklist output
        if process_name.lower() in process_check.stdout.lower():
            cmd = ["taskkill", "/f", "/im", process_name]
            self.run_cmd(cmd)

    def run_cmd(self, cmd: list[str], **kwargs) -> subprocess.CompletedProcess:
        """
        Executes the specified command.

        Parameters
        ----------
        cmd : list of str
            The command to execute.
        **kwargs
            Keyword arguments to pass to `subprocess.run()`.

        Returns
        -------
        subprocess.CompletedProcess
            Used to check the return code of the command.
        """

        if not self.verbose:
            kwargs.setdefault("capture_output", True)

        # allow output even when verbose is False so user can interact with xcopy prompts
        if "xcopy" in cmd and "/Y" not in cmd:
            kwargs["capture_output"] = False

        return subprocess.run(cmd, **kwargs)
