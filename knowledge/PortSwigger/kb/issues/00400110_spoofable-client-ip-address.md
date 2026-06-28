# Spoofable client IP address

Source: https://portswigger.net/kb/issues/00400110_spoofable-client-ip-address
Fetched: 2026-06-28T09:17:11.467368+00:00

Support Center

Issue Definitions

Spoofable client IP address

Spoofable client IP address

Twitter

WhatsApp

Facebook

Reddit

LinkedIn

Email

Description: Spoofable client IP address

If an application trusts an HTTP request header like X-Forwarded-For to accurately specify the remote IP address of the connecting client, then malicious clients can spoof their IP address. This behavior does not necessarily constitute a security vulnerability, however some applications use client IP addresses to enforce access controls and rate limits. For example, an application might expose administrative functionality only to clients connecting from the local IP address of the server, or allow a certain number of failed login attempts from each unique IP address. Consider reviewing relevant functionality to determine whether this might be the case.

Remediation: Spoofable client IP address

HTTP request headers such as X-Forwarded-For, True-Client-IP, and X-Real-IP are not a robust foundation on which to build any security measures, such as access controls. Any such measures should be replaced with more secure alternatives that are not vulnerable to spoofing.

If the platform application server returns incorrect information about the client's IP address due to the presence of any particular HTTP request header, then the server may need to be reconfigured, or an alternative method of identifying clients should be used.

Vulnerability classifications

CWE-16: Configuration

Typical severity

Information

Type index (hex)

0x00400110

Type index (decimal)

4194576

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
