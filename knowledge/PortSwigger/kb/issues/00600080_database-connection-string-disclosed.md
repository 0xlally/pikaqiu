# Database connection string disclosed

Source: https://portswigger.net/kb/issues/00600080_database-connection-string-disclosed
Fetched: 2026-06-28T09:17:16.424486+00:00

Support Center

Issue Definitions

Database connection string disclosed

Database connection string disclosed

Twitter

WhatsApp

Facebook

Reddit

LinkedIn

Email

Description: Database connection string disclosed

A database connection string specifies information about a data source and the means of connecting to it. In web applications, connection strings are generally used by the application tier to connect to the back database used for storing application data. They are usually read from server-side configuration files or hard-coded into application source code.

Remediation: Database connection string disclosed

It is almost never necessary for applications to disclose database connection strings to clients. The reason for the disclosure should be reviewed and addressed.

References

Web Security Academy: Information disclosure

Vulnerability classifications

CWE-15: External Control of System or Configuration Setting

CWE-497: Exposure of System Data to an Unauthorized Control Sphere

CAPEC-37: Retrieve Embedded Sensitive Data

Typical severity

Medium

Type index (hex)

0x00600080

Type index (decimal)

6291584

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
