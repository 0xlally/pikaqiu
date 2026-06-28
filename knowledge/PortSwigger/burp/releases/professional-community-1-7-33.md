# Professional / Community 1.7.33

Source: https://portswigger.net/burp/releases/professional-community-1-7-33
Fetched: 2026-06-28T09:16:32.207514+00:00

This release significantly improves the effectiveness of project repair when project file corruption occurs. Some users still experience corrupted project files when using virtualized file systems (for example, using Burp within a guest VM can lead to project file corruption if the host OS terminates abnormally). Previously, if some key metadata near the start of the project file was lost, then Burp's project repair feature would not recover any data. In the new release, uncorrupted data within the file can still be recovered even if this key metadata is lost. Further feedback is welcomed regarding the effectiveness of project repair.

To support the new project repair function, changes have been made to the Burp project file format. The new release is backwards compatible with project files from all prior versions, but project files created with the new release cannot be opened with older versions of Burp.

Some bugs have been fixed:

A bug in macro configuration where some settings for cookie handling might not be saved correctly across executions of Burp.

Some minor bugs in the automatic project backup feature that was recently released.

A bug where extensions could still gain API access to the Burp Collaborator client even when the user had disabled use of Collaborator.
