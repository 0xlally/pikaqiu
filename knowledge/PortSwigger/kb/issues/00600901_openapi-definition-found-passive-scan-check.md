# OpenAPI definition found (passive scan check)

Source: https://portswigger.net/kb/issues/00600901_openapi-definition-found-passive-scan-check
Fetched: 2026-06-28T09:17:17.129123+00:00

Support Center

Issue Definitions

OpenAPI definition found (passive scan check)

OpenAPI definition found (passive scan check)

Twitter

WhatsApp

Facebook

Reddit

LinkedIn

Email

Description: OpenAPI definition found (passive scan check)

A publicly available OpenAPI definition was found.

An OpenAPI definition describes the structure of an HTTP-based API in YAML or JSON format, according to the OpenAPI specification. It enables humans to discover and understand the service's capabilities, and is also designed to be processed by software for automating tasks like API integration and validation.

A publicly-available OpenAPI definition does not necessarily present a security vulnerability. However, the API definition can be valuable to attackers as it may include information about the API structure, potentially enabling targeted attacks. For example it may include detailed explanations, examples, and usage scenarios.

Remediation: OpenAPI definition found (passive scan check)

Make sure that your API documentation only contains necessary information before you deploy it to production. This prevents attackers from using the definition to discover details about the API's available operations and other potentially sensitive information, including administrative functions.

References

Web Security Academy: Identifying API endpoints

Vulnerability classifications

CWE-200: Information Exposure

Typical severity

Information

Type index (hex)

0x00600901

Type index (decimal)

6293761

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
