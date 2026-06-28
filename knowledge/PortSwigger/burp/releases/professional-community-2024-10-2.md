# Professional / Community 2024.10.2

Source: https://portswigger.net/burp/releases/professional-community-2024-10-2
Fetched: 2026-06-28T09:16:45.223843+00:00

This release introduces a streamlined Intruder layout with customizable settings, a combined scan launcher for web apps and APIs, support for SOAP authentication, partial scanning support for OpenAPI 3.1.x definitions, and the ability to customize which HTTP headers appear in the message editor. We’ve also made several quality of life improvements and some bug fixes.

Streamlined layout for Burp Intruder

We've added a Default Intruder side panel layout setting. This enables you to customize the Intruder sidebar independently from other sidebars in Burp, giving you more control over your Intruder workspace layout.

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

We’ve added the the ability to filter the Collaborator results table by network protocol, making it easier to find specific interactions even in large amounts of data.

We’ve added a Drop all button to Proxy Intercept, enabling you to quickly clear irrelevant traffic and minimize clutter.

We’ve added the Default Proxy history message type setting to the Settings dialog, enabling you to set whether the Proxy history message editor displays auto-modified, manually edited, or original messages by default.

We’ve disabled the Google Lens overlay in Burp’s browser, improving user privacy by reducing the chance of accidental data transmission to Google, and providing a cleaner interface.

We’ve improved the Hex tab of the message editor for a more efficient editing experience:

You can now overwrite values in cells directly instead of appending to existing data.

You can now input up to two characters per cell to maintain proper byte formatting.

You can now press Enter after editing a cell to select the next cell horizontally.

Bug fixes

We've fixed the following bugs:

A bug preventing editing of extension-driven active audit tasks.

A bug preventing browser resources from being released immediately after completion of each crawl segment.

A bug causing changes made by extensions to intercepted requests from being correctly applied.

A bug preventing scan issues from being deleted in isolated scans.

An issue on Windows preventing Intruder attacks from starting if the attack configuration was copied from a previous tab with payload encoding enabled but no encoding characters specified.

Browser upgrade

We've upgraded Burp's browser to Chromium 131.0.6778.86 for Windows & Mac and 131.0.6778.85 for Linux. For more information, see the Chromium release notes.
