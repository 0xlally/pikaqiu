# Professional / Community 2021.4.1

Source: https://portswigger.net/burp/releases/professional-community-2021-4-1
Fetched: 2026-06-28T09:16:35.005942+00:00

This release provides logging for individual task traffic. It also provides a new hotkey action, support for multiple TXT DNS records in Burp Collaborator, and several bug fixes.

Task logger

You can now view log traffic for individual tasks (such as scans). This allows you to analyze what's happening if one of your tasks shows unexpected behavior, or to monitor a task's progress.

To see the log for a task, click on the task's "View details" icon and then select the "Logger" tab. Logging for each task has its own memory limit, separate from the main Burp Logger.

Hotkey for "Clear all payload markers"

We have added "Clear all payload markers", for Intruder, to the list of actions that you can assign a hotkey to.

Multiple custom TXT DNS records in Burp Collaborator

We have added support for multiple custom TXT DNS records within Burp Collaborator. You can read more here.

Bug fixes

This release also provides several bug fixes:

Filter dialogs now work correctly when you use the settings button to restore defaults or load a configuration.

We have improved the heuristics of the crawler to better fill out text fields in forms.

The crawler now correctly clears session data held in local storage when it is no longer needed.
