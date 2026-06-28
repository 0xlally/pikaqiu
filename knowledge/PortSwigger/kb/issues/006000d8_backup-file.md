# Backup file

Source: https://portswigger.net/kb/issues/006000d8_backup-file
Fetched: 2026-06-28T09:17:16.599603+00:00

Support Center

Issue Definitions

Backup file

Backup file

Twitter

WhatsApp

Facebook

Reddit

LinkedIn

Email

Description: Backup file

Publicly accessible backups and outdated copies of files can provide attackers with extra attack surface. Depending on the server configuration and file type, they may also expose source code, configuration details, and other information intended to remain secret.

Remediation: Backup file

Review the file to identify whether it's intended to be publicly accessible, and remove it from the server's web root if it isn't. It may also be worth auditing the server contents to find other outdated files, and taking measures to prevent the problem from reoccurring.

References

Web Security Academy: Information disclosure via backup files

Vulnerability classifications

CWE-530: Exposure of Backup File to an Unauthorized Control Sphere

CAPEC-37: Retrieve Embedded Sensitive Data

CAPEC-204: Lifting Sensitive Data Embedded in Cache

Typical severity

Information

Type index (hex)

0x006000d8

Type index (decimal)

6291672

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
