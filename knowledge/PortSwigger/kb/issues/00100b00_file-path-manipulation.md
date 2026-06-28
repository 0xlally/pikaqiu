# File path manipulation

Source: https://portswigger.net/kb/issues/00100b00_file-path-manipulation
Fetched: 2026-06-28T09:17:05.729290+00:00

Support Center

Issue Definitions

File path manipulation

File path manipulation

Twitter

WhatsApp

Facebook

Reddit

LinkedIn

Email

Description: File path manipulation

File path manipulation vulnerabilities arise when user-controllable data is placed into a file or URL path that is used on the server to access local resources, which may be within or outside the web root. If vulnerable, an attacker can modify the file path to access different resources, which may contain sensitive information. Even where an attack is constrained within the web root, it is often possible to retrieve items that are normally protected from direct access, such as application configuration files, the source code for server-executable scripts, or files with extensions that the web server is not configured to serve directly.

Remediation: File path manipulation

Ideally, application functionality should be designed in such a way that user-controllable data does not need to be placed into file or URL paths in order to access local resources on the server. This can normally be achieved by referencing known files via an index number rather than their name.

If it is considered unavoidable to place user data into file or URL paths, the data should be strictly validated against a whitelist of accepted values. Note that when accessing resources within the web root, simply blocking input containing file path traversal sequences (such as dot-dot-slash) is not always sufficient to prevent retrieval of sensitive information, because some protected items may be accessible at the original path without using any traversal sequences.

References

Web Security Academy: Directory traversal

Vulnerability classifications

CWE-22: Improper Limitation of a Pathname to a Restricted Directory ('Path Traversal')

CWE-23: Relative Path Traversal

CWE-35: Path Traversal: '.../...//'

CWE-36: Absolute Path Traversal

CAPEC-126: Path Traversal

Typical severity

High

Type index (hex)

0x00100b00

Type index (decimal)

1051392

Twitter

WhatsApp

Facebook

Reddit

LinkedIn

Email

Burp Scanner

This issue - and many more like it - can be found using our

web vulnerability scanner

Read more

Get Burp

Scan your web application from just $499.00

Find out more
