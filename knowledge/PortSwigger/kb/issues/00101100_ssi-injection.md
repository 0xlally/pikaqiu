# SSI injection

Source: https://portswigger.net/kb/issues/00101100_ssi-injection
Fetched: 2026-06-28T09:17:06.640568+00:00

Support Center

Issue Definitions

SSI injection

SSI injection

Twitter

WhatsApp

Facebook

Reddit

LinkedIn

Email

Description: SSI injection

Server-Side Include (SSI) injection vulnerabilities arise when an application incorporates user-controllable data into response that is then parsed for Server-Side Include directives. If the data is not strictly validated, an attacker can modify or inject directives to carry out malicious actions.

SSI injection vulnerabilities can typically be exploited to inject arbitrary content, including JavaScript, into the application's response, with the same impact as cross-site scripting. Depending on the server configuration, it may also be possible to read protected files, or perform arbitrary code execution on the server, with the same impact as OS command injection.

Remediation: SSI injection

If possible, applications should avoid incorporating user-controllable data into pages that are processed for SSI directives. In almost every situation, there are safer alternative methods of implementing the required functionality. If this is not considered feasible, then the data should be strictly validated. Ideally, a whitelist of specific accepted values should be used. Otherwise, only short alphanumeric strings should be accepted. Input containing any other data, including any conceivable SSI metacharacter, should be rejected.

References

Introduction to Server-Side Includes

Vulnerability classifications

CWE-96: Improper Neutralization of Directives in Statically Saved Code ('Static Code Injection')

CWE-116: Improper Encoding or Escaping of Output

CWE-159: Failure to Sanitize Special Element

CAPEC-101: Server Side Include (SSI) Injection

Typical severity

High

Type index (hex)

0x00101100

Type index (decimal)

1052928

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
