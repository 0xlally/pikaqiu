# HTTP/2-exclusive vectors

Source: https://portswigger.net/web-security/request-smuggling/advanced/http2-exclusive-vectors
Fetched: 2026-06-28T09:18:00.051638+00:00

Web Security Academy

Request smuggling

Advanced

HTTP/2-exclusive vectors

HTTP/2-exclusive vectors

Due to the fact that HTTP/2 is a binary protocol rather than text-based, there are a number of potential vectors that are impossible to construct in HTTP/1 due to the limitations of its syntax.

We've already seen how you can inject CRLF sequences into a header value. In this section, we'll give you an idea of some of the other HTTP/2-exclusive vectors you can use to inject payloads. Although these kinds of requests are officially prohibited by the HTTP/2 specification, some servers fail to validate and block them effectively.

Note

It's only possible to perform these attacks using the specialized HTTP/2 features in Burp's Inspector panel.

Injecting via header names

In HTTP/1, it's not possible for a header name to contain a colon because this character is used to indicate the end of the name to parsers. This is not the case in HTTP/2.

By combining colons with \r\n characters, you may be able to use an HTTP/2 header's name field to sneak other headers past front-end filters. These will then be interpreted as separate headers on the back-end once the request is rewritten using HTTP/1 syntax:

Front-end (HTTP/2)

foo: bar\r\nTransfer-Encoding: chunked\r\nX:

ignore

Back-end (HTTP/1)

Foo: bar\r\n

Transfer-Encoding: chunked\r\n

X: ignore\r\n

Injecting via pseudo-headers

HTTP/2 doesn't use a request line or status line. Instead, this data is passed via a series of "pseudo-headers" on the front of the request. In text-based representations of HTTP/2 messages, these are commonly prefixed with a colon to help differentiate them from normal headers. There five pseudo-headers in total:

:method - The request method.

:path - The request path. Note that this includes the query string.

:authority - Roughly equivalent to the HTTP/1 Host header.

:scheme - The request scheme, typically http or https.

:status - The response status code (not used in requests).

When websites downgrade requests to HTTP/1, they use the values of some of these pseudo-headers to dynamically construct the request line. This enables some interesting new ways of constructing attacks.

Supplying an ambiguous host

Although the HTTP/1 Host header is effectively replaced by the :authority pseudo-header in HTTP/2, you're still allowed to send a host header in the request as well.

In some cases, this may result in two Host headers occurring in the rewritten HTTP/1 request, which opens up another possibility for bypassing front-end "duplicate Host header" filters, for example. This potentially makes the site vulnerable to a range of Host header attacks to which it may otherwise have been immune.

Supplying an ambiguous path

Trying to send a request with an ambiguous path is not possible in HTTP/1 due to how the request line is parsed. But as the path in HTTP/2 is specified using a pseudo-header, it's now possible to send a request with two distinct paths as follows:

:method

POST

:path

/anything

:path

/admin

:authority

vulnerable-website.com

If there is a discrepancy between which path is validated by the website's access controls and which path is used to route the request, this may enable you to access endpoints that would otherwise be off limits.

Injecting a full request line

During downgrading, the value of the :method pseudo-header will be written to the very beginning of the resulting HTTP/1 request. If the server allows you to include spaces in the :method value, you may be able to inject an entirely different request line as follows:

Front-end (HTTP/2)

:method

GET /admin HTTP/1.1

:path

/anything

:authority

vulnerable-website.com

Back-end (HTTP/1)

GET /admin HTTP/1.1 /anything HTTP/1.1

Host: vulnerable-website.com

As long as the server also tolerates the arbitrary trailing characters in the request line, this provides another means of creating a request with an ambiguous path.

Injecting a URL prefix

Another interesting feature of HTTP/2 is the ability to explicitly specify a scheme in the request itself using the :scheme pseudo-header. Although this will ordinarily just contain http or https, you may be able to include arbitrary values.

This can be useful when the server uses the :scheme header to dynamically generate a URL, for example. In this case, you could add a prefix to the URL or even override it completely by pushing the real URL into the query string:

Request

:method

GET

:path

/anything

:authority

vulnerable-website.com

:scheme

https://evil-user.net/poison?

Response

:status

301

location

https://evil-user.net/poison?://vulnerable-website.com/anything/

Injecting newlines into pseudo-headers

When injecting into the :path or :method pseudo-headers, you need to make sure that the resulting HTTP/1 request still has a valid request line.

As the \r\n terminates the request line in HTTP/1, simply adding \r\n part way through will just break the request. After downgrading, the rewritten request must contain the following sequence prior to the first \r\n that you inject:

<method> + space + <path> + space + HTTP/1.1

Just visualize where your injection falls within this sequence and include all of the remaining parts accordingly. For example, when injecting into the :path, you need to add a space and HTTP/1.1 before the \r\n as follows:

Front-end (HTTP/2)

:method

GET

:path

/example HTTP/1.1\r\n

Transfer-Encoding: chunked\r\n

X: x

:authority

vulnerable-website.com

Back-end (HTTP/1)

GET /example HTTP/1.1\r\n

Transfer-Encoding: chunked\r\n

X: x HTTP/1.1\r\n

Host: vulnerable-website.com\r\n

\r\n

Notice that in this case, we've also added an arbitrary trailing header to catch the space and protocol that were added automatically during rewriting.

Find HTTP request smuggling vulnerabilities using Burp Suite

Try for free
