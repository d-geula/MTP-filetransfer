# Author: D.Geula
# GitHub: https://github.com/d-geula
# Date: 18-06-2023
# Description: Provides a simple python interface for the mtpmount command line tool.

import re
import subprocess
from pathlib import Path
from typing import Optional


""" def _validate(arg):
    if arg == drive_letter:
        # do something
    elif arg == drive_letter:
        # do something else
    elif arg == dest:
        # do something else """


class MTPManager:
    """Provides a simple python interface for the mtpmount command line tool."""

    def __init__(
        self,
        device_name: str,
        storage_name: str,
        drive_letter: str,
        verbose: Optional[bool] = True,
    ):
        """
        Initializes a new instance of the MTPManager class.

        Use `manage_storage()` to mount/unmount the storage manually, or use the context manager to do it automatically.

        Parameters
        ----------
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
        ValueError
            If `drive_letter` is not a valid drive letter (D-Z).
        """
        self._mtpmount = Path("tools/mtpmount-x64.exe")
        self.device_name = device_name
        self.storage_name = storage_name

        if not re.match("^[D-Zd-z]$", drive_letter):
            raise ValueError(f'"{drive_letter}" is not a valid drive letter (D-Z).')

        self.drive_letter = drive_letter
        self.verbose = verbose
        self._mounted = False

    def __enter__(self):
        print("enter method called")

        self.manage_storage("mount")
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        print("exit method called")
        print(f"exc_type: {exc_type}")
        print(f"exc_value: {exc_value}")
        self._kill_process()

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
            The destination path to copy to on the MTP device.
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

        overwrite_flag = "/Y"

        if not isinstance(src, list):
            src = [src]

        dest = Path(dest).resolve()
        src = [Path(path).resolve() for path in src]

        for path in src:
            try:
                if path.is_file():
                    cmd = ["xcopy", str(path), str(dest)]
                    if overwrite:
                        cmd.append(overwrite_flag)
                    self._run(cmd, check=True)

                elif path.is_dir():
                    dest_dir_path = dest / path.name
                    cmd = ["xcopy", str(path), str(dest_dir_path), "/E", "/I"]
                    if overwrite:
                        cmd.append(overwrite_flag)
                    self._run(cmd, check=True)

                else:
                    raise ValueError(f'the path "{path}" does not exist.')

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

    def manage_storage(self, operation) -> int:
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
            self._run(
                [
                    self._mtpmount,
                    operation,
                    self.device_name,
                    self.storage_name,
                    self.drive_letter,
                ],
                check=True,
            )
            return 0
        except subprocess.CalledProcessError as e:
            raise e

    def _kill_process(self):
        self._run(["taskkill", "/f", "/im", "mtpmount-x64.exe"])

    def _run(self, cmd, **kwargs) -> int:
        if not self.verbose:
            kwargs.setdefault("capture_output", True)

        # override verbose for xcopy prompts
        if "xcopy" in cmd and "/Y" not in cmd:
            kwargs["capture_output"] = False

        return subprocess.run(cmd, **kwargs).returncode
