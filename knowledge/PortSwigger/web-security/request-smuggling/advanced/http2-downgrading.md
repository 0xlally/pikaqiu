# HTTP/2 downgrading

Source: https://portswigger.net/web-security/request-smuggling/advanced/http2-downgrading
Fetched: 2026-06-28T09:18:00.299080+00:00

Web Security Academy

Request smuggling

Advanced

HTTP/2 downgrading

HTTP/2 downgrading

As HTTP/2 is still relatively new, web servers that support it often still have to communicate with legacy back-end infrastructure that only speaks HTTP/1. As a result, it has become common practice for front-end servers rewrite each incoming HTTP/2 request using HTTP/1 syntax, effectively generating its HTTP/1 equivalent. This "downgraded" request is then forwarded to the relevant back-end server instead.

When the HTTP/1-speaking back-end issues a response, the front-end server reverses this process to generate the HTTP/2 response that it returns to the client.

This works because each version of the protocol is fundamentally just a different way of representing the same information. Each item in an HTTP/1 message has an approximate equivalent in HTTP/2.

As a result, it's relatively straightforward for servers to convert these requests and responses between the two protocols. In fact, this is how Burp is able to display HTTP/2 messages in the message editor using HTTP/1 syntax.

HTTP/2 downgrading is extremely widespread and is even the default behavior for a number of popular reverse proxy services. In some cases, there isn't even an option to disable it.

What risks are associated with HTTP/2 downgrading?

HTTP/2 downgrading can expose websites to request smuggling attacks, even though HTTP/2 itself is generally considered immune when used end to end.

HTTP/2's built-in length mechanism means that, when HTTP downgrading is used, there are potentially three different ways to specify the length of the same request, which is the basis of all request smuggling attacks.

Read more

HTTP/2 request smuggling

Find HTTP request smuggling vulnerabilities using Burp Suite

Try for free
