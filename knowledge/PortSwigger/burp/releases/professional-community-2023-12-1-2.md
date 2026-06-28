# Professional / Community 2023.12.1.2

Source: https://portswigger.net/burp/releases/professional-community-2023-12-1-2
Fetched: 2026-06-28T09:16:46.665199+00:00

This release introduces some minor improvements and bug fixes for Burp Scanner. It also upgrades Burp's browser.

Changes to notifications

We have made the following changes to notifications:

To reduce notification noise when launching Burp, the log message indicating that the Proxy is running is now recorded as a debug log item.

The event log and All issues notifications now respect any filters you have applied. Any filtered log items do not cause these tabs to display a notification.

Large project file fix

We have fixed an issue with the way Burp Scanner handles insertion points, which was causing some project files to become disproportionately large.

Browser upgrade

We have upgraded Burp's built-in browser to 120.0.6099.216 for Mac / Linux and 120.0.6099.216/217 for Windows. For more information, see the Chromium release notes.
