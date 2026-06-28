# Professional / Community 2023.1.1

Source: https://portswigger.net/burp/releases/professional-community-2023-1-1
Fetched: 2026-06-28T09:16:39.668015+00:00

This release introduces improvements to authenticated crawling, as well as a number of minor improvements and bug fixes.

Improvements to Burp Scanner

This release includes several minor improvements to authenticated crawling with popup-based login mechanisms:

We have added a wait after the final event in a recorded sequence. This means that the sequence now captures links that are added by the final page after a delay.

When you login after receiving a temporary failure status code, Burp now authenticates subsequent requests for the same resource.

When you change the Await navigation timeout in a crawler configuration, it now automatically updates in the recorded login sequence replayer. It is also stored in the crawler tuning.

Bug Fixes

We have released a couple of bug fixes related to the Montoya API:

Previously, the Javadoc incorrectly stated that the passiveAudit() method of the ScanCheck interface returns null if no issues are identified. The method in fact returns an empty AuditResult object if no issues are identified. We have updated the Javadoc.

We have fixed a bug whereby the copyToTempFile method in HttpRequestResponse was causing null pointer exceptions.

Browser upgrade

This release upgrades Burp's browser to Chromium 109.0.5414.119/.120.
