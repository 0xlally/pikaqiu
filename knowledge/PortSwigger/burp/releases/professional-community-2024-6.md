# Professional / Community 2024.6

Source: https://portswigger.net/burp/releases/professional-community-2024-6
Fetched: 2026-06-28T09:16:47.818023+00:00

This release introduces scan checks for detecting OpenAPI definitions, support for scanning OpenAPI v2.0 definitions, and some changes to the user interface. We've also made performance improvements to the site map filter, and fixed some bugs.

Scan checks for detecting OpenAPI definitions

Burp Suite Professional now includes active and passive scan checks for detecting OpenAPI definitions during scans and while browsing. The scan checks use a list of common OpenAPI definition file names and locations to search for publicly available definitions. This enables you to more easily find API definitions, enabling you to identify further attack surface that they may expose.

Support for OpenAPI v2.0 definitions

We've introduced support for scanning OpenAPI version 2.0 definitions, so that you can scan more of your APIs.

User interface changes

In the Settings > User interface menu, we split Inspector and message editor into two separate pages: Side panel and Message editor. You can adjust the Inspector widget settings from the Side panel menu.

Quality of life improvements

We made the following quality of life improvements:

We now enter text for recorded logins character by character, instead of as a whole string. This more realistically simulates keys being pressed and released.

You can now add a hotkey to quickly open and close the Event log or All issues panel from the bottom dock. If you've detached the Event log or All issues panel, the hotkey brings the detached window to the front of your screen.

When you sort large tables such as the Proxy HTTP history, we now show a spinner in the table column header. This shows you that sorting is in progress.

Performance improvements

We made the following performance improvements:

We improved the performance of the site map filters when filtering large datasets or using complex filter criteria. Filters that previously could take several hours to apply can now complete in minutes.

CPU usage no longer spikes if you scroll the Proxy HTTP history table while using custom columns.

Bug fixes

We fixed the following bugs:

We corrected the default width of the Repeater request pane.

Live audits now resume if a project file is closed and reopened.

Updates to the Intruder table filter during an attack are now applied to new messages as the attack runs.

If you're using a Mac, the message editor Response > Render tab now correctly scales content.

We fixed a bug with disk-based project files. In version 2024.5.3 of Burp, the Target tab wasn't visible for projects with crawl tasks started in previous versions of Burp.
