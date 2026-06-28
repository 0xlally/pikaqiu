# Testing for XXE injection vulnerabilities with Burp Suite

Source: https://portswigger.net/burp/documentation/desktop/testing-workflow/vulnerabilities/input-validation/xxe-injection/testing
Fetched: 2026-06-28T09:16:00.753226+00:00

Support Center

Documentation

Desktop editions

Testing workflow

Testing for vulnerabilities

Testing input validation

XXE injection

Testing for XXE injection vulnerabilities

ProfessionalCommunity Edition

Testing for XXE injection vulnerabilities with Burp Suite

Last updated:

June 18, 2026

Read time:

2 Minutes

XML external entity injection (also known as XXE) is a web security vulnerability that allows an attacker to interfere with an application's processing of XML data. It occurs when user input that contains a reference to an defined external entity is processed in an unsafe way on the server-side. This may mean that the application returns the value of the defined external entity within its responses.

You can use Burp to test for XXE injection vulnerabilities:

Professional Use Burp Scanner to automatically flag potential vulnerabilities.

Use Burp Repeater to manually test for vulnerabilities, or investigate any vulnerabilities further.

Steps

You can follow this process using a lab with an XXE injection vulnerability. For example, Exploiting XXE using external entities to retrieve files.

Scanning for XXE vulnerabilities

If you're using Burp Suite Professional, you can use Burp Scanner to test for XXE vulnerabilities:

Identify a request that contains XML that you want to investigate.

In Proxy > HTTP history, right-click the request and select Do active scan. Burp Scanner audits the request.

Review the Issues tab on the Dashboard to identify any XXE issues that Burp Scanner flags.

Manually testing for XXE vulnerabilities

You can also use Burp Repeater to test for XXE vulnerabilities. This process also enables you to exploit XXE vulnerabilities, and closely investigate any issues that Burp Scanner has identified:

In Proxy > HTTP history identify a request that contains XML that you want to

investigate.

Right-click the request and select Send to Repeater.

Go to the Repeater tab.

Insert an XXE payload into the XML string. The payload should define an XML entity and contain a

system identifier as a value. The system identifier could be, for example, a file path or URL. For

example, this payload defines the entity

&xxe; with a value of the /etc/passwd file:

<!DOCTYPE foo [<!ENTITY xxe SYSTEM "file:///etc/passwd"> ]>

Replace a data value in the XML with your defined XML entity.

Click Send.

Review the response to determine whether any data is returned. For example, look to see whether you can view the file or interact with any back-end systems.

Test additional XML data values by replacing a different data value in the XML with your defined XML entity.

Target other file paths or URLs by changing the system identifier value in your XXE payload.

Related pages

Burp Repeater

Academy: XML external entity (XXE) injection
