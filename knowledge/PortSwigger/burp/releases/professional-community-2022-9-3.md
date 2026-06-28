# Professional / Community 2022.9.3

Source: https://portswigger.net/burp/releases/professional-community-2022-9-3
Fetched: 2026-06-28T09:16:39.284514+00:00

This release provides some minor bug fixes and upgrades Burp's browser.

Browser upgrade

We have upgraded Burp's browser to Chromium 106.0.5249.119, which fixes a number of high-severity security issues.

Security patch

This release also patches a low-severity security issue that was reported via our bug bounty program. We will provide further details once the patch is available on our Stable release channel.

Bug fixes

This release also includes a couple of bug fixes, including:

We have fixed a bug whereby Repeater was not identifying streaming responses correctly, meaning that the affected responses would never complete.

We have fixed a UI issue whereby checkboxes and radio buttons were not displaying correctly on the Extensions tab when using the Light display theme.
