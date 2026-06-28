# Importing custom scan checks into your library

Source: https://portswigger.net/burp/documentation/desktop/extend-burp/custom-scan-checks/importing
Fetched: 2026-06-28T09:15:46.244480+00:00

Support Center

Documentation

Desktop editions

Extending Burp

Custom scan checks

Importing custom scan checks

Professional

Importing custom scan checks into your library

Last updated:

June 18, 2026

Read time:

2 Minutes

You can import custom scan checks into your library that have been shared with you or downloaded from our Bambda scripts repository or BChecks repository. Once imported, your checks are immediately available from the scan launcher and can be reused across different projects.

Related pages

For instructions on how to use custom scan checks in your scans, see Adding custom scan checks to scans.

For instructions on how to test your imported custom scan checks, see Testing custom scan checks.

Warning

Custom scan checks can run arbitrary code. For security reasons, please be cautious when importing and using scan checks from unverified sources.

To import custom scan checks into your library:

Go to Extensions > Custom scan checks.

Click Import. The Import custom scan checks dialog opens.

Select one of the following:

.bcheck files

.bambda files that define a scan check function

A folder containing .bcheck files or .bambda scan check files

Click Open.

Burp adds the selected files to your library. If you select a folder, Burp identifies any .bcheck or .bambda scan check files in the folder and its subfolders and adds them to your library.

Note

If you import a .bambda scan check file, Burp also adds it to your Bambda library, under Extensions > Bambda library.

Importing full GitHub repositories

To quickly import all custom scan checks from our GitHub repositories:

Download either the Bambda scripts repository or BChecks repository as a ZIP file.

Extract the ZIP file contents.

In Extensions > Custom scan checks, click Import. The Import custom scan checks dialog opens.

Select the extracted folder containing the GitHub repository files.

Click Open.

Burp identifies all .bcheck or .bambda scan check files in the folder and its subfolders and adds them to your library.

Updating your custom scan checks

If your checks have been modified outside Burp, you can re-import them. Burp gives you the option to replace existing checks with the new versions.

Note

As checks in our GitHub repositories may be updated frequently, we recommend re-importing these regularly to keep your library current.

How Burp overwrites script-based checks

When you create or import a script-based custom scan check, Burp assigns it a unique ID. The ID isn't visible in the interface, but Burp uses it to match checks and resolve conflicts.

If you export checks from Burp, the unique ID is included in the metadata.

When you import a .bambda file, Burp checks its unique ID against existing checks in your library. If the unique IDs match, Burp gives you the option to overwrite the existing check. If there is no matching ID, Burp treats it as a new check.

How Burp overwrites BCheck-based checks

For BCheck-based custom scan checks, Burp uses the filename to match checks instead of a unique ID.

When you import a .bcheck file with the same name as an existing check, Burp appends a number to the new file's name, keeping each BCheck as a separate entry.
