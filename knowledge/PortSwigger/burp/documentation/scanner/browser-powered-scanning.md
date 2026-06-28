# Browser-powered scanning

Source: https://portswigger.net/burp/documentation/scanner/browser-powered-scanning
Fetched: 2026-06-28T09:16:10.907479+00:00

Support Center

Documentation

Scanner

Browser-powered scanning

DASTProfessional

Browser-powered scanning

Last updated:

June 18, 2026

Read time:

1 Minute

By default, Burp Scanner uses an embedded Chromium browser to navigate during both the crawl and audit phases of a scan. This enables it to accurately handle virtually any client-side technology that a modern browser can, which offers dramatically increased coverage compared to a regular crawler engine.

Use cases for browser-powered scanning

Browser-powered scanning enables you to test modern websites comprehensively. For example, some websites have a dynamically generated UI that is not present in raw HTML. A regular crawler engine would miss key vulnerabilities as it would be unable to render the full content. Burp Scanner is able to load the page and execute any scripts required to build the UI, before continuing to crawl as normal.

Browser-powered scans can also handle websites that send requests on-the-fly using JavaScript event handlers. Burp Scanner uses its browser to trigger the relevant events and execute the corresponding script, issuing any requests as needed.

When using browser-powered scanning, you can also record and upload full login sequences. This means that Burp Scanner can handle complex login mechanisms, including single sign-on.

Related pages

Browser-powered scanning for Burp Suite DAST.

Recorded login sequences.
