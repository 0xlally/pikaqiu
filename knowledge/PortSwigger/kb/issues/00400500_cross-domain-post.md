# Cross-domain POST

Source: https://portswigger.net/kb/issues/00400500_cross-domain-post
Fetched: 2026-06-28T09:17:12.331351+00:00

Support Center

Issue Definitions

Cross-domain POST

Cross-domain POST

Twitter

WhatsApp

Facebook

Reddit

LinkedIn

Email

Description: Cross-domain POST

Applications sometimes use POST requests to transfer sensitive information from one domain to another. This does not necessarily constitute a security vulnerability, but it creates a trust relationship between the two domains. Data transmitted between domains should be reviewed to determine whether the originating application should be trusting the receiving domain with this information.

Vulnerability classifications

CWE-16: Configuration

Typical severity

Information

Type index (hex)

0x00400500

Type index (decimal)

4195584

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
