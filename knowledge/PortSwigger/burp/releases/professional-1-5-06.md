# Professional 1.5.06

Source: https://portswigger.net/burp/releases/professional-1-5-06
Fetched: 2026-06-28T09:16:24.727727+00:00

This release adds a number of useful new features and bugfixes.

New CSRF technique

The CSRF PoC generator adds a new technique to generate requests using cross-domain XmlHttpRequest (XHR). This allows the submission of arbitrary binary request bodies together with any "standard" Content-Type header, including "application/x-www-form-urlencoded" and "multipart/form-data". One obvious use for the new technique is that it allows for cross-domain file upload, where a filename attribute needs to be included in a multi-part message body.

The cross-domain XHR technique requires a modern browser that is capable of cross-origin resource sharing (CORS). CORS allows XHR to make arbitrary cross-domain requests. However, if a request contains any "non-standard" features (method, headers or content type) then the request is "preflighted". Here, the browser first verifies whether the destination server is configured to accept cross-domain requests of the relevant type, and this will normally cause the attack to fail. On the other hand, if a request contains only "simple" features (roughly, those that can be generated using a standard HTML form) then the request is not preflighted: the browser simply makes the full cross-domain request, and adds an Origin header identifying the domain from which the request originated. Servers will typically ignore the Origin header and process the request in the normal way.

The loophole provided by the XHR technique is that it allows us to create requests with a "normal" Content-Type header together with completely arbitrary content in the message body. So in the case of cross-domain file upload, we can include the required filename attribute in a way that cannot be done in a pure HTML form (unless, of course, the victim user is induced into selecting a file to upload).

The following points should be noted about the cross-domain XHR technique:

It includes the browser's cookies in the normal way, and so works with authenticated (in-session) requests.

It requires a relatively recent browser, and works on current versions of Firefox, Internet Explorer and Chrome.

The application's response is not processed by the browser in the normal way, so the technique is not suitable for making cross-domain requests to deliver reflected cross-site scripting (XSS) attacks.

If you try to generate a PoC for a request containing any unusual features that may trigger a preflighted request, Burp will do its best to construct a valid PoC, and will warn you about the problematic features.

New SSL options

Several new options are available for SSL negotiation. You can now individually select which SSL protocols and ciphers to use:

Two new options are also available to help work around common problems in SSL negotiation:

"Automatically select compatible SSL parameters on negotiation failure" - If this option is enabled, then when Burp fails to negotiate SSL using the configured protocols and ciphers, it will probe the server to try and establish a set of compatible SSL parameters that are supported by both the server and Java. If compatible parameters are found, Burp caches this information and uses the parameters in the first instance for subsequent connections to the same server. This option is generally desirable and can avoid the need to troubleshoot SSL issues and experiment with protocols and ciphers.

"Enable algorithms blocked by Java security policy" - As of Java 7, the Java security policy can be used to block certain obsolete algorithms from being used in SSL negotiation, and some of these are blocked by default (such as MD2). Many live web servers have SSL certificates that use these obsolete algorithms, and it is not possible to connect to these servers using the default Java security policy. Enabling this option allows Burp to use the obsolete algorithms when connecting to the affected servers. Changes to this option take effect when you restart Burp.

Both these new options are enabled by default.

Other updates

The release includes the following new features and bugfixes:

When doing invisible proxying of SSL connections, Burp now inspects the Client Hello message for the server_name extension. If this is present, Burp uses it to generate per-host CA-signed certificates in the normal way.

To facilitate development and debugging of extensions, you can now fast-reload an extension by Ctrl+clicking the "Loaded" checkbox in the table of extensions. The extension will be unloaded and reloaded without displaying a confirmation dialog. Further, extensions will now reuse the existing output window if one was already created for that extension.

The IInterceptedProxyMessage interface has two new methods, getListenerInterface and getClientIpAddress, which you can query to obtain details about the Burp Proxy listener and the client for the intercepted message.

The scope configuration UI now lets you load a list of items from a text file. Each item in the list should be either a URL or a domain name, and Burp will create appropriate scope rules accordingly.

A bug where sending requests from the Target Analyzer to other Burp tools always results in non-parameterized GET requests being sent, has been fixed.

A bug in the display of messages where character set encoding is wrongly applied to HTTP headers, making them unreadable in some cases (e.g. UTF-16LE) has been fixed.

There is a new workaround to try to prevent OS X from periodically deleting Burp's temporary files when using the default location.
