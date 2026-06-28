# XML injection

Source: https://portswigger.net/kb/issues/00100700_xml-injection
Fetched: 2026-06-28T09:17:05.310489+00:00

Support Center

Issue Definitions

XML injection

XML injection

Twitter

WhatsApp

Facebook

Reddit

LinkedIn

Email

Description: XML injection

XML or SOAP injection vulnerabilities arise when user input is inserted into a server-side XML document or SOAP message in an unsafe way. It may be possible to use XML metacharacters to modify the structure of the resulting XML. Depending on the function in which the XML is used, it may be possible to interfere with the application's logic, to perform unauthorized actions or access sensitive data.

This kind of vulnerability can be difficult to detect and exploit remotely; you should review the application's response, and the purpose that the relevant input performs within the application's functionality, to determine whether it is indeed vulnerable.

Remediation: XML injection

The application should validate or sanitize user input before incorporating it into an XML document or SOAP message. It may be possible to block any input containing XML metacharacters such as < and >. Alternatively, these characters can be replaced with the corresponding entities: &lt; and &gt;.

References

Web Security Academy: XXE injection

Vulnerability classifications

CWE-91: XML Injection (aka Blind XPath Injection)

CWE-116: Improper Encoding or Escaping of Output

CWE-159: Failure to Sanitize Special Element

CWE-611: Improper Restriction of XML External Entity Reference ('XXE')

CWE-776: Improper Restriction of Recursive Entity References in DTDs ('XML Entity Expansion')

CAPEC-250: XML Injection

Typical severity

Medium

Type index (hex)

0x00100700

Type index (decimal)

1050368

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
