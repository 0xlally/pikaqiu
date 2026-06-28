# Professional 1.6.18

Source: https://portswigger.net/burp/releases/professional-1-6-18
Fetched: 2026-06-28T09:16:26.997040+00:00

This release updates the Scanner to enable it to find blind XML external entity (XXE) injection vulnerabilities. See today's blog post for more details.

The following bugs have been fixed:

A bug in the display of Scanner issues which prevented the configured font size from being correctly used.

A false negative in the detection of certain edge-case OS command injection vulnerabilities.

A bug in the Burp Proxy listeners options panel, which prevented newly added listeners from being correctly displayed.

Some performance improvements have been made to the Burp Collaborator server, and the metrics page now splits interaction counters into TCP and UDP interactions.
