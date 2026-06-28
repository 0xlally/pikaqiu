# Professional 1.5.14

Source: https://portswigger.net/burp/releases/professional-1-5-14
Fetched: 2026-06-28T09:16:25.274864+00:00

This release includes various small enhancements and bugfixes:

The Repeater tool now lets you configure the layout of the main request and response views. You can display these in a left/right split, a top/bottom split, or in tabs. You can change this setting via the Repeater menu.

There is a new extensibility API: IBurpExtenderCallbacks.sendToComparer().

There are new settings to enable session handling rules to be in scope for the Extender tool, and to update Burp's cookie jar based on traffic via Extender, allowing requests made by extensions to be fully integrated with Burp's session handling mechanisms.

A bug where Burp fails to wait on exit if a scheduled automatic backup is already in progress, causing the backup file to be truncated, has been fixed.

A bug that prevented the saving of state in some situations has been fixed.
