# Lab: Exploiting XInclude to retrieve files

Source: https://portswigger.net/web-security/xxe/lab-xinclude-attack
Fetched: 2026-06-28T09:18:07.120051+00:00

Web Security Academy

XXE injection

Lab

Lab: Exploiting XInclude to retrieve files

This lab has a "Check stock" feature that embeds the user input inside a server-side XML document that is subsequently parsed.

Because you don't control the entire XML document you can't define a DTD to launch a classic XXE attack.

To solve the lab, inject an XInclude statement to retrieve the contents of the /etc/passwd file.

Hint

By default, XInclude will try to parse the included document as XML. Since /etc/passwd isn't valid XML, you will need to add an extra attribute to the XInclude directive to change this behavior.

Solution

Visit a product page, click "Check stock", and intercept the resulting POST request in Burp Suite.

Set the value of the productId parameter to:

<foo xmlns:xi="http://www.w3.org/2001/XInclude"><xi:include parse="text" href="file:///etc/passwd"/></foo>

Community solutions

Garr_7

Michael Sommer (no audio)

Find XSS vulnerabilities using Burp Suite

Try for free
