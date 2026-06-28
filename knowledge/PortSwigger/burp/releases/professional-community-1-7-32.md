# Professional / Community 1.7.32

Source: https://portswigger.net/burp/releases/professional-community-1-7-32
Fetched: 2026-06-28T09:16:32.053628+00:00

This release adds a new automatic project file backup function. If you are using a disk-based project, this function automatically saves a backup copy of your project file periodically in the background. The options for the new function can be found at User options / Misc / Automatic Project Backup:

The new function is superior to the older function that saved a state file backup in several respects:

Project file backups are considerably faster. Project files of 1Gb in size are typically backed up in a few seconds.

You can optionally include in-scope items only, to reduce the size of the backup file.

Available disk space is checked before performing a backup. If insufficient space is available, the backup is skipped and an alert is shown.

A single backup file is saved alongside the main project file. On successful completion of a new backup, the previous backup file is deleted.

On attempting to open a corrupted project file, Burp checks if a backup is available, and if so offers to open that as an alternative to repairing the original.

By default, the backup file is deleted on clean shutdown of Burp. Since the main project file is saved incrementally in real time, and project file corruption is typically caused by abnormal termination of the OS, it is not normally necessary to retain backup files following a clean shutdown. You can choose to retain the backup file on shutdown in the automatic project backup options.

You can optionally disable the progress dialog that is shown when a backup is performed, so you can continue working without interruption.

Backups are enabled by default with no configuration required. If you don't want to use the feature, you can quickly turn it off using the option that is shown in the progress dialog:

Other enhancements include:

Installed BApps are now updated automatically on startup. We issue frequent updates to BApps and it is highly recommended to be using the latest versions. You can disable automatic BApp updates in Extender options.

A bug in the import project function, which omitted to import the Scanner issue activity log, has been fixed.

Requests made by extensions during custom scan checks are now correctly reflected in the scan queue request counts, and are correctly subjected to configured request throttling.
