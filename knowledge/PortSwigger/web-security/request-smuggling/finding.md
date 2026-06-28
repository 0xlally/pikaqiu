# Finding HTTP request smuggling vulnerabilities

Source: https://portswigger.net/web-security/request-smuggling/finding
Fetched: 2026-06-28T09:18:02.114638+00:00

Web Security Academy

Request smuggling

Finding

Finding HTTP request smuggling vulnerabilities

In this section, we'll explain different techniques for finding HTTP request smuggling vulnerabilities.

Finding HTTP request smuggling vulnerabilities using timing techniques

The most generally effective way to detect HTTP request smuggling vulnerabilities is to send requests that will cause a time delay in the application's responses if a vulnerability is present. This technique is used by Burp Scanner to automate the detection of request smuggling vulnerabilities.

Finding CL.TE vulnerabilities using timing techniques

If an application is vulnerable to the CL.TE variant of request smuggling, then sending a request like the following will often cause a time delay:

POST / HTTP/1.1

Host: vulnerable-website.com

Transfer-Encoding: chunked

Content-Length: 4

1

A

X

Since the front-end server uses the Content-Length header, it will forward only part of this request, omitting the X. The back-end server uses the Transfer-Encoding header, processes the first chunk, and then waits for the next chunk to arrive. This will cause an observable time delay.

Finding TE.CL vulnerabilities using timing techniques

If an application is vulnerable to the TE.CL variant of request smuggling, then sending a request like the following will often cause a time delay:

POST / HTTP/1.1

Host: vulnerable-website.com

Transfer-Encoding: chunked

Content-Length: 6

0

X

Since the front-end server uses the Transfer-Encoding header, it will forward only part of this request, omitting the X. The back-end server uses the Content-Length header, expects more content in the message body, and waits for the remaining content to arrive. This will cause an observable time delay.

Note

The timing-based test for TE.CL vulnerabilities will potentially disrupt other application users if the application is vulnerable to the CL.TE variant of the vulnerability. So to be stealthy and minimize disruption, you should use the CL.TE test first and continue to the TE.CL test only if the first test is unsuccessful.

Confirming HTTP request smuggling vulnerabilities using differential responses

When a probable request smuggling vulnerability has been detected, you can obtain further evidence for the vulnerability by exploiting it to trigger differences in the contents of the application's responses. This involves sending two requests to the application in quick succession:

An "attack" request that is designed to interfere with the processing of the next request.

A "normal" request.

If the response to the normal request contains the expected interference, then the vulnerability is confirmed.

For example, suppose the normal request looks like this:

POST /search HTTP/1.1

Host: vulnerable-website.com

Content-Type: application/x-www-form-urlencoded

Content-Length: 11

q=smuggling

This request normally receives an HTTP response with status code 200, containing some search results.

The attack request that is needed to interfere with this request depends on the variant of request smuggling that is present: CL.TE vs TE.CL.

Confirming CL.TE vulnerabilities using differential responses

To confirm a CL.TE vulnerability, you would send an attack request like this:

POST /search HTTP/1.1

Host: vulnerable-website.com

Content-Type: application/x-www-form-urlencoded

Content-Length: 49

Transfer-Encoding: chunked

e

q=smuggling&x=

0

GET /404 HTTP/1.1

Foo: x

If the attack is successful, then the last two lines of this request are treated by the back-end server as belonging to the next request that is received. This will cause the subsequent "normal" request to look like this:

GET /404 HTTP/1.1

Foo: xPOST /search HTTP/1.1

Host: vulnerable-website.com

Content-Type: application/x-www-form-urlencoded

Content-Length: 11

q=smuggling

Since this request now contains an invalid URL, the server will respond with status code 404, indicating that the attack request did indeed interfere with it.

Confirming TE.CL vulnerabilities using differential responses

To confirm a TE.CL vulnerability, you would send an attack request like this:

POST /search HTTP/1.1

Host: vulnerable-website.com

Content-Type: application/x-www-form-urlencoded

Content-Length: 4

Transfer-Encoding: chunked

7c

GET /404 HTTP/1.1

Host: vulnerable-website.com

Content-Type: application/x-www-form-urlencoded

Content-Length: 144

x=

0

Note

To send this request using Burp Repeater, you will first need to go to the Repeater menu and ensure that the "Update Content-Length" option is unchecked.

You need to include the trailing sequence \r\n\r\n following the final 0.

If the attack is successful, then everything from GET /404 onwards is treated by the back-end server as belonging to the next request that is received. This will cause the subsequent "normal" request to look like this:

GET /404 HTTP/1.1

Host: vulnerable-website.com

Content-Type: application/x-www-form-urlencoded

Content-Length: 144

x=

0

POST /search HTTP/1.1

Host: vulnerable-website.com

Content-Type: application/x-www-form-urlencoded

Content-Length: 11

q=smuggling

Since this request now contains an invalid URL, the server will respond with status code 404, indicating that the attack request did indeed interfere with it.

Note

Some important considerations should be kept in mind when attempting to confirm request smuggling vulnerabilities via interference with other requests:

The "attack" request and the "normal" request should be sent to the server using different network connections. Sending both requests through the same connection won't prove that the vulnerability exists.

The "attack" request and the "normal" request should use the same URL and parameter names, as far as possible. This is because many modern applications route front-end requests to different back-end servers based on the URL and parameters. Using the same URL and parameters increases the chance that the requests will be processed by the same back-end server, which is essential for the attack to work.

When testing the "normal" request to detect any interference from the "attack" request, you are in a race with any other requests that the application is receiving at the same time, including those from other users. You should send the "normal" request immediately after the "attack" request. If the application is busy, you might need to perform multiple attempts to confirm the vulnerability.

In some applications, the front-end server functions as a load balancer, and forwards requests to different back-end systems according to some load balancing algorithm. If your "attack" and "normal" requests are forwarded to different back-end systems, then the attack will fail. This is an additional reason why you might need to try several times before a vulnerability can be confirmed.

If your attack succeeds in interfering with a subsequent request, but this wasn't the "normal" request that you sent to detect the interference, then this means that another application user was affected by your attack. If you continue performing the test, this could have a disruptive effect on other users, and you should exercise caution.

Read more

Exploiting HTTP request smuggling vulnerabilities

Find HTTP request smuggling vulnerabilities using Burp Suite

Try for free
