# Professional / Community 2020.6

Source: https://portswigger.net/burp/releases/professional-community-2020-6
Fetched: 2026-06-28T09:16:33.766035+00:00

This release adds an option for using HTTP/2 and provides several minor improvements and bug fixes.

Experimental HTTP/2 support

This release provides experimental support for HTTP/2. From the "Project settings" > "HTTP" tab, you can now choose to use HTTP/2 for inbound and outbound communication over TLS.

As this is still an experimental feature, please use it at your own discretion.

Other improvements

You can now control the TLS protocols that Burp Proxy will use when performing TLS negotiation with the browser. You can configure Burp Proxy to use the default protocols of your Java installation, or override these defaults and enable custom protocols as required.

Bug fixes

In the HTTP history, you can now hover the mouse over URL encoded data to show the decoded data in a tooltip. Previously, this worked in Burp Repeater but not the "Proxy" > "HTTP history" tab.
