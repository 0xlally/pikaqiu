# Professional 1.6.07

Source: https://portswigger.net/burp/releases/professional-1-6-07
Fetched: 2026-06-28T09:16:26.459241+00:00

This release contains various enhancements to the Scanner engine logic, to improve both the reliability of issue reporting, and the quality of proof-of-concept exploits. Improvements have been made to the following checks:

OS command injection

SQL injection

HTTP response header injection

File path traversal

Server-side JavaScript / NoSQL injection

Reflected cross-site scripting

Various DOM-based issues

Open redirection

Several other improvements have also been made, including:

The maximum number of active scan threads has been increased to 999.

A workaround has been applied to override a recent change in Java platform behavior which affected SSL negotiation with some servers.

A problem in which extension-initiated restoration of state could cause the configuration of the Extender tool to be reloaded, thereby interfering with the extension's own execution, has been resolved,

A "Start attack" button has been added to each configuration panel in the Intruder tool.

A bug in which multibyte characters are copied from the HTTP message viewer to the clipboard as raw bytes has been resolved.
