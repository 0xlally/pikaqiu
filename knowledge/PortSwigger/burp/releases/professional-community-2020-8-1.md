# Professional / Community 2020.8.1

Source: https://portswigger.net/burp/releases/professional-community-2020-8-1
Fetched: 2026-06-28T09:16:34.187677+00:00

After several months of live testing, we are pleased to announce that this release enables browser-powered scanning by default.

Browser-powered scanning

By default, Burp Scanner will now perform all navigation using an embedded Chromium browser, during both crawl and audit. This approach enables the scanner to accurately handle JavaScript and other navigational structures that modern browsers can. This has the potential to dramatically improve the coverage of the scan during both the crawl and audit phases.

To run browser-powered scanning efficiently, we recommend a machine with at least 2 CPU cores and 8 GB RAM. Burp Scanner automatically checks whether your machine appears to meet these requirements and will use the embedded browser if possible. Otherwise, scans will revert to the previous crawling engine.

If you prefer, you can also manually enable/disable browser-powered scanning in your scan configuration. You can find this option under "Crawl options" > "Miscellaneous" > "Embedded browser options".

Note: Browser-powered scanning currently remains off by default for Burp Suite Enterprise Edition.

Other improvements

Scan performance has been improved by reducing the number of duplicate locations that are scanned. Even when you choose to scan a URL using both HTTP and HTTPS, if Burp identifies that the content is the same, it will now only crawl and audit the location once.

SVG images are now displayed correctly on the "Render" tab.

The HTTP message editor now supports pretty printing of the content type image/svg+xml.

The embedded browser has been upgraded to Chromium 84.0.4147.125.
