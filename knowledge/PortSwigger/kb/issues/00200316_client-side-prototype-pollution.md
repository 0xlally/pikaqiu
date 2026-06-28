# Client-side prototype pollution

Source: https://portswigger.net/kb/issues/00200316_client-side-prototype-pollution
Fetched: 2026-06-28T09:17:07.215583+00:00

Support Center

Issue Definitions

Client-side prototype pollution

Client-side prototype pollution

Twitter

WhatsApp

Facebook

Reddit

LinkedIn

Email

Description: Client-side prototype pollution

A client-side prototype pollution source is any user-controlled JSON property, query string, or hash parameter that is converted to a JavaScript object and then merged with another object. This enables an attacker to use property keys, such as __proto__, to assign properties to the Object.prototype or other global prototypes.

Client-side prototype pollution is not a vulnerability in its own right. However, when paired with a gadget, this may lead to vulnerabilities such as DOM XSS, which could enable the attacker to control JavaScript on the page.

Remediation: Client-side prototype pollution

Ensure that property keys, such as __proto__, constructor, and prototype are correctly filtered when merging objects. When creating objects, we recommend using the Object.create(null) API to ensure that your object does not inherit from the Object.prototype and, therefore, won't be vulnerable to prototype pollution.

References

Testing for client-side prototype pollution in DOM Invader

Web Security Academy: Prototype pollution

Vulnerability classifications

CWE-1321: Improperly Controlled Modification of Object Prototype Attributes ('Prototype Pollution')

Typical severity

Information

Type index (hex)

0x00200316

Type index (decimal)

2097942

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
