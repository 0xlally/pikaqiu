# Professional / Community 2021.10.3

Source: https://portswigger.net/burp/releases/professional-community-2021-10-3
Fetched: 2026-06-28T09:16:34.443412+00:00

This release provides a security patch, as well as several minor bug fixes.

Security patch

We have fixed a medium-severity security issue in the way Burp Suite processed HTTP/2 responses, which could have introduced XSS in certain circumstances.

Thanks to Ademar Nowasky Junior | @nowaskyjr, who reported this issue via our bug bounty program.

Browser upgrade

We have upgraded Burp's browser to Chromium 96.0.4664.45

Bug fixes

To prevent accidental loss of Burp project files, we have made the following adjustments:

If you create a new project file without explicitly specifying a directory, the file will now be created in your user's home directory by default.

On MacOS, if any project (.burp) files are detected within your Burp Suite installation directory, or any of its subdirectories, new updates will be prevented from running. In this case, you will be notified that you need to move your project files before you can update Burp Suite.
