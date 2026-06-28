# Professional / Community 1.7.24

Source: https://portswigger.net/burp/releases/professional-community-1-7-24
Fetched: 2026-06-28T09:16:31.916876+00:00

This release adds a new feature to save a copy of the current project.

You can choose the tools whose data you want to be included in the project file and whether you only want to save in-scope items.

The new feature is useful for various purposes:

You can begin working in a temporary project, and later save it to disk if it proves useful.

You can save a live backup copy of a disk-based project while continuing to work.

You can save a smaller copy of a project after refining your target scope or deleting unnecessary data.

Note that after Burp saves the copy of the current project, it continues working in the current project. If you want to switch to using the newly saved copy, you will need to restart Burp and select the new project file at startup.

Some bugs have also been fixed:

A bug that caused SNI not to work with upstream HTTP proxy servers.

A bug that caused the Burp Infiltrator patcher to cause bytecode corruption, or fail to patch at all, when certain unusual bytecode features were encountered.

A bug that could cause remembered user settings to be lost if the user closed down Burp during startup.

Various other bugfixes and enhancements.
