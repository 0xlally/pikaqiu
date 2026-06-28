# Serialized object in HTTP message

Source: https://portswigger.net/kb/issues/00400900_serialized-object-in-http-message
Fetched: 2026-06-28T09:17:11.907752+00:00

Support Center

Issue Definitions

Serialized object in HTTP message

Serialized object in HTTP message

Twitter

WhatsApp

Facebook

Reddit

LinkedIn

Email

Description: Serialized object in HTTP message

Applications may submit a serialized object in a request parameter. This behavior can expose the application in various ways, including:

Any sensitive data contained within the object can be viewed by the user.

An attacker may be able to interfere with server-side logic by tampering with the contents of the object and re-serializing it.

An attacker may be able to cause unauthorized code execution on the server, by controlling the server-side function that is invoked when the object is processed.

Actual exploitation of any code execution vulnerabilities arising from the application's use of serialized objects will typically require the attacker to have access to the source code of the server-side application. This may mitigate the practical impact of this issue in many situations. However, it is still highly recommended to fix the underlying vulnerability. Vulnerabilities in native deserialization functions often allow practical exploitation without source code access.

Remediation: Serialized object in HTTP message

The best way to avoid vulnerabilities that arise from the use of serialized objects is not to pass these in request parameters, or expose them in any other way to the client. Generally, it is possible to transmit application data in plain non-serialized form, and handle it with the same precautions that apply to all client-submitted data. If it is considered unavoidable to place serialized objects into request parameters, then it may be possible to prevent attacks by also placing a server-generated cryptographic signature of the object into the same request, and validating the signature before performing deserialization or other processing on the object.

References

Web Security Academy: Insecure deserialization

Vulnerability classifications

CWE-502: Deserialization of Untrusted Data

CAPEC-586: Object Injection

Typical severity

High

Type index (hex)

0x00400900

Type index (decimal)

4196608

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
