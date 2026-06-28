# Professional / Community 2021.2.1

Source: https://portswigger.net/burp/releases/professional-community-2021-2-1
Fetched: 2026-06-28T09:16:34.647921+00:00

This release provides multiple Burp Suite update channels, including an Early Adopter channel. It also provides improved Intruder payload lists and several bug fixes.

Multiple update channels

We now deliver automatic updates to Burp Suite via two channels: Stable and Early Adopter. The default channel for all users is Stable. New versions of Burp Suite will appear on the Early Adopter channel first, and then go to the Stable channel when any initial problems have been resolved. The update channel setting is per installation, so multiple installations set to different update channels are possible.

Choose the Early Adopter channel to get the latest features fast. Choose the Stable channel for the most robust and reliable version of Burp Suite.

To change your update channel, go to "User options" and select the "Misc" tab. Then scroll down to "Update" and select the channel you prefer.

Improved Intruder default payload lists

We have improved and expanded Intruder's default payload lists. There are also new lists, such as SSRF payloads and common files and directories.

Bug fixes

This release also provides several bug fixes, such as:

Custom User-Agent values will now save correctly if they contain a colon character.

Using the rule to disable browser XSS protection in Proxy options no longer results in an error.

Windows created by generating a CSRF PoC now open correctly, rather than opening behind the main Burp window.
