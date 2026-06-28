# Password field with autocomplete enabled

Source: https://portswigger.net/kb/issues/00500800_password-field-with-autocomplete-enabled
Fetched: 2026-06-28T09:17:13.234076+00:00

Support Center

Issue Definitions

Password field with autocomplete enabled

Password field with autocomplete enabled

Twitter

WhatsApp

Facebook

Reddit

LinkedIn

Email

Description: Password field with autocomplete enabled

Most browsers have a facility to remember user credentials that are entered into HTML forms. This function can be configured by the user and also by applications that employ user credentials. If the function is enabled, then credentials entered by the user are stored on their local computer and retrieved by the browser on future visits to the same application.

The stored credentials can be captured by an attacker who gains control over the user's computer. Further, an attacker who finds a separate application vulnerability such as cross-site scripting may be able to exploit this to retrieve a user's browser-stored credentials.

Remediation: Password field with autocomplete enabled

To prevent browsers from storing credentials entered into HTML forms, include the attribute autocomplete="off" within the FORM tag (to protect all form fields) or within the relevant INPUT tags (to protect specific individual fields).

Please note that modern web browsers may ignore this directive. In spite of this there is a chance that not disabling autocomplete may cause problems obtaining PCI compliance.

Vulnerability classifications

CWE-200: Information Exposure

Typical severity

Low

Type index (hex)

0x00500800

Type index (decimal)

5244928

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
