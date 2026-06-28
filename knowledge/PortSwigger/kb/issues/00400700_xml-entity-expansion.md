# XML entity expansion

Source: https://portswigger.net/kb/issues/00400700_xml-entity-expansion
Fetched: 2026-06-28T09:17:11.841415+00:00

Support Center

Issue Definitions

XML entity expansion

XML entity expansion

Twitter

WhatsApp

Facebook

Reddit

LinkedIn

Email

Description: XML entity expansion

XML entity expansion vulnerabilities arise because the XML specification allows XML documents to define entities that reference other entities defined within the document. If this is done recursively to a significant depth, then the XML parser will consume exponentially increasing amounts of memory and processor resources as each level of recursion is processed. This might result in a denial-of-service condition, causing the entire application to stop functioning.

Note: To avoid causing an actual denial-of-service, Burp Suite merely verifies that entities are being recursively expanded to a modest depth. It is possible that reported applications are not actually vulnerable because they are designed to prevent entity expansion beyond a given depth.

Remediation: XML entity expansion

XML entity expansion makes use of the DOCTYPE tag to define the injected entities. XML parsers can usually be configured to disable support for this tag. You should consult the documentation for your XML parsing library to determine how to disable this feature.

It may also be possible to use input validation to block input containing a DOCTYPE tag.

References

Web Security Academy: XXE injection

Vulnerability classifications

CWE-776: Improper Restriction of Recursive Entity References in DTDs ('XML Entity Expansion')

CAPEC-197: XML Entity Expansion

Typical severity

Medium

Type index (hex)

0x00400700

Type index (decimal)

4196096

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
