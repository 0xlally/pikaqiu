# Professional / Community 2021.8.2

Source: https://portswigger.net/burp/releases/professional-community-2021-8-2
Fetched: 2026-06-28T09:16:35.773998+00:00

This release upgrades the embedded browser and fixes an issue that was reported to our bug bounty program.

Embedded browser upgrade

Burp's embedded Chromium browser has been updated to version 92.0.4515.159.

Security fix

We have fixed a vulnerability that could result in Burp Suite issuing requests that do not respect its upstream proxy configuration and could leak NetNTLM hashes on Windows systems that fail to block outbound SMB.

This issue was reported to our bug bounty program.
