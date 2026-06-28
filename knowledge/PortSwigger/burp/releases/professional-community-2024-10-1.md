# Professional / Community 2024.10.1

Source: https://portswigger.net/burp/releases/professional-community-2024-10-1
Fetched: 2026-06-28T09:16:45.487626+00:00

This release introduces a new setting which gives you more control over the Intruder side panel layout. We've also fixed a couple of bugs.

Intruder side panel layout

We've added the Default Intruder side panel layout setting, which enables you to configure the Intruder sidebar layout independently from other sidebars. This gives you more control over your Intruder workspace layout.

Bug fixes

We've fixed the following bugs:

An issue that was preventing editing extension driven active audit tasks.

An issue where browser resources were not immediately released after completion of each crawl segment.

An issue on Windows where Intruder attacks wouldn't start if the attack configuration was copied from a previous tab with payload encoding enabled but no encoding characters specified.
