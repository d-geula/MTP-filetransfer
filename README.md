# MTP-filetransfer
Mount, unmount, and transfer files to an MTP device using [mtpmount](https://github.com/hst125fan/mtpmount) in Python.

<br>

# Requirements
Dokan library ([v1.5.1.1](https://github.com/dokan-dev/dokany/releases/tag/v1.5.1.1000))

Ensure that you have installed the Dokan library by following these steps:
1. Run the installer file (.msi) to launch the installation wizard.
2. Follow the on-screen instructions to complete the installation.

<br>

# Usage

1. Import the `MTPManager` class:
    ```python
    from mtp import MTPManager
    ```

2. Create an instance of the `MTPManager` class by providing the necessary parameters:
    ```python
    mtp_manager = MTPManager(mtpmount_path, device_name, storage_name, drive_letter)
    ```
    - `mtpmount_path`: The path to the mtpmount executable.
    - `device_name`: The name of the MTP device.
    - `storage_name`: The name of the storage on the MTP device.
    - `drive_letter` (str): The drive letter to assign to the mounted storage.

3. Copy files and/or folders to the MTP device using the `copy_files` method:
    ```python
    mtp_manager.copy_files(src, dest, overwrite=False)
    ```
    - `src` (list): A list of source file or folder paths to be copied.
    - `dest`: The destination path on the MTP device.
    - `overwrite` (bool): Set to `True` to overwrite existing files or folders without prompting (default is `False`).

    <br>

    Example usage:
    ```python
    mtp_manager.copy_files(["/path/to/file.txt", "/path/to/folder"], "/destination/path", overwrite=True)
    ```

    **Note:** The `copy_files` method will automatically mount the specified storage before copying the files and unmount it afterward.

<br>

## Example

Here's a complete example demonstrating the usage of `MTPManager`:

```python
from pathlib import Path
from mtp import MTPManager

dest_path = Path("V:/")
files_to_copy = [
    Path("folder_to_copy"),
    Path("file_to_copy.jpg")
]

mtpmount_path = Path("tools/mtpmount-x64/mtpmount.exe")
device_name = "MyDeviceName"
storage_name = "Internal shared storage"
drive_letter = "v"

mtp = MTPManager(mtpmount_path, device_name, storage_name, drive_letter)

mtp.copy_files(files_to_copy, dest_path, overwrite=True)
```