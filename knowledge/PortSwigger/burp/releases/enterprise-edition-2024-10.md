# Enterprise Edition 2024.10

Source: https://portswigger.net/burp/releases/enterprise-edition-2024-10
Fetched: 2026-06-28T09:16:20.053449+00:00

This release gives you better visibility of the crawl paths found by Burp Scanner, introduces support for sharing issues with Splunk, and enables you to use custom extensions, BChecks, and BApps with CI-driven scans. We've also added partial support for scanning OpenAPI 3.1.x definitions.

Enhanced crawl path visibility

We've enhanced the visibility of the crawl paths discovered by Burp Scanner. When you review your scan results, you can now see a list of all the URLs that were discovered by Burp Scanner during the crawl phase, along with a status showing whether the URL was audited and, if not, why.

This gives you:

A deeper understanding of the crawl and audit phases of your scans.

Increased confidence in the level of coverage you're achieving.

Help when troubleshooting your scan configurations, if any of your URLs aren't being audited.

For more information, see Reviewing discovered URLs.

Integration with Splunk

If you use Splunk for your Security Information and Event Management (SIEM), you can now integrate this with Burp Suite Enterprise Edition.

This enables you to stream issues directly to Splunk for advanced analysis, enabling real-time monitoring and event management.

Using custom extensions, BChecks, and BApps with CI-driven scans

You can now use trusted custom extensions, BChecks, and BApps with CI-driven scans. This enables you to implement custom scan behaviors and capabilities.

Partial support for scanning OpenAPI 3.1.x definitions

Burp Scanner now includes limited support for scanning OpenAPI version 3.1.x definitions, giving you broader security coverage.

While many 3.1.x definitions are able to be scanned successfully, those that include specific 3.1.x features may not be supported. For best compatibility, we recommend using definitions that align closely with OpenAPI 3.0 standards.
