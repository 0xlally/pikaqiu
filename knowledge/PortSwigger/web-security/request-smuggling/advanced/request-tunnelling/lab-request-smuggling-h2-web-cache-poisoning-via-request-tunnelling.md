# Lab: Web cache poisoning via HTTP/2 request tunnelling

Source: https://portswigger.net/web-security/request-smuggling/advanced/request-tunnelling/lab-request-smuggling-h2-web-cache-poisoning-via-request-tunnelling
Fetched: 2026-06-28T09:18:00.338980+00:00

Web Security Academy

Request smuggling

Advanced

Request tunnelling

Lab

Lab: Web cache poisoning via HTTP/2 request tunnelling

This lab is vulnerable to request smuggling because the front-end server downgrades HTTP/2 requests and doesn't consistently sanitize incoming headers.

To solve the lab, poison the cache in such a way that when the victim visits the home page, their browser executes alert(1). A victim user will visit the home page every 15 seconds.

The front-end server doesn't reuse the connection to the back-end, so isn't vulnerable to classic request smuggling attacks. However, it is still vulnerable to request tunnelling.

Solution

Send a request for GET / to Burp Repeater. Expand the Inspector's Request Attributes section and make sure the protocol is set to HTTP/2.

Using the Inspector, try smuggling an arbitrary header in the :path pseudo-header, making sure to preserve a valid request line for the downgraded request as follows:

Name

:path

Value

/?cachebuster=1 HTTP/1.1\r\n

Foo: bar

Observe that you still receive a normal response, confirming that you're able to inject via the :path.

Change the request method to HEAD and use the :path pseudo-header to tunnel a request for another arbitrary endpoint as follows:

Name

:path

Value

/?cachebuster=2 HTTP/1.1\r\n

Host: YOUR-LAB-ID.web-security-academy.net\r\n

\r\n

GET /post?postId=1 HTTP/1.1\r\n

Foo: bar

Note that we've ensured that the main request is valid by including a Host header before the split. We've also left an arbitrary trailing header to capture the HTTP/1.1 suffix that will be appended to the request line by the front-end during rewriting.

Send the request and observe that you are able to view the tunnelled response. If you can't, try using a different postId.

Remove everything except the path and cachebuster query parameter from the :path pseudo-header and resend the request. Observe that you have successfully poisoned the cache with the tunnelled response.

Now you need to find a gadget that reflects an HTML-based XSS payload without encoding or escaping it. Send a response for GET /resources and observe that this triggers a redirect to /resources/.

Try tunnelling this request via the :path pseudo-header, including an XSS payload in the query string as follows.

Name

:path

Value

/?cachebuster=3 HTTP/1.1\r\n

Host: YOUR-LAB-ID.web-security-academy.net\r\n

\r\n

GET /resources?<script>alert(1)</script> HTTP/1.1\r\n

Foo: bar

Observe that the request times out. This is because the Content-Length header in the main response is longer than the nested response to your tunnelled request.

From the proxy history, check the Content-Length in the response to a normal GET / request and make a note of its value. Go back to your malicious request in Burp Repeater and add enough arbitrary characters after the closing </script> tag to pad your reflected payload so that the length of the tunnelled response will exceed the Content-Length you just noted.

Send the request and confirm that your payload is successfully reflected in the tunnelled response. If you still encounter a timeout, you may not have added enough padding.

While the cache is still poisoned, visit the home page using the same cachebuster query parameter and confirm that the alert() fires.

In the Inspector, remove the cachebuster from your request and resend it until you have poisoned the cache. Keep resending the request every 5 seconds or so to keep the cache poisoned until the victim visits the home page and the lab is solved.

Community solutions

Sam Bowne

Find HTTP request smuggling vulnerabilities using Burp Suite

Try for free
