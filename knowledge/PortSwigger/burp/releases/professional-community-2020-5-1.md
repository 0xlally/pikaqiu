# Professional / Community 2020.5.1

Source: https://portswigger.net/burp/releases/professional-community-2020-5-1
Fetched: 2026-06-28T09:16:34.109257+00:00

This release provides several bug fixes, including the following improvements to the HTTP message editor:

Highlighting text no longer causes it to disappear and reappear after resizing the panel.

Clicking on an empty line now positions the cursor where you click instead of at the end of the previous line.

We have also fixed a security bug that was reported via our bug bounty program. With a significant amount of user interaction, an attacker could potentially read local files. The attacker would have to induce a user to visit a malicious website, copy the request as a curl command, and then execute it via the command line. This was classed as a medium severity issue due to the level of user interaction required.
