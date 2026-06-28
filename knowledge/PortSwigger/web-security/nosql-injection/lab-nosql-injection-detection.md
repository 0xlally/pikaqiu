# Lab: Detecting NoSQL injection

Source: https://portswigger.net/web-security/nosql-injection/lab-nosql-injection-detection
Fetched: 2026-06-28T09:17:59.390270+00:00

Web Security Academy

NoSQL injection

Lab

Lab: Detecting NoSQL injection

The product category filter for this lab is powered by a MongoDB NoSQL database. It is vulnerable to NoSQL injection.

To solve the lab, perform a NoSQL injection attack that causes the application to display unreleased products.

Solution

In Burp's browser, access the lab and click on a product category filter.

In Burp, go to Proxy > HTTP history. Right-click the category filter request and select Send to Repeater.

In Repeater, submit a ' character in the category parameter. Notice that this causes a JavaScript syntax error. This may indicate that the user input was not filtered or sanitized correctly.

Submit a valid JavaScript payload in the value of the category query parameter. You could use the following payload:

Gifts'+'

Make sure to URL-encode the payload by highlighting it and using the Ctrl-U hotkey. Notice that it doesn't cause a syntax error. This indicates that a form of server-side injection may be occurring.

Identify whether you can inject boolean conditions to change the response:

Insert a false condition in the category parameter. For example:

Gifts' && 0 && 'x

Make sure to URL-encode the payload. Notice that no products are retrieved.

Insert a true condition in the category parameter. For example:

Gifts' && 1 && 'x

Make sure to URL-encode the payload. Notice that products in the Gifts category are retrieved.

Submit a boolean condition that always evaluates to true in the category parameter. For example:

Gifts'||1||'

Right-click the response and select Show response in browser.

Copy the URL and load it in Burp's browser. Verify that the response now contains unreleased products. The lab is solved.

Community solutions

Popo Hack

Find NoSQL injection vulnerabilities using Burp Suite

Try for free
