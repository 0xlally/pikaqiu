# HTTP settings

Source: https://portswigger.net/burp/documentation/desktop/settings/network/http
Fetched: 2026-06-28T09:15:54.976917+00:00

Support Center

Documentation

Desktop editions

Settings

Network

HTTP

ProfessionalCommunity Edition

HTTP settings

Last updated:

June 18, 2026

Read time:

4 Minutes

The HTTP settings enable you to configure:

Allowed redirect types.

Streaming responses.

Status 100 response handling.

HTTP/1 settings.

HTTP/2 settings.

Allowed redirect types

These settings control the redirect types that Burp can use. Select from the following redirect types:

3xx status code with Location header.

Refresh header.

Meta refresh tag.

JavaScript-driven.

Any status code with Location header.

Note

Burp's behavior in following redirects is determined by the configuration of the individual Burp tools (for instance, the Target scope).

The Allowed redirect types settings are project settings. They apply to the current project only.

Streaming responses

These settings enable you to identify URLs that return streaming responses - responses that remain open and continuously deliver data. Burp handles these responses differently to normal responses.

Streaming is commonly used in AI-powered applications, such as chat interfaces backed by LLMs. In these cases, the server keeps the connection open and sends partial responses (for example, one word or sentence at a time), allowing real-time output as the model completes its response. Streaming is also used in other live-update applications, such as continuously-updating price data in trading applications.

However, intercepting proxies can break these applications because they use a store-and-forward model. In this case, the Proxy waits indefinitely for the streaming response to finish, and none of the response is ever forwarded to the client.

Burp's tools handle streaming responses in the following ways:

The Proxy passes these responses straight through to the client in real time.

Repeater updates the response panel in real time as data is received. You can set a timeout in the Settings dialog under Tools > Repeater > Streaming response timeout. For more information, see

Streaming responses timeout.

All other tools ignore streaming responses and close the connection.

To add a URL to the streaming responses list, click Add and enter the required details.

Note

Streaming response URLs use Burp's standard URL matching rules. For more information, see URL-matching rules.

You can also edit and reorder the rules in the list if required.

There are three other options available:

Store streaming responses - This setting causes Burp to store streaming responses in full. This option is necessary if you wish to view the contents of streaming responses within the Proxy history and Repeater response panel. Note that storing streaming responses may result in large temporary files.

Strip chunked encoding metadata in streaming responses - Streaming responses are generally chunked-encoded over HTTP. If you select this option, Burp removes the chunked encoding metadata which makes the responses more easily readable within Burp. Note that removing this metadata may break the client-side application.

Treat responses with the text/event-stream MIME type as streaming - Burp automatically treats responses with the

text/event-stream MIME type as streaming, even if they're not specified in the streaming responses list. This MIME type is commonly used for server-sent events (SSE), which are often used in AI-powered applications.

Streaming responses are often compressed using GZIP encoding. You can configure Burp to decompress GZIP content via options in the Proxy and Repeater configurations.

Note

You can also use Burp's support for streaming responses to handle very large responses that are not strictly streaming responses (such as binary file downloads), in order to bypass the store-and-forward proxy model and improve Burp's performance.

The Streaming responses settings are project settings. They apply to the current project only.

Status 100 response handling

These settings control how Burp handles status 100 HTTP responses. These responses often occur when a POST request is sent to the server, and the server makes an interim response before the request body is transmitted.

The following settings are available:

Understand 100 Continue responses - Burp skips the interim response and parses the "real" response headers for information such as status code and content type.

Remove 100 Continue headers - Burp removes any interim headers from the server's response before it is passed to individual tools.

The Status 100 response handling settings are project settings. They apply to the current project only.

HTTP/1

By default, Burp Suite opens a new TCP connection for each HTTP/1.1 request / response pair. If you select Use keep-alive for HTTP/1 if the server supports it, the system keeps the same TCP connection open for multiple request / response pairs. This brings significant benefits in speed and request timing.

Burp Suite closes any open TCP connections after five seconds of inactivity.

Note

This setting affects all Burp Suite tools that send HTTP requests.

You can override this for Repeater using the Enable HTTP/1 connection reuse menu setting. For more information, see the Repeater settings page.

You can override this for Intruder using the HTTP/1 connection reuse setting. For more information, see the Intruder HTTP settings page.

The HTTP/1 settings are project settings. They apply to the current project only.

HTTP/2

By default, Burp uses HTTP/2 to communicate with all servers that advertise support for it during the TLS handshake. If you deselect Default to HTTP/2 if the server supports it then Burp uses HTTP/1 even if the server supports HTTP/2.

You can override this setting for individual tools in Burp:

Use the Protocol toggle in the Inspector panel to override this setting. For example, use this in Burp Repeater requests or an intercepted request in Burp Proxy.

Use the HTTP version Burp Intruder attack setting to override this setting for a specific Intruder attack. For more information, see

Burp Intruder attack settings.

Burp provides two options for working with HTTP/2 messages in a human-readable format. For more information, see the HTTP/2 documentation.

Note

We have only implemented the features of HTTP/2 that are relevant for use with Burp Suite. Additional features, such as server push, are not supported.

The HTTP/2 settings are project settings. They apply to the current project only.
