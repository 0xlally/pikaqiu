# Professional 1.5.18

Source: https://portswigger.net/burp/releases/professional-1-5-18
Fetched: 2026-06-28T09:16:25.547813+00:00

This release includes a number of updates to the Scanner tool:

Several checks for new types of vulnerabilities have been added.

Various existing checks have been enhanced to improve their accuracy in avoiding false negatives and positives.

A number of bugs have been fixed.

The new types of issues that Burp can now report are:

Remote file inclusion

Recursive XML entity expansion

Response dependent on X-Forwarded-For header in request

"Long" redirection responses

Base64-encoded data within request parameters
