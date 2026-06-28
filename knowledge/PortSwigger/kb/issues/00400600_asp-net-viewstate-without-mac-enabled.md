# ASP.NET ViewState without MAC enabled

Source: https://portswigger.net/kb/issues/00400600_asp-net-viewstate-without-mac-enabled
Fetched: 2026-06-28T09:17:11.880406+00:00

Support Center

Issue Definitions

ASP.NET ViewState without MAC enabled

ASP.NET ViewState without MAC enabled

Twitter

WhatsApp

Facebook

Reddit

LinkedIn

Email

Description: ASP.NET ViewState without MAC enabled

The ViewState is a mechanism built in to the ASP.NET platform for persisting elements of the user interface and other data across successive requests. The data to be persisted is serialized by the server and transmitted via a hidden form field. When it is posted back to the server, the ViewState parameter is deserialized and the data is retrieved.

By default, the serialized value is signed by the server to prevent tampering by the user; however, this behavior can be disabled by setting the Page.EnableViewStateMac property to false. If this is done, then an attacker can modify the contents of the ViewState and cause arbitrary data to be deserialized and processed by the server. An attacker may be able to execute arbitrary code on the server by supplying a gadget chain. Also, if the ViewState contains any items that are critical to the server's processing of the request, then this may result in a direct security exposure.

You should try to identify a valid gadget chain to take control of the server and, failing that, review the contents of the ViewState to determine whether it contains any critical items that can be manipulated to attack the application.

Remediation: ASP.NET ViewState without MAC enabled

There is no good reason to disable the default ASP.NET behavior in which the ViewState is signed to prevent tampering. To ensure that this occurs, you should set the Page.EnableViewStateMac property to true on any pages where the ViewState is not currently signed.

References

Exploiting Deserialisation in ASP.NET via ViewState

Web Security Academy: Insecure deserialization

Vulnerability classifications

CWE-642: External Control of Critical State Data

CAPEC-586: Object Injection

Typical severity

High

Type index (hex)

0x00400600

Type index (decimal)

4195840

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
