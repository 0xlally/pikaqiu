# Duplicate cookies set

Source: https://portswigger.net/kb/issues/00400a00_duplicate-cookies-set
Fetched: 2026-06-28T09:17:12.186030+00:00

Support Center

Issue Definitions

Duplicate cookies set

Duplicate cookies set

Twitter

WhatsApp

Facebook

Reddit

LinkedIn

Email

Description: Duplicate cookies set

The response contains two or more Set-Cookie headers that attempt to set the same cookie to different values. Browsers will only accept one of these values, typically the value in the last header. The presence of the duplicate headers may indicate a programming error.

Vulnerability classifications

CWE-16: Configuration

Typical severity

Information

Type index (hex)

0x00400a00

Type index (decimal)

4196864

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
