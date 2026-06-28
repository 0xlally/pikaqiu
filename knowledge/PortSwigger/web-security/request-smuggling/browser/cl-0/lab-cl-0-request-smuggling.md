# Lab: CL.0 request smuggling

Source: https://portswigger.net/web-security/request-smuggling/browser/cl-0/lab-cl-0-request-smuggling
Fetched: 2026-06-28T09:18:00.925606+00:00

Web Security Academy

Request smuggling

Browser-powered

CL.0 request smuggling

Lab

Lab: CL.0 request smuggling

This lab is vulnerable to CL.0 request smuggling attacks. The back-end server ignores the Content-Length header on requests to some endpoints.

To solve the lab, identify a vulnerable endpoint, smuggle a request to the back-end to access to the admin panel at /admin, then delete the user carlos.

This lab is based on real-world vulnerabilities discovered by PortSwigger Research. For more details, check out Browser-Powered Desync Attacks: A New Frontier in HTTP Request Smuggling.

Solution

Probe for vulnerable endpoints

From the Proxy > HTTP history, send the GET / request to Burp Repeater twice.

In Burp Repeater, add both of these tabs to a new group.

Go to the first request and convert it to a POST request (right-click and select Change request method).

In the body, add an arbitrary request smuggling prefix. The result should look something like this:

POST / HTTP/1.1

Host: YOUR-LAB-ID.web-security-academy.net

Cookie: session=YOUR-SESSION-COOKIE

Connection: close

Content-Type: application/x-www-form-urlencoded

Content-Length: CORRECT

GET /hopefully404 HTTP/1.1

Foo: x

Change the path of the main POST request to point to an arbitrary endpoint that you want to test.

Using the drop-down menu next to the Send button, change the send mode to Send group in sequence (single connection).

Change the Connection header of the first request to keep-alive.

Send the sequence and check the responses.

If the server responds to the second request as normal, this endpoint is not vulnerable.

If the response to the second request matches what you expected from the smuggled prefix (in this case, a 404 response), this indicates that the back-end server is ignoring the Content-Length of requests.

Deduce that you can use requests for static files under /resources, such as /resources/images/blog.svg, to cause a CL.0 desync.

Exploit

In Burp Repeater, change the path of your smuggled prefix to point to /admin.

Send the requests in sequence again and observe that the second request has successfully accessed the admin panel.

Smuggle a request to GET /admin/delete?username=carlos request to solve the lab.

POST /resources/images/blog.svg HTTP/1.1

Host: YOUR-LAB-ID.web-security-academy.net

Cookie: session=YOUR-SESSION-COOKIE

Connection: keep-alive

Content-Length: CORRECT

GET /admin/delete?username=carlos HTTP/1.1

Foo: x

Community solutions

Jarno Timmermans

Find HTTP request smuggling vulnerabilities using Burp Suite

Try for free
