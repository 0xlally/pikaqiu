# Performing HTTP/2-exclusive attacks

Source: https://portswigger.net/burp/documentation/desktop/http2/performing-http2-exclusive-attacks
Fetched: 2026-06-28T09:15:51.339568+00:00

Support Center

Documentation

Desktop editions

HTTP/2

Performing HTTP/2-exclusive attacks

ProfessionalCommunity Edition

Performing HTTP/2-exclusive attacks

Last updated:

June 18, 2026

Read time:

2 Minutes

When you intercept a request in Burp Proxy, or send it to Burp Repeater, the Inspector enables you to work with HTTP/2 headers and pseudo-headers in a way that closely resembles the underlying request.

Each header and pseudo-header has its own entry under Request Headers, split into distinct Name and Value fields. Although we don't show you the actual binary, this is an accurate representation of what will be sent to the server. You can see this in action in the following video demonstration:

As this representation is completely decoupled from HTTP/1, you aren't bound by the limitations of HTTP/1 syntax when constructing malicious requests. This allows you to perform some advanced, HTTP/2-exclusive attacks.

For example, you can:

Inject colons into header names.

Inject arbitrary spaces or newlines within the method and path.

Inject newlines anywhere within a header name or value.

You can make most of these changes by just double-clicking the name or value of a header in the main Inspector view.

According to the specification, these kinds of injections should cause the request to be rejected by the server, but some servers tolerate them anyway. Burp is currently the only tool that enables you to take advantage of this behavior.

Note

Once you apply these changes, the message editor will be unable to accurately represent the request using HTTP/1 syntax without losing information. In this case, the request is considered "kettled".

Injecting newlines into headers

To inject a newline into an HTTP/2 header or value, drill down into the header by clicking the chevron to the right of its entry in the Inspector. From this view, you can select either the Name or Value field and press the Shift + Return keys to enter the sequence \r\n.
