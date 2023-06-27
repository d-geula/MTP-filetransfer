Easily transfer files to a MTP storage device using mtpcount in Python.

# Requirements
[mtpmount](https://github.com/hst125fan/mtpmount) (included in the tools folder)

Dokan library ([v1.5.1.1](https://github.com/dokan-dev/dokany/releases/tag/v1.5.1.1000))

Ensure that you have installed the Dokan library by following these steps:
1. Run the installer file (.msi) to launch the installation wizard.
2. Follow the on-screen instructions to complete the installation.

# Usage

1. Import the `MTPManager` class:
    ```
    from mtp import MTPManager
    ```

2. Create an instance of the `MTPManager` class by providing the necessary parameters:
    ```
    mtp = MTPManager(mtpmount_path, device_name, storage_name, drive_letter, verbose=True)
    ```
    - `mtpmount_path` (str):
        The path to the mtpmount executable.
    - `device_name` (str):
        The name of the device to mount.
    - `storage_name` (str):
        The name of the storage to mount.
    - `drive_letter` (str):
        The drive letter to mount the storage to.
    - `verbose` (bool, optional):
        Whether to print the output of subprocess commands.

3. Copy files and/or folders to the MTP device using the `copy_files` method:
    ```
    mtp.copy_files(src, dest, overwrite=False)
    ```
    - `src` (list): A list of source file or folder paths to be copied.
    - `dest` (str): The destination path on the MTP device.
    - `overwrite` (bool, optional): Set to `True` to overwrite existing files or folders without prompting (default is `False`).

<br>

# Example

Here's a complete example demonstrating the usage of `MTPManager`:

```
from mtp import MTPManager

mtp = MTPManager(
    mtpmount_path="tools\mtpmount-x64\mtpmount.exe",
    device_name="MyDevice",
    storage_name="Internal shared storage",
    drive_letter="X",
    verbose=False,  # Optional, default is True
)

# Copy to device
mtp.copy_files(
    src=[
        "tests/folder2",  # Folder
        "tests/file.jpg",  # File
    ],
    dest="X:/",
    overwrite=False,  # Optional, default is False
)

# Copy from device
mtp.copy_files(
    src=[
        "X:/folder",
        "X:/file.jpg",
    ],
    dest="tests/copied/",
    overwrite=True,
)
```

# Licence
Do whatever you want with this code.
