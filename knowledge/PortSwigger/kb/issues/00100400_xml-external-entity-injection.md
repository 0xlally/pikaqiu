# XML external entity injection

Source: https://portswigger.net/kb/issues/00100400_xml-external-entity-injection
Fetched: 2026-06-28T09:17:05.080025+00:00

Support Center

Issue Definitions

XML external entity injection

XML external entity injection

Twitter

WhatsApp

Facebook

Reddit

LinkedIn

Email

Description: XML external entity injection

XML external entity (XXE) injection vulnerabilities arise when applications process user-supplied XML documents without disabling references to external resources. XML parsers typically support external references by default, even though they are rarely required by applications during normal usage.

External entities can reference files on the parser's filesystem; exploiting this feature may allow retrieval of arbitrary files, or denial of service by causing the server to read from a file such as /dev/random.

External entities can often also reference network resources via the HTTP protocol handler. The ability to send requests to other systems can allow the vulnerable server to be used as an attack proxy. By submitting suitable payloads, an attacker can cause the application server to attack other systems that it can interact with. This may include public third-party systems, internal systems within the same organization, or services available on the local loopback adapter of the application server itself. Depending on the network architecture, this may expose highly vulnerable internal services that are not otherwise accessible to external attackers.

Remediation: XML external entity injection

Parsers that are used to process XML from untrusted sources should be configured to disable processing of all external resources. This is usually possible, and will prevent a number of related attacks. You should consult the documentation for your XML parsing library to determine how to achieve this.

XML external entity injection makes use of the DOCTYPE tag to define the injected entity. It may also be possible to disable the DOCTYPE tag or use input validation to block input containing it.

References

Web Security Academy: XXE injection

Vulnerability classifications

CWE-611: Improper Restriction of XML External Entity Reference ('XXE')

CAPEC-228: DTD Injection

Typical severity

High

Type index (hex)

0x00100400

Type index (decimal)

1049600

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
