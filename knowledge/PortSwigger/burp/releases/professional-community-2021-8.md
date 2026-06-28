# Professional / Community 2021.8

Source: https://portswigger.net/burp/releases/professional-community-2021-8
Fetched: 2026-06-28T09:16:36.128588+00:00

This release provides a range of powerful new enhancements to Burp's HTTP/2 support. This enables you to identify and exploit a number of HTTP/2-exclusive vulnerabilities, including those presented by James Kettle at Black Hat USA 2021. It also implements a security fix for the embedded browser and some minor bug fixes for recorded login sequences.

Control the protocol for individual requests

In Burp Repeater and Proxy Intercept, you can now choose whether to send each request using HTTP/1 or HTTP/2. When you switch protocols, Burp will automatically perform the necessary transformations behind the scenes to generate an equivalent request suitable for the new protocol. For example, the HTTP/1 request line is mapped to HTTP/2's :method and :path pseudo-headers.

This enables you to easily upgrade and downgrade requests to experiment with protocol-specific vulnerabilities.

Test for HTTP/2-exclusive vulnerabilities

We are excited to announce that Burp Suite Professional and Community Edition now provide native support for viewing and manipulating HTTP/2 requests.

In addition to the HTTP/1-style representation of the request that you can see in the message editor, the Inspector now lets you work with HTTP/2 headers and pseudo-headers in a way that more closely resembles what will be sent to the server. As this view doesn't rely on HTTP/1 syntax, you're able to construct attacks using a number of HTTP/2-exclusive vectors that are impossible to reproduce in HTTP/1. This gives you the opportunity to explore a whole new attack surface that has barely been audited due to the complete lack of any suitable tooling until now.

For some real-world examples of what's possible, check out the whitepaper for James Kettle's latest research, HTTP/2: The Sequel Is Always Worse, which he recently presented at Black Hat USA 2021.

Burp's message editor still lets you work with an HTTP/1-style representation of the request and converts this to an equivalent HTTP/2 request under the hood. This is great for performing general testing where the protocol you're using isn't important.

For more information about these features, the configuration options, and a breakdown of some HTTP/2 fundamentals, please refer to the accompanying documentation

New HTTP/2 scan checks

In addition to the new manual HTTP/2 tooling, this release adds some HTTP/2-specific improvements to Burp Scanner:

Two new HTTP/2-exclusive methods of obfuscating the transfer-encoding header for HTTP request smuggling.

A new detection method for HTTP/2 request tunnelling.

A new scan check for "hidden" HTTP/2 support. Scanner can now detect when a server supports HTTP/2 but doesn't advertise this in the ALPN during the TLS handshake.

We've also improved the issue details for HTTP request smuggling to flag when server-side countermeasures have limited the impact to request tunnelling.

These enhancements are also based on James's research.

Embedded browser security fix

We have updated Burp Suite's embedded browser to fix a clickjacking-based remote code execution bug in Burp Suite, as reported to our bug bounty program by @mattaustin and @DanAmodio. We have updated to Chromium 92.0.4515.131, which fixes several bugs that Google has classified as high

Bug fixes

This release fixes several bugs that should improve the reliability of recorded login playback.
