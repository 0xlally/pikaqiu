# Private IP addresses disclosed

Source: https://portswigger.net/kb/issues/00600300_private-ip-addresses-disclosed
Fetched: 2026-06-28T09:17:16.471580+00:00

Support Center

Issue Definitions

Private IP addresses disclosed

Private IP addresses disclosed

Twitter

WhatsApp

Facebook

Reddit

LinkedIn

Email

Description: Private IP addresses disclosed

RFC 1918 specifies ranges of IP addresses that are reserved for use in private networks and cannot be routed on the public Internet. Although various methods exist by which an attacker can determine the public IP addresses in use by an organization, the private addresses used internally cannot usually be determined in the same ways.

Discovering the private addresses used within an organization can help an attacker in carrying out network-layer attacks aiming to penetrate the organization's internal infrastructure.

Remediation: Private IP addresses disclosed

There is not usually any good reason to disclose the internal IP addresses used within an organization's infrastructure. If these are being returned in service banners or debug messages, then the relevant services should be configured to mask the private addresses. If they are being used to track back-end servers for load balancing purposes, then the addresses should be rewritten with innocuous identifiers from which an attacker cannot infer any useful information about the infrastructure.

References

Web Security Academy: Information disclosure

Vulnerability classifications

CWE-200: Information Exposure

CAPEC-37: Retrieve Embedded Sensitive Data

Typical severity

Information

Type index (hex)

0x00600300

Type index (decimal)

6292224

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
