# Professional / Community 2026.6

Source: https://portswigger.net/burp/releases/professional-community-2026-6
Fetched: 2026-06-28T09:16:57.127882+00:00

This release updates the bundled Java runtime to Java 26. It also includes improvements to Burp Scanner and a range of bug fixes.

Bug fixes

We've fixed the following bugs:

An issue where generated per-host certificates had lifetimes exceeding current browser requirements. Certificate lifetimes are now limited to 199 days.

An issue where the Render tab would sometimes fail to render responses.

An issue where Decoder didn't preserve CRLF line endings when pasting content with Ctrl+V.

An issue where Intruder attack numbers skipped every other number instead of incrementing sequentially.

An issue where Collaborator settings didn't respect the user/project configuration scope.

An issue where closing a Bambda or Custom Action editor with unsaved changes would silently discard them. Burp now prompts before discarding.

An issue where hotkeys imported via the Settings > User interface > Hotkeys settings cog weren't saved correctly.

An issue where scope rules generated from URLs didn't correctly escape regular-expression metacharacters.

An issue where long words didn't soft-wrap in the Markdown notes editor.

Burp Scanner

We've made the following improvements and bug fixes to Burp Scanner:

The Cross-Domain Referer Leakage check now honours per-element referrerpolicy attributes, reducing false positives.

Configured custom headers are now applied when probing common endpoints.

URLs that differ only in cache-busting or session-token parameters are now de-duplicated, reducing noise and memory use during scans.

We've resolved several memory and resource leaks across crawl and audit, significantly improving stability for large scans.

We've fixed an issue in DOM Invader where sinks could disappear.

We've improved the scanner's ability to replay recorded logins that have many requests.

Java update

We've updated Burp's Java version to Java 26 (26.0.1).

Browser upgrade

We've upgraded Burp's browser to Chromium 149.0.7827.103 for Windows & Mac and 149.0.7827.102 for Linux. For more information, see the Chromium release notes.
