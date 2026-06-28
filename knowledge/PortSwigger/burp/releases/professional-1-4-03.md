# Professional 1.4.03

Source: https://portswigger.net/burp/releases/professional-1-4-03
Fetched: 2026-06-28T09:16:24.109863+00:00

1. There is a new CSRF generator, which produces proof-of-concept HTML for generating virtually any HTTP request. You can access this feature by right-clicking any item within Burp, and using the engagement tools context menu to select "generate CSRF PoC":

Some useful features are:

Support for all form encoding types: standard URL encoding, multipart encoding, and plain text encoding.

Auto-detection of the optimal encoding type, with manual override.

Ability to edit both the request and response in-place, to fine tune attacks.

In-browser testing, by pasting a URL into your browser that will cause Burp Proxy to serve up the CSRF PoC in its response.

Using this feature, you can even generate CSRF attacks containing completely arbitrary content in the message body, including binary data, provided the target application accepts text/plain encoding.

2. You can now add comments and highlighting to items as they appear in the proxy intercept window. This is useful when manually stepping through an application, allowing you to annotate interesting requests as they are made, and then return to these in the proxy history for further investigation:

3. The site analyser function (accessible via the engagement tools context menu), now has a tab showing all the unique parameters found, and the number of URLs in which they appear. You can drill down into the individual requests that use a given parameter, allowing you to quickly focus in on interesting or unusual parameters when testing a large application:

4. You can now bind proxy listeners to specific IP addresses, in addition to the loopback interface and all interfaces:

5. Burp now implements sslstrip-style functionality, allowing you to use non-SSL-capable tools against HTTPS applications, or to perform active MITM attacks against users who begin browsing using HTTP:

You can force Burp Proxy to use HTTPS in outgoing requests, even if the incoming request did not use HTTPS. This is configured per-listener, in the request redirection settings.

You can configure Burp Proxy to convert all HTTPS links in responses and redirects to use HTTP.

You can configure Burp Proxy to remove the secure flag on set cookies, so that browsers will still submit them over HTTP.

6. The configuration UI for session handling rules and macros now includes "copy" buttons, allowing you to duplicate and modify an existing rule or macro.
