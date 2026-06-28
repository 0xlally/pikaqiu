# Professional / Community 2024.10

Source: https://portswigger.net/burp/releases/professional-community-2024-10
Fetched: 2026-06-28T09:16:45.542192+00:00

This release introduces a combined scan launcher for web app and API-only scans, the ability to customize which headers appear in the message editor, support for SOAP authentication, and several quality of life improvements.

Combined scan launcher for web apps and APIs

You can now select the type of scan you want to run from the scan launcher, rather than choosing between a web application scan or an API scan on the Dashboard.

If you select Crawl or Crawl and audit, Burp automatically catalogs and analyzes the application's structure and traffic, including any OpenAPI, SOAP, or GraphQL APIs that it discovers. If you select API-only scan, Burp performs an audit based on an OpenAPI definition or SOAP WSDL that you provide.

Support for SOAP authentication

You can now configure authentication for SOAP APIs. Add your authentication methods and credentials in the API details > Authentication tab of the scan launcher to give Burp Scanner access to restricted endpoints and increase scanning coverage for your SOAP APIs.

Customize which HTTP request headers appear in the message editor

We've introduced the ability to customize the list of HTTP request headers in the Uninteresting headers setting. This gives you fine-tuned control over which headers are hidden by Burp in the Pretty tab of the message editor.

Partial support for scanning OpenAPI version 3.1.x definitions

Burp Scanner now includes limited support for scanning OpenAPI version 3.1.x definitions, giving you broader security coverage.

While many 3.1.x definitions are able to be scanned successfully, those that include specific 3.1.x features may not be supported. For best compatibility, we recommend using definitions that align closely with OpenAPI 3.0 standards.

Please note, this feature is currently only available in Burp Suite Professional.

Quality of life improvements

We've made the following quality of life improvements:

You can now filter the Collaborator results table by network protocol. This enables you to find specific interactions more easily in a large amount of data.

We've added a Drop all button to Proxy Intercept, enabling you to quickly clear irrelevant traffic and minimize clutter.

We've added the Default Proxy history message type setting to the Settings dialog. This enables you to set whether the Proxy history message editor displays auto-modified, manually edited, or original messages by default.

We’ve disabled the Google Lens overlay in Burp’s browser. This improves user privacy by reducing the chance of accidental data transmission to Google, and also provides a cleaner interface.

Burp Suite now reuses Chromium’s default User-Agent header, improving compatibility with websites that use bot detection. This update reduces the likelihood of requests being blocked by services like Cloudflare.

We've made several improvements to the Hex tab of the message editor for a more efficient editing experience:

You can now overwrite values in cells directly instead of appending to existing data.

The hex editor now limits input to two characters per cell to maintain proper byte formatting.

Pressing Enter after editing a cell now selects the next cell horizontally.

Bug fixes

We've fixed the following bugs:

We've fixed an issue where changes made by extensions to intercepted requests weren’t correctly applied.

We've fixed a bug where scan issues couldn't be deleted from isolated scans.

Browser upgrade

We've upgraded Burp's browser to Chromium 130.0.6723.70 for Windows & Mac and 130.0.6723.69 for Linux. For more information, see the Chromium release notes.
