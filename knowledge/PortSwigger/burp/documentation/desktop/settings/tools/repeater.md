# Repeater settings

Source: https://portswigger.net/burp/documentation/desktop/settings/tools/repeater
Fetched: 2026-06-28T09:15:56.611448+00:00

Support Center

Documentation

Desktop editions

Settings

Tools

Repeater

ProfessionalCommunity Edition

Repeater settings

Last updated:

June 18, 2026

Read time:

4 Minutes

The Repeater page in the Settings dialog contains settings for the following:

Connections.

Message modification.

Redirects.

Streaming responses timeout

Default tab group.

Tab view.

Note

You can override the settings selected in the Settings dialog for an individual Repeater tab. For more information, see

Configuring tab-specific settings.

Otherwise, these global settings apply to all Repeater tabs.

Connections

These settings control whether Repeater reuses TCP connections, and whether it can send HTTP/2 requests when the server doesn't advertise HTTP/2 support.

The following settings are available:

HTTP/1 connection reuse - Enable this setting to reuse the same connection for HTTP/1 requests, instead of opening a new connection for each HTTP 1.1 request / response pair. This increases speed and benefits request timing. Burp closes any open connection after five seconds of inactivity.

HTTP/2 connection reuse - By default, Repeater reuses the same TCP connection for multiple HTTP/2 requests. You may want to disable this setting if the server treats the first request on a connection differently to subsequent requests.

Allow HTTP/2 ALPN override - Enable this setting to use ALPN to send HTTP/2 requests when the server doesn't advertise HTTP/2 support. This enables you to test for hidden HTTP/2 support, and explore hidden HTTP/2 attack surfaces.

Related pages

Working with HTTP/2 in Burp Suite.

The Connections settings are project settings. They apply to the current project only.

Message modification

These settings control Repeater's behavior when sending or receiving messages. The following settings are available:

Update Content-Length - By default, Burp automatically updates the Content-Length header of the request. This is usually necessary when the request message contains a body.

Unpack compressed responses - By default, Burp automatically unpacks any gzip, deflate, and Brotli-compressed content received in responses.

Normalize HTTP/1 line endings - By default, Burp normalizes HTTP/1 line endings by appending a carriage return (\r) to any lines that end with a newline character (\n). The carriage return appends immediately before the newline, which reduces the risk of sending an invalid request. You can disable this setting when you intentionally omit the newline to test for vulnerabilities such as request smuggling.

Strip Connection header over HTTP/2 - By default, Burp strips the Connection header from HTTP/2 requests before the requests are sent. Many HTTP/2 servers reject requests that contain this header. You can disable this setting to see how the server responds when it receives a HTTP/2 request with a Connection header.

The Message modification settings are project settings. They apply to the current project only.

Redirects

These settings control how Repeater handles redirection responses.

Follow redirects

You can control whether Repeater follows redirects automatically. The following options are available:

Never - Never follow redirects.

On-site only - Follow redirects that point to a destination in the same domain.

In-scope only - Follow redirects that point to a destination that is in-scope.

Always - Always follow redirects.

Repeater displays a Follow redirection button if it receives a redirect response that it is not configured to follow automatically. Click this button to follow the redirect. This enables you to manually step through a redirection sequence.

Process cookies in redirects

If you enable this setting, Burp resubmits any cookies set in the redirect response when it follows the redirection target.

Use selected protocol for cross-domain redirects

This setting controls whether Repeater uses the protocol selected under the Request Attributes field in Burp Inspector to follow any cross-domain redirects. By default, this setting is disabled and Repeater negotiates protocol as normal.

You may wish to enable this setting when you test for HTTP/2-specific vulnerabilities that trigger cross-domain requests.

Related pages

Working with HTTP/2 in Burp Suite.

The Redirects settings are project settings. They apply to the current project only.

Streaming responses timeout

Streaming responses remain open and deliver data continuously. When Burp Repeater handles a streaming response, it updates the response panel in real time as data is received.

This setting controls how long Repeater keeps a streaming connection open. By default, it's set to 600 seconds (10 minutes).

To turn off the timeout, set it to 0.

The Streaming responses setting is a project setting. It applies to the current project only.

Related pages

You can configure how Burp detects and handles streaming responses in the Settings dialog under Network >

HTTP > Streaming responses. For more information, see Streaming responses.

Default tab group

This setting enables you to specify the tab group that new requests are added to when you send them to Repeater.

Use the drop-down menu to specify the tab group that you want to add new requests to.

Before you use this setting, create a tab group in Repeater. For more information, see Managing tab

groups.

Note

This setting doesn't influence new request tabs that you create within Repeater. These aren't allocated to a group when they're created.

The Default tab group setting is a project setting. It applies to the current project only.

Tab view

This setting controls the default tab view in Repeater. The following options are available:

Scrolling view - Tabs are displayed in a single, scrollable row. Click on the search icon to view a drop-down list of all open tabs.

Wrapped view - Tabs wrap into multiple rows.

The Tab view setting is a user setting. It applies to all installations of Burp on your machine.

Related pages

Managing Burp Repeater tabs.
