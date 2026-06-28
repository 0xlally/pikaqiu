# SMTP header injection

Source: https://portswigger.net/kb/issues/00200800_smtp-header-injection
Fetched: 2026-06-28T09:17:10.487245+00:00

Support Center

Issue Definitions

SMTP header injection

SMTP header injection

Twitter

WhatsApp

Facebook

Reddit

LinkedIn

Email

Description: SMTP header injection

SMTP header injection vulnerabilities arise when user input is placed into email headers without adequate sanitization, allowing an attacker to inject additional headers with arbitrary values. This behavior can be exploited to send copies of emails to third parties, attach viruses, deliver phishing attacks, and often alter the content of emails. It is typically exploited by spammers looking to leverage the vulnerable company's reputation to add legitimacy to their emails.

This issue is particularly serious if the email contains sensitive information not intended for the attacker, such as a password reset token.

Remediation: SMTP header injection

Validate that user input conforms to a whitelist of safe characters before placing it into email headers. In particular, input containing newlines and carriage returns should be rejected. Alternatively, consider switching to an email library that automatically prevents such attacks.

References

Burp Collaborator

Vulnerability classifications

CWE-93: Improper Neutralization of CRLF Sequences ('CRLF Injection')

CWE-159: Failure to Sanitize Special Element

CAPEC-183: IMAP/SMTP Command Injection

Typical severity

Medium

Type index (hex)

0x00200800

Type index (decimal)

2099200

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
