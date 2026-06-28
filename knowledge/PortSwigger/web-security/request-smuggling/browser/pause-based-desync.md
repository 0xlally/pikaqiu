# Pause-based desync attacks

Source: https://portswigger.net/web-security/request-smuggling/browser/pause-based-desync
Fetched: 2026-06-28T09:18:01.293743+00:00

Web Security Academy

Request smuggling

Browser-powered

Pause-based desync attacks

Pause-based desync attacks

Seemingly secure websites may contain hidden desync vulnerabilities that only reveal themselves if you pause mid-request.

Servers are commonly configured with a read timeout. If they don't receive any more data for a certain amount of time, they treat the request as complete and issue a response, regardless of how many bytes they were told to expect. Pause-based desync vulnerabilities can occur when a server times out a request but leaves the connection open for reuse. Given the right conditions, this behavior can provide an alternative vector for both server-side and client-side desync attacks.

PortSwigger Research

The materials and labs in this section are based on Browser-Powered Desync Attacks: A New Frontier in HTTP Request Smuggling by PortSwigger Research.

Server-side pause-based desync

You can potentially use the pause-based technique to elicit CL.0-like behavior, allowing you to construct server-side request smuggling exploits for websites that may initially appear secure.

This is dependent on the following conditions:

The front-end server must immediately forward each byte of the request to the back-end rather than waiting until it has received the full request.

The front-end server must not (or can be encouraged not to) time out requests before the back-end server.

The back-end server must leave the connection open for reuse following a read timeout.

To demonstrate how this technique works, let's walk through an example. The following is a standard CL.0 request smuggling probe:

POST /example HTTP/1.1

Host: vulnerable-website.com

Connection: keep-alive

Content-Type: application/x-www-form-urlencoded

Content-Length: 34

GET /hopefully404 HTTP/1.1

Foo: x

Consider what happens if we send the headers to a vulnerable website, but pause before sending the body.

The front-end forwards the headers to the back-end, then continues to wait for the remaining bytes promised by the Content-Length header.

After a while, the back-end times out and sends a response, even though it has only consumed part of the request. At this point, the front-end may or may not read in this response and forward it to us.

We finally send the body, which contains a basic request smuggling prefix in this case.

The front-end server treats this as a continuation of the initial request and forwards this to the back-end down the same connection.

The back-end server has already responded to the initial request, so assumes that these bytes are the start of another request.

At this point, we have effectively achieved a CL.0 desync, poisoning the front-end/back-end connection with a request prefix.

We've found that servers are more likely to be vulnerable when they generate a response themselves rather than passing the request to the application.

PortSwigger Research

Our research team discovered this vulnerability on the widely used Apache HTTP Server, which exhibited this behavior when performing server-level redirects from /example to /example/. We reported this issue and it has been fixed in version 2.4.53, so make sure to update if you haven't already. For more details, check out Browser-Powered Desync Attacks: A New Frontier in HTTP Request Smuggling by PortSwigger Research.

Testing for pause-based CL.0 vulnerabilities

It's possible to test for pause-based CL.0 vulnerabilities using Burp Repeater, but only if the front-end server forwards the back-end's post-timeout response to you the moment it's generated, which isn't always the case. We recommend using the Turbo Intruder extension as it lets you pause mid-request then resume regardless of whether you've received a response.

In Burp Repeater, create a CL.0 request smuggling probe like we used in the example above, then send it to Turbo Intruder.

POST /example HTTP/1.1

Host: vulnerable-website.com

Connection: keep-alive

Content-Type: application/x-www-form-urlencoded

Content-Length: 34

GET /hopefully404 HTTP/1.1

Foo: x

In Turbo Intruder's Python editor panel, adjust the request engine configuration to set the following options:

concurrentConnections=1

requestsPerConnection=100

pipeline=False

Queue the request, adding the following arguments to the queue() interface:

pauseMarker - A list of strings after which you want Turbo Intruder to pause.

pauseTime - The duration of the pause in milliseconds.

For example, to pause after the headers for 60 seconds, queue the request as follows:

engine.queue(target.req, pauseMarker=['\r\n\r\n'], pauseTime=60000)

Queue an arbitrary follow-up request as normal:

followUp = 'GET / HTTP/1.1\r\nHost: vulnerable-website.com\r\n\r\n'

engine.queue(followUp)

Ensure that you're logging all responses to the results table:

def handleResponse(req, interesting):

table.add(req)

When you first start the attack, you won't see any results in the table. However, after the specified pause duration, you should see two results. If the response to the second request matches what you expected from the smuggled prefix (in this case a 404), this strongly suggests that the desync was successful.

Note

Instead of using pauseMarker to specify a pause based on string matching, you can use the pauseBefore argument to specify an offset. For example, you could pause before the body by specifying an offset that's the inverse of the Content-Length (pauseBefore=-34).

Client-side pause-based desync

In theory, it may be possible to perform a client-side variation of the pause-based CL.0 desync. Unfortunately, we haven't yet found a reliable way to make a browser pause mid-request. However, there is one possible workaround - an active MITM attack.

The encryption provided by TLS may prevent a MITM from reading traffic in-flight, but there's nothing to stop them from delaying the TCP packets on their way from the browser to the web server. By simply delaying the final packet until the web server issues a response, you may be able to desync the browser's connection.

The flow of this attack is similar to any other client-side desync attack. The user visits a malicious website, which causes their browser to issue a series of cross-domain requests to the target site. In this case, you need to deliberately pad the first request so that the operating system splits it into multiple TCP packets. As you control the padding, you can pad the request until the final packet has a distinct size so you can work out which one to delay.

For an example of how this might look in practice, see Browser-Powered Desync Attacks: A New Frontier in HTTP Request Smuggling.

How to prevent pause-based desync vulnerabilities

For some high-level measures you can take to prevent pause-based desync vulnerabilities, and other forms of desync attack, see How to prevent HTTP request smuggling vulnerabilities.

Find HTTP request smuggling vulnerabilities using Burp Suite

Try for free
