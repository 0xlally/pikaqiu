# Form action hijacking (stored)

Source: https://portswigger.net/kb/issues/00501501_form-action-hijacking-stored
Fetched: 2026-06-28T09:17:17.098416+00:00

Support Center

Issue Definitions

Form action hijacking (stored)

Form action hijacking (stored)

Twitter

WhatsApp

Facebook

Reddit

LinkedIn

Email

Description: Form action hijacking (stored)

Form action hijacking vulnerabilities arise when an application places user-supplied input into the action URL of an HTML form. An attacker can use this vulnerability to construct a URL that, if visited by another application user, will modify the action URL of a form to point to the attacker's server. If a user submits the form then its contents, including any input from the victim user, will be delivered directly to the attacker.

Even if the user doesn't enter any sensitive information, the form may still deliver a valid CSRF token to the attacker, enabling them to perform CSRF attacks. In some cases web browsers may help exacerbate this issue by autocompleting forms with previously entered user input.

Stored form action hijacking vulnerabilities arise when the applicable input was submitted in an previous request and stored by the application.

Remediation: Form action hijacking (stored)

Consider hard-coding the form action URL, or implementing a whitelist of allowed values.

Vulnerability classifications

CWE-73: External Control of File Name or Path

CWE-20: Improper Input Validation

CAPEC-153: Input Data Manipulation

Typical severity

Medium

Type index (hex)

0x00501501

Type index (decimal)

5248257

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
