# Professional / Community 2022.12.3

Source: https://portswigger.net/burp/releases/professional-community-2022-12-3
Fetched: 2026-06-28T09:16:36.969357+00:00

This release fixes bugs relating to saving reports and Burp's browser. It also upgrades Burp's browser to a later version of Chromium.

Bug fixes

We have fixed a bug whereby reports were not saving correctly on Windows machines. Burp was displaying a "Failed to open file" error at the point the report was saved.

We have fixed a bug whereby Burp's browser was unable to register service workers, causing issues with recorded login sequences and manual testing.

Browser upgrade

This release upgrades Burp's browser to Chromium 108.0.5359.98 / 99.
