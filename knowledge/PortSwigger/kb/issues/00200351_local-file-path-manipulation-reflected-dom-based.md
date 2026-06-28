# Local file path manipulation (reflected DOM-based)

Source: https://portswigger.net/kb/issues/00200351_local-file-path-manipulation-reflected-dom-based
Fetched: 2026-06-28T09:17:08.506361+00:00

Support Center

Issue Definitions

Local file path manipulation (reflected DOM-based)

Local file path manipulation (reflected DOM-based)

Twitter

WhatsApp

Facebook

Reddit

LinkedIn

Email

Description: Local file path manipulation (reflected DOM-based)

Reflected DOM-based vulnerabilities arise when data is copied from a request and echoed into the application's immediate response within a part of the DOM that is then processed in an unsafe way by a client-side script. An attacker can leverage the reflection to control a part of the response (for example, a JavaScript string) that can be used to trigger the DOM-based vulnerability.

Local file path manipulation arises when a script uses controllable data as the filename parameter to a file handling API. An attacker may be able to use the vulnerability to construct a URL that, if visited by another application user, will cause the user's browser to open an arbitrary local file.

The potential impact of the vulnerability depends on the application's usage of the opened file. If the application reads data from the file, then the attacker may be able to retrieve this data. If the application writes data to the file, then the attacker may be able to write specific data to a sensitive file, such as an operating system configuration file. In both these cases, the actual exploitability of the potential vulnerability may depend on other suitable functionality being present in the application.

Burp Suite automatically identifies this issue using dynamic and static code analysis. Static analysis can lead to false positives that are not actually exploitable. If Burp Scanner has not provided any evidence resulting from dynamic analysis, you should review the relevant code and execution paths to determine whether this vulnerability is indeed present, or whether mitigations are in place that would prevent exploitation.

Remediation: Local file path manipulation (reflected DOM-based)

The most effective way to avoid DOM-based local file path manipulation vulnerabilities is not to dynamically pass a filename to a file handling API using data that originated from any untrusted source. If the desired functionality of the application means that this behavior is unavoidable, then defenses must be implemented within the client-side code to prevent malicious data from accessing arbitrary files. In general, this is best achieved by using a whitelist of permitted filenames, and strictly validating the filename against this list before invoking the file handling API.

References

Web Security Academy: Local file path manipulation (DOM-based)

Vulnerability classifications

CWE-22: Improper Limitation of a Pathname to a Restricted Directory ('Path Traversal')

CWE-73: External Control of File Name or Path

CAPEC-126: Path Traversal

Typical severity

High

Type index (hex)

0x00200351

Type index (decimal)

2098001

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
