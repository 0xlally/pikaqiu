# HTTP/2 normalization in the message editor

Source: https://portswigger.net/burp/documentation/desktop/http2/http2-normalization-in-the-message-editor
Fetched: 2026-06-28T09:15:51.141728+00:00

Support Center

Documentation

Desktop editions

HTTP/2

Normalization

ProfessionalCommunity Edition

HTTP/2 normalization in the message editor

Last updated:

June 18, 2026

Read time:

2 Minutes

Burp's message editor displays HTTP/2 requests using HTTP/1-style syntax. In other words, it shows you what the request would look like if it was an HTTP/1 request. It does this by mapping each component of the request to its HTTP/1 equivalent, and reversing this process when you make any changes in the editor. For example, it maps the request line to the :method and :path pseudo-headers and derives the :authority from the Host header.

Burp performs some lightweight normalization on any changes you make in the editor to reduce the risk of inadvertently sending an HTTP/2 request that is likely to be rejected. You can still send requests without any normalization if you want to see how the server responds to requests that are theoretically invalid.

What normalization is performed?

The following normalization is performed when Burp converts your HTTP/1-style input in the message editor to an HTTP/2 message:

Any capital letters in header names are converted to lowercase.

If present, the Connection header is stripped.

If you've moved the Host header, it is returned to its original position.

This ensures that, as long as you create a syntactically valid HTTP/1 request, Burp will generate an HTTP/2 request that adheres to the specification. Otherwise, it would be easy to accidentally create requests that would be rejected by many servers.

When you send the request, the representation of it in the editor is updated to reflect any normalization was performed. This transparency helps you understand what's happening to your request behind the scenes.

Why can't I move the Host header?

Burp maps the Host header you see in the editor to its HTTP/2 equivalent, namely the :authority pseudo-header. In HTTP/2, all pseudo-headers are supposed to be sent before any normal headers. For this reason, Burp sends the pseudo-headers in a fixed order unless you override this by moving them in the Inspector.

Sending requests without any normalization

To send HTTP/2 requests without any normalization, use the Inspector to make your changes rather than the message editor. The only exception to this is that the Connection header is still stripped by default, but you can control this behavior from the Repeater menu.

This enables you to intentionally send requests that do not adhere to the HTTP/2 specification to see how the server responds.
