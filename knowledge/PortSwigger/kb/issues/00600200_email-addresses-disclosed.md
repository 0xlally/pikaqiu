# Email addresses disclosed

Source: https://portswigger.net/kb/issues/00600200_email-addresses-disclosed
Fetched: 2026-06-28T09:17:16.601931+00:00

Support Center

Issue Definitions

Email addresses disclosed

Email addresses disclosed

Twitter

WhatsApp

Facebook

Reddit

LinkedIn

Email

Description: Email addresses disclosed

The presence of email addresses within application responses does not necessarily constitute a security vulnerability. Email addresses may appear intentionally within contact information, and many applications (such as web mail) include arbitrary third-party email addresses within their core content.

However, email addresses of developers and other individuals (whether appearing on-screen or hidden within page source) may disclose information that is useful to an attacker; for example, they may represent usernames that can be used at the application's login, and they may be used in social engineering attacks against the organization's personnel. Unnecessary or excessive disclosure of email addresses may also lead to an increase in the volume of spam email received.

Remediation: Email addresses disclosed

Consider removing any email addresses that are unnecessary, or replacing personal addresses with anonymous mailbox addresses (such as helpdesk@example.com).

To reduce the quantity of spam sent to anonymous mailbox addresses, consider hiding the email address and instead providing a form that generates the email server-side, protected by a CAPTCHA if necessary.

References

Web Security Academy: Information disclosure

Vulnerability classifications

CWE-200: Information Exposure

CAPEC-37: Retrieve Embedded Sensitive Data

Typical severity

Information

Type index (hex)

0x00600200

Type index (decimal)

6291968

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
