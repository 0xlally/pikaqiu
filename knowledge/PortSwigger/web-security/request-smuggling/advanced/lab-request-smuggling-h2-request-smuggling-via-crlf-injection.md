# Lab: HTTP/2 request smuggling via CRLF injection

Source: https://portswigger.net/web-security/request-smuggling/advanced/lab-request-smuggling-h2-request-smuggling-via-crlf-injection
Fetched: 2026-06-28T09:18:00.314069+00:00

Web Security Academy

Request smuggling

Advanced

Lab

Lab: HTTP/2 request smuggling via CRLF injection

This lab is vulnerable to request smuggling because the front-end server downgrades HTTP/2 requests and fails to adequately sanitize incoming headers.

To solve the lab, use an HTTP/2-exclusive request smuggling vector to gain access to another user's account. The victim accesses the home page every 15 seconds.

If you're not familiar with Burp's exclusive features for HTTP/2 testing, please refer to the documentation for details on how to use them.

Hint

To inject newlines into HTTP/2 headers, use the Inspector to drill down into the header, then press the Shift + Return keys. Note that this feature is not available when you double-click on the header.

Hint

We covered some ways you can capture other users' requests via request smuggling in a previous lab.

Solution

In Burp's browser, use the lab's search function a couple of times and observe that the website records your recent search history. Send the most recent POST / request to Burp Repeater and remove your session cookie before resending the request. Notice that your search history is reset, confirming that it's tied to your session cookie.

Expand the Inspector's Request Attributes section and make sure the protocol is set to HTTP/2.

Using the Inspector, add an arbitrary header to the request. Append the sequence \r\n to the header's value, followed by the Transfer-Encoding: chunked header:

Name

foo

Value

bar\r\n

Transfer-Encoding: chunked

In the body, attempt to smuggle an arbitrary prefix as follows:

0

SMUGGLED

Observe that every second request you send receives a 404 response, confirming that you have caused the back-end to append the subsequent request to the smuggled prefix

Change the body of the request to the following:

0

POST / HTTP/1.1

Host: YOUR-LAB-ID.web-security-academy.net

Cookie: session=YOUR-SESSION-COOKIE

Content-Length: 800

search=x

Send the request, then immediately refresh the page in the browser. The next step depends on which response you receive:

If you got lucky with your timing, you may see a 404 Not Found response. In this case, refresh the page again and move on to the next step.

If you instead see the search results page, observe that the start of your request is reflected on the page because it was appended to the search=x parameter in the smuggled prefix. In this case, send the request again, but this time wait for 15 seconds before refreshing the page. If you see a 404 response, just refresh the page again.

Check the recent searches list. If it contains a GET request, this is the start of the victim user's request and includes their session cookie. If you instead see your own POST request, you refreshed the page too early. Try again until you have successfully stolen the victim's session cookie.

In Burp Repeater, send a request for the home page using the stolen session cookie to solve the lab.

Community solutions

Jarno Timmermans

InfoSec

Find HTTP request smuggling vulnerabilities using Burp Suite

Try for free
