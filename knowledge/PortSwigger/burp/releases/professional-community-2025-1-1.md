# Professional / Community 2025.1.1

Source: https://portswigger.net/burp/releases/professional-community-2025-1-1
Fetched: 2026-06-28T09:16:49.536530+00:00

This release introduces the ability to automatically pause Burp Intruder attacks based on response content, CSV export for Burp Collaborator interactions, and automatic highlighting of Content-Length response header mismatches. We've also upgraded Burp's browser and fixed several bugs.

Auto-pause Intruder attacks

We've added a new Auto-pause attack setting to Burp Intruder. This enables you to automatically pause an attack when a specified expression appears in or is missing from a response. This reduces memory use when running a large attack and helps you focus on relevant responses.

Automatic Content-Length mismatch highlighting in HTTP responses

Burp now automatically highlights the Content-Length response header when the declared length doesn't match the actual response body size. This can help you more quickly identify vulnerabilities such as HTTP request smuggling.

Export and manage Collaborator interactions

You can now export Collaborator interactions as CSV files. This enables you to more easily include interaction data in proof-of-concept demonstrations and reports.

In addition, you can now mark Collaborator interactions as read, helping you visually separate reviewed data from new activity and focus on the most recent interactions.

Bug fixes

We've fixed the following bugs:

An issue where the Home and End keys caused the cursor to jump to incorrect lines in the message editor under certain conditions.

An issue where Burp Logger's view filter wasn't reapplied correctly after reaching the capture limit, causing the display of entries that didn't match the active filter.

A bug where newly saved configurations weren't visible in the configuration library until restarting Burp.

A bug where payload encoding characters weren't copied correctly when creating a new Intruder tab with Payload encoding disabled.

A bug where the Add notes hotkey didn't function in Burp Organizer or Burp Repeater.

An issue where using Ctrl+C to copy text in the BCheck preview screen did not work on Linux and Windows.

An issue where loading multiple extensions could cause extension-provided tabs to disappear or fail to load, particularly when loading extensions with WebSocket message editor implementations.

Browser upgrade

We've upgraded Burp's browser to Chromium 133.0.6943.54 for Windows & Mac and 133.0.6943.53 for Linux. For more information, see the Chrome for Developers release notes.
