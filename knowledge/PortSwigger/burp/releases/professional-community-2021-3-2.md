# Professional / Community 2021.3.2

Source: https://portswigger.net/burp/releases/professional-community-2021-3-2
Fetched: 2026-06-28T09:16:35.001601+00:00

This release strengthens support for HTTP/2 and turns it on by default. It also fixes several bugs.

HTTP/2 support

We have strengthened support for HTTP/2 within Burp Suite. HTTP/2 support is now turned on by default and is no longer considered experimental. Burp will interact with targets via HTTP/2 when a target supports it.

HTTP/2 support brings a significant performance improvement to the network layer, benefiting Scanner and Intruder speed. It also provides future compatibility with any site that no longer supports HTTP/1.1.

If you prefer not to use HTTP/2, you can disable its use under Project Options / HTTP.

Bug fixes

This release provides several minor improvements and bug fixes, including:

The crawler no longer produces an error when it encounters request bodies that contain JSON literals when it is crawling OpenAPI definitions.

Burp Suite now shuts down correctly on macOS.

The number of characters selected now shows in the message inspector when selecting non-editable messages.

Custom menu items added by extensions are now shown in a sub-menu of the context menu, to avoid cluttering.

The hash algorithm list within Burp Decoder is now sorted alphanumerically.

The resource pool button is now disabled when configuring a live passive crawl, as this crawl does not make requests.

The automatic backup progress dialog box no longer appears if Burp Suite is minimized.
