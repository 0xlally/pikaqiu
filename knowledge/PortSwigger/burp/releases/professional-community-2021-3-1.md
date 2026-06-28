# Professional / Community 2021.3.1

Source: https://portswigger.net/burp/releases/professional-community-2021-3-1
Fetched: 2026-06-28T09:16:34.823617+00:00

This release provides a security fix for the embedded Chromium browser, and several bug fixes.

Chromium security fix

This release includes an update of Burp's embedded browser to Chromium 89.0.4389.90 which fixes a security issue that Google have classified as high.

Bug fixes

This release provides several bug fixes, including:

Copy and cut hotkeys now work in inspector tables, and the copied data is formatted appropriately for the types of items in the table.

Burp Suite now correctly deletes update files after they have been used.

The title bar now displays the name of the update channel you have has chosen if it is not the Stable channel.

We have improved the layout of the Intruder "Grep - Payloads" panel.

Unwanted update behaviour no longer happens when you have more than one installation of Burp Suite on macOS.

We have fixed an issue where the crawler encounters an error if it finds links with URL fragments during the "discovering hidden content" section of the crawl.

We have converted filter pop-up windows to dialog boxes throughout Burp Suite, to improve consistency.
