# Description
A simple python interface for the mtpmount command line tool.

# Requirements
[mtpmount](https://github.com/hst125fan/mtpmount) (included in the tools folder)

Dokan library ([v1.5.1.1](https://github.com/dokan-dev/dokany/releases/tag/v1.5.1.1000))

Ensure that you have installed the Dokan library by following these steps:
1. Run the installer file (.msi) to launch the installation wizard.
2. Follow the on-screen instructions to complete the installation.

# Usage

1. Import the `MTPManager` class:
    ```py
    from mtpmanager import MTPManager
    ```

2. Create an instance of the `MTPManager` class by providing the necessary parameters:
    ```py
    mtp = MTPManager(mtpmount_path, device_name, storage_name, drive_letter, verbose=True)
    ```
    - `mtpmount_path` (path_like):
        The path to the mtpmount executable.
    - `device_name` (str):
        The name of the device to mount.
    - `storage_name` (str):
        The name of the storage to mount.
    - `drive_letter` (str):
        A valid drive letter (D-Z) that is not already in use to mount the storage to.
    - `verbose` (bool, default=True):
        Whether to print the output of subprocess commands.

3. Copy files and/or folders to the MTP device using the `copy` method:
    ```py
    mtp.copy(src, dest, overwrite=False)
    ```
    - `src` (path_like or list of path_like): A single path or a list of source paths to copy.
    - `dest` (path_like): The destination path to copy to on the MTP device.
    - `overwrite` (bool, default=False): Adds the '/Y' flag to the xcopy command to overwrite files without prompting.

<br>

# Example

Here's a complete example demonstrating the usage of `MTPManager`:

```py
from mtpmanager import MTPManager

mtp = MTPManager(
    mtpmount_path="tools\mtpmount-x64\mtpmount.exe",
    device_name="MyDevice",
    storage_name="Internal shared storage",
    drive_letter="X",
    verbose=False,  # Optional, default is True
)

# Copy to device
mtp.copy(
    src=[
        "path/to/folder",
        "path/to/file.jpg",
    ],
    dest="X:/",
    overwrite=False,  # Optional, default is False
)

# Copy from device
mtp.copy(
    src="X:/file.jpg",
    dest="path/to/destination",
    overwrite=True,
)
```
