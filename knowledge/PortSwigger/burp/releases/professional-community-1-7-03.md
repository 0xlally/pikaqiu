# Professional / Community 1.7.03

Source: https://portswigger.net/burp/releases/professional-community-1-7-03
Fetched: 2026-06-28T09:16:30.697655+00:00

This release adds some enhancements to, and fixes some minor issues with, the Burp projects feature:

If the operating system exits abnormally when Burp is running with a disk-based project then some in-memory data may not be saved to disk, resulting in a partially corrupted project file. On reopening a project, Burp now detects this condition, and offers to repair the project file. The repair process will preserve as much data as possible from the corrupted project file.

When a new project is created, at the second step of the startup wizard where a configuration file is selected, Burp now lets you specify to use the selected option by default in future. If you have created a configuration file that you prefer to use for new projects, using this feature avoids the need to manually select your configuration file every time.

In the startup wizard, the lists of recently used project and configuration files now automatically hide any items that no longer exist on disk.

Burp now prevents selection of the current project file in all file dialogs, to avoid accidental overwriting of project data.

A bug that could lead to bloating of project files with redundant data has been resolved.

Thanks are due to everyone who has provided feedback about the new projects feature since the 1.7beta release. Based on the enhancements made since that release, the projects feature is now officially out of beta, and this release may be regarded as stable. As with all Burp features, we welcome ongoing feedback about the projects feature as people continue to use it.
