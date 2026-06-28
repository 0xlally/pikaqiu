# Credit card numbers disclosed

Source: https://portswigger.net/kb/issues/00600500_credit-card-numbers-disclosed
Fetched: 2026-06-28T09:17:16.747254+00:00

Support Center

Issue Definitions

Credit card numbers disclosed

Credit card numbers disclosed

Twitter

WhatsApp

Facebook

Reddit

LinkedIn

Email

Description: Credit card numbers disclosed

Applications sometimes disclose sensitive financial information such as credit card numbers. Responses containing credit card numbers may not represent any security vulnerability - for example, a number may belong to the logged-in user to whom it is displayed. If a credit card number is identified during a security assessment it should be verified, then application logic reviewed to identify whether its disclosure within the application is necessary and appropriate.

References

Web Security Academy: Information disclosure

Vulnerability classifications

CWE-200: Information Exposure

CWE-388: Error Handling

CAPEC-37: Retrieve Embedded Sensitive Data

Typical severity

Information

Type index (hex)

0x00600500

Type index (decimal)

6292736

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
