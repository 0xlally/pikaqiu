# Professional / Community 2025.9.2

Source: https://portswigger.net/burp/releases/professional-community-2025-9-2
Fetched: 2026-06-28T09:16:56.062237+00:00

This release fixes a number of custom scan check bugs and upgrades Burp's browser.

Bug fixes

We've fixed a number of issues:

A bug that sometimes caused custom scan checks with default content to incorrectly show as modified.

A bug where new custom scan checks added while the scan launcher is open weren't enabled by default.

A bug that incorrectly caused the save dialog to be shown when double-clicking the Create using this template button.

A bug where filter text in the Bambda library prevented the split pane from resizing correctly. The left panel now truncates the filter text and shrinks as expected.

Chromium upgrade

We've upgraded Burp's browser to Chromium 140.0.7339.186

for Windows & Mac and 140.0.7339.185

for Linux. For more information, see the Chromium release notes.
