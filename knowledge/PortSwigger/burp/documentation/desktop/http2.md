# Working with HTTP/2 in Burp Suite

Source: https://portswigger.net/burp/documentation/desktop/http2
Fetched: 2026-06-28T09:15:51.183104+00:00

Support Center

Documentation

Desktop editions

HTTP/2

ProfessionalCommunity Edition

Working with HTTP/2 in Burp Suite

Last updated:

June 18, 2026

Read time:

7 Minutes

Many servers now support HTTP/2. This exposes them to potential vulnerabilities that are impossible to test for using tools that only speak HTTP/1. Burp Suite provides unrivaled support for HTTP/2-based testing, allowing you to work with HTTP/2 requests in ways that no other tools can. You can either:

Work with an HTTP/1-style representation of the request in the message editor

Burp normalizes any changes you make and sends an equivalent HTTP/2 request to the server. This is perfect for general testing in cases where the protocol you're using isn't important.

Work with an HTTP/2 view in the Inspector

This shows a more accurate representation of the headers and pseudo-headers that will be sent to the server. As this view doesn't rely on any HTTP/1 syntax, it also enables you to construct attacks using a number of HTTP/2-exclusive vectors.

Burp's unique HTTP/2 features give you the opportunity to explore a whole new attack surface that has barely been audited due to the complete lack of any suitable tooling until now. For some real-world examples of what's possible, check out how one of our researchers was able to use these features to identify and exploit a widespread new vector for request smuggling.

PortSwigger Research

HTTP/2: The Sequel Is Always Worse

Background concepts

Under the hood, HTTP/2 is very different from HTTP/1. To help you get the most out of these features, we've provided a brief overview of the background concepts that are relevant.

Default protocol

By default, Burp speaks HTTP/2 to all servers that advertise support for it via ALPN during the TLS handshake. This ensures that, even if you're not conducting any protocol-specific testing, you can still take advantage of the performance improvements provided by HTTP/2 where available.

You can also tailor this behavior to suit your current needs by changing the default protocol for the project. This is useful if you're performing testing where it's necessary to always use HTTP/1. You can still send individual HTTP/2 requests by switching the protocol in the Inspector if necessary.

Keeping track of which protocol you're using

When testing for protocol-level vulnerabilities, it's important that you're aware of which protocol is being used for each request. There are a number of places where this information is displayed:

In the message editor, the request line and status line contain the protocol version. This is standard for HTTP/1 messages, but also applies to the editor's representation of HTTP/2 messages.

In Burp Repeater, the current protocol is displayed in the upper-right corner of the screen, next to the target host.

In the Inspector, the Request Attributes section displays the protocol version. In non-editable contexts, such as in the proxy history, the highlighted protocol is purely informational. For requests that you've intercepted in Burp Proxy or sent to Burp Repeater, you can toggle which protocol you want to use to send the request.

Changing the protocol for a request

Regardless of your default protocol settings, you can manually choose which protocol is used to send each request. To do this, use the toggle switch under Inspector > Request Attributes.

When you change the protocol, Burp performs the necessary transformations to generate an equivalent request in the correct format for the new protocol. This means you can easily upgrade and downgrade individual requests as needed.

By default, you can only upgrade requests to HTTP/2 if the server explicitly advertises support for this via ALPN during the TLS handshake. If you want to try sending HTTP/2 requests anyway to test for hidden HTTP/2 support, you first need to enable the Allow HTTP/2 ALPN override option from the Repeater menu.

Note

When working in the Inspector, it's possible to create an HTTP/2 request that cannot be accurately represented using HTTP/1 syntax without losing information. Burp refers to this as a "kettled" request. If you try to downgrade such a request, Burp warns you that the request will have to be normalized so that it can be displayed in the editor.

Kettled requests

The Inspector enables you to create HTTP/2 requests that are impossible to accurately represent using HTTP/1 syntax without losing information. In honor of our infamous Director of Research, James Kettle, we've coined the term "kettled" to describe such requests.

For example, it's technically possible to add a newline character inside a header value in HTTP/2. There is no way to show this in HTTP/1 as a newline indicates the end of a header, so anything after it would just appear to be the start of the next header's name.

Once a request is kettled, the message editor no longer attempts to display an HTTP/1 equivalent of it. You will still be able to see the body of the message, but in place of the headers, Burp will display a notification that tells you why the request is considered kettled. If you want to make further changes to the headers of a kettled request, you need to use the Inspector.

Note

Burp Proxy, Repeater, Logger, and Scanner currently support kettled requests. If you send a kettled request to a tool that doesn't support them, such as Intruder, it will be normalized so that it can be displayed in the editor.

What can cause a request to become kettled?

Requests become kettled whenever you make the following changes using the Inspector:

Adding an uppercase letter or colon to a header name.

Adding a newline character to a header name or value.

Modifying the value of the :scheme pseudo-header.

Adding a space character to the :path or :method pseudo-header.

Adding a duplicate pseudo-header.

Adding a semicolon and space character to a cookie value.

Unkettling a request

If you accidentally kettle a request, you have a number of options for unkettling it. You can:

Undo your changes using the Ctrl/Cmd + Z keys.

Use the Inspector to manually reverse the specific changes that have caused the request to be kettled. Check the notification in the editor to see which changes you need to make.

Downgrade the request to HTTP/1 using the toggle in the Inspector and dismiss the warning telling you that your changes will be lost. Burp will normalize the request, effectively discarding any changes that are incompatible with HTTP/1.

Kettled requests and extensions

Extensions are able to generate and issue new kettled requests, so you can already develop your own extensions for HTTP/2-based testing. However, extensions are currently unable to modify kettled requests that were originally issued by Burp. This is because they only have access to the normalized, HTTP/1-style representation of Burp's requests.

HTTP/2 settings

There are a number of settings throughout Burp that let you adjust its behavior when working with HTTP/2.

Changing the default protocol

By default, Burp speaks HTTP/2 to all servers that advertise support for it via ALPN during the TLS handshake. However, you can change the default protocol so that it uses HTTP/1 unless you explicitly tell it to send an HTTP/2 request. To do this, go to Settings > Network > HTTP and deselect the Default to HTTP/2 if the server supports it option.

You might want to do this if you're focusing on a vulnerability that specifically requires HTTP/1, such as classic CL.TE or TE.CL request smuggling.

You can still override this global setting for individual requests by using the Protocol toggle under Inspector > Request Attributes.

Repeater options for HTTP/2

From the Repeater menu at the top of the screen, you can access the following options for controlling Burp Repeater's behavior when handling HTTP/2 requests.

Enforce protocol choice on cross-domain redirections

By default, Repeater will negotiate the protocol as normal when redirected cross-domain. If you enable this option, it will follow any cross-domain redirections using the same protocol that is selected under Inspector > Request Attributes. This is important when testing for HTTP/2-specific vulnerabilities that trigger cross-domain requests.

Enable HTTP/2 connection reuse

By default, Repeater reuses the same connection for multiple HTTP/2 requests. Some servers treat the first request on each connection differently to subsequent requests, which can lead to vulnerabilities appearing intermittent or even being missed entirely. On other servers, sometimes a request will corrupt a connection without causing the server to tear it down, silently influencing how all subsequent requests get processed.

If you run into either of these problems, you can mitigate them by disabling this option so that the request you send is always the first one on the connection.

Strip Connection header over HTTP/2

By default, when an HTTP/2 request contains a Connection header, Burp strips this before sending the request to the server. This is because many HTTP/2 servers will reject requests containing this header.

If you want to experiment with sending the Connection header anyway, you can disable this option.

Allow HTTP/2 ALPN override

Enabling this setting allows you to send HTTP/2 requests from Burp Repeater even when the server doesn't advertise HTTP/2 support via ALPN. This lets you explore any "hidden HTTP/2" attack surface reported by Burp Scanner or manually test for hidden HTTP/2 support.

Disabling HTTP/2 for proxy listeners

In some rare cases, such as when a client has problems with its HTTP/2 implementation, you may want to disable HTTP/2 on the connection between the client and Burp's proxy listener. To do this, click

Settings to open the Settings dialog. Go to Tools > Proxy and select the relevant listener under

Proxy listeners, then click Edit. In the dialog, go to the HTTP/2 tab and deselect the Support HTTP/2 checkbox. Burp will then only accept HTTP/1 on this connection even if the client wants to use HTTP/2.

Note that this does not affect the connection between Burp and the server.

Upcoming enhancements for HTTP/2 in Burp

There are some limitations to Burp's HTTP/2 support. We are currently working on the following enhancements.

Increased support for kettled requests

At the moment, some of Burp's tools cannot handle kettled requests, most notably, Burp Intruder. We aim to enable you to work with kettled requests in all of Burp's tools in future releases.
