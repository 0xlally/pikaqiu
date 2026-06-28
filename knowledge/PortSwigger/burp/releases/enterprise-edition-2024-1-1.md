# Enterprise Edition 2024.1.1

Source: https://portswigger.net/burp/releases/enterprise-edition-2024-1-1
Fetched: 2026-06-28T09:16:19.897233+00:00

This release upgrades Burp Scanner to version 2023.12.1.3, which introduces a new scan check for broken access control vulnerabilities, as well as a number of other improvements.

New scan check: Broken access control

We've added an experimental new scan check for broken access control vulnerabilities.

While we refine it to reduce the number of false positives it generates, we've disabled this check when using Normal audit accuracy. To try it out, from your audit configuration, go to Audit optimization > Audit accuracy and select Minimize false negatives. We welcome any feedback.

If you want to learn more about broken access control vulnerabilities, check out the Access control topic on the Web Security Academy.

Other improvements

We've added some other improvements to Burp Scanner, including:

Scanner now automatically generates logical examples for path parameters when scanning open API specifications, meaning fewer pages are missed during the audit.

Scanner now manages memory usage much more efficiently during the audit phase of browser-powered scans.

Scanner is now able to submit requests that match the Content-Type of non-standard JSON endpoints, for example, application/json-patch+json or application/*+json.

Scanner can now send arrays as query string parameters when scanning an OpenAPI schema. This enables it to find more endpoints.

Scanner is now better able to identify - and disregard - duplicate items in different areas of your application during scans. This helps to reduce the time it takes for scans to complete.

Browser upgrade

We have upgraded the browser used for scanning to Chromium 121.0.6167.85 for Mac and Linux and 121.0.6167.85/.86 for Windows. For more information, see the Chromium release notes.
