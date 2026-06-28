# Professional / Community 2023.4

Source: https://portswigger.net/burp/releases/professional-community-2023-4
Fetched: 2026-06-28T09:16:44.105615+00:00

This release introduces improvements to Burp Intruder and Burp Scanner, ARM64 support for Linux, and a number of minor improvements and bug fixes.

Improvements to Burp Scanner

We have made a number of improvements to Burp Scanner:

You can now scan YAML API definitions.

You can now scan floating input fields, which enables Burp Scanner to better handle single-page applications (SPAs).

We have reduced the amount of noise in the event log that recorded logins produce when pop-ups close.

Improvements to Burp Intruder

We have made a number of improvements to Burp Intruder:

Payload positions are no longer predefined when you send a request to Intruder. This means that you no longer need to clear payload positions before you start to configure your attack. You can still set the automatic payload positions if required - click Auto § in the Intruder > Positions tab.

You can now preset a payload position before you send a request to Intruder, to streamline your workflow. To do this, highlight the part of the request that you want to set as a payload position, then send the request to Intruder.

We have added the ability to control whether Intruder uses HTTP/1 or HTTP/2 for a specific attack.

ARM64 on Linux

We have introduced support for ARM64 on Linux. Note that Burp's browser will only work with the installer build, not the plain JAR file.

Montoya API

We have continued to update the Montoya API, which enables you to create extensions with additional functionality:

You can now pause and resume the task execution engine.

You can now load and export user settings in JSON. This gives you more control over Burp’s configuration.

You can now add custom tabs to WebSocket message editors.

Display scaling

We have added a Scaling setting to the Settings dialog. This enables you to view Burp correctly when you use a high resolution display with custom scaling.

Bugs

We have fixed a number of minor bugs:

When you add further items to a finished task, it is now correctly relabelled as Running.

When you reopen a project file that contains completed scan tasks, they now remain completed with no further scanning actions taken.

We have fixed a bug whereby you received an error message when you loaded an extension to a temporary file with a path that contains spaces.

We have fixed a bug whereby extension popups displayed incorrectly when Burp was set to automatically recognize character sets.

Chromium upgrade

This release upgrades Burp's browser to Chromium 112.0.5615.49 for Linux and Mac and 112.0.5615.49/50 for Windows.

Note

We have also updated Burp so that all feedback is now attributable to a Burp license. We will use this information to continue to improve your Burp experience and provide you with more targeted support. No sensitive information is transmitted in your feedback, and you can still choose to opt out of feedback at any time.
