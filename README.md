# MTP-filetransfer
Functions to mount, unmount, and transfer files to an MTP device using [mtpmount](https://github.com/hst125fan/mtpmount) in Python.

# Requirements
mtpmount ([latest](https://github.com/hst125fan/mtpmount/releases/tag/19.8.0))

Dokan library ([v1.5.1.1](https://github.com/dokan-dev/dokany/releases/tag/v1.5.1.1000))

Ensure that you have installed the Dokan library by following these steps:
1. Run the installer file (.msi) to launch the installation wizard.
2. Follow the on-screen instructions to complete the installation.

# Usage
### Storage management
`manage_storage(device_name, storage_name, drive_letter, operation)`

Mounts or unmounts the specified storage on the device.
* device_name (str): The name of the device.
* storage_name (str): The name of the storage to be managed.
* drive_letter (str): The drive letter to assign to the mounted storage.
* operation (str): The operation to perform. Possible values: "mount" or "unmount".

### Transfer files to device
`copy_files(file_paths, destination_path)`

Copies one or more files to the specified destination path.

* file_paths (str or list): The path(s) of the file(s) to be copied. Can be either full path(s) or wildcard(s).
* destination_path (str): The destination path where the file(s) will be copied to.

### mtpmount process management
> **Note**
> It is advised that you kill the mtpmount process before (and after) trying to transfer files. It might be unnecessary for you, but I've found that it causes problems otherwise.

`is_process_running(process_name)`

Checks if a process with the specified name is running.
* process_name (str): The name of the process to check.

Returns:
* bool: True if the process is running, False otherwise.
<br>

`terminate_process(process_name)`

Terminates a process with the specified name.
* process_name (str): The name of the process to terminate.
