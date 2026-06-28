# WebSocket URL poisoning (DOM-based)

Source: https://portswigger.net/kb/issues/00200340_websocket-url-poisoning-dom-based
Fetched: 2026-06-28T09:17:08.717942+00:00

Support Center

Issue Definitions

WebSocket URL poisoning (DOM-based)

WebSocket URL poisoning (DOM-based)

Twitter

WhatsApp

Facebook

Reddit

LinkedIn

Email

Description: WebSocket URL poisoning (DOM-based)

DOM-based vulnerabilities arise when a client-side script reads data from a controllable part of the DOM (for example, the URL) and processes this data in an unsafe way.

WebSocket URL poisoning occurs when a script uses controllable data as the target URL of a WebSocket connection. An attacker may be able to use the vulnerability to construct a URL that, if visited by another application user, will cause the user's browser to open a WebSocket connection to a URL that is under the attacker's control.

The potential impact of the vulnerability depends on the application's usage of WebSockets. If the application transmits sensitive data from the user's browser to the WebSocket server, then the attacker may be able to capture this data. If the application reads data from the WebSocket server and performs processing on this data, then the attacker may be able to subvert the application's logic or deliver additional client-side attacks against the user.

Burp Suite automatically identifies this issue using dynamic and static code analysis. Static analysis can lead to false positives that are not actually exploitable. If Burp Scanner has not provided any evidence resulting from dynamic analysis, you should review the relevant code and execution paths to determine whether this vulnerability is indeed present, or whether mitigations are in place that would prevent exploitation.

Remediation: WebSocket URL poisoning (DOM-based)

The most effective way to avoid DOM-based WebSocket URL poisoning vulnerabilities is not to dynamically set the target URL of a WebSocket connection using data that originated from any untrusted source. If the desired functionality of the application means that this behavior is unavoidable, then defenses must be implemented within the client-side code to prevent malicious data from introducing an arbitrary URL as a target of a WebSocket. In general, this is best achieved by using a whitelist of URLs that are permitted WebSocket targets, and strictly validating the target against this list before creating the WebSocket.

References

Web Security Academy: WebSocket URL poisoning (DOM-based)

Vulnerability classifications

CWE-345: Insufficient Verification of Data Authenticity

CWE-346: Origin Validation Error

CWE-441: Unintended Proxy or Intermediary ('Confused Deputy')

Typical severity

High

Type index (hex)

0x00200340

Type index (decimal)

2097984

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
