# Professional / Community 2022.2.3

Source: https://portswigger.net/burp/releases/professional-community-2022-2-3
Fetched: 2026-06-28T09:16:37.339982+00:00

This release enables ultra-fast crawling of static content, enhanced scanning of single-page applications, as well as several bug fixes.

Ultra-fast crawling of static content

Burp Scanner's Fastest crawl strategy is now optimized for crawling static sites as quickly as possible. We have achieved this by disabling features that are irrelevant for static content, such as automated session handling and state recovery.

To give you a rough idea of the savings, these changes reduce the time taken to crawl our static documentation site from around 45 minutes to well under 10 minutes.

For the long-time Burp users out there, this strategy is effectively an improved version of the Spider tool from Burp Suite 1.7, emulated using the new crawling engine.

Improved scanning of single-page applications

This release greatly enhances Burp Scanner's ability to handle single-page applications (SPAs) built on frameworks like React.

The crawler can now recognize when a website uses URL fragments for client-side routing and adjust its behavior accordingly. This enables it to successfully scan content that is reached without sending additional requests to the server.

The crawler can now identify API calls triggered when the browser renders components on the page and send them for audit if necessary.

Security fix

Several months ago, we fixed an HTML injection vulnerability that could result in Burp Suite sending requests that did not respect its upstream proxy configuration. This could leak NetNTLM hashes on Windows systems that failed to block outbound SMB. This issue was caused by Swing GUI components that were insecurely configured to render HTML.

This release provides additional mitigation that prevents BApps from introducing this vulnerability even if they contain Swing components that allow HTML rendering.

This issue was reported via our bug bounty program.

Browser upgrade

We have upgraded Burp's browser to Chromium 99.0.4844.51.

Bug fixes

We have also fixed several minor bugs. Most notably, we have:

Resolved an issue that caused some Windows users to see a "No JVM found on your system" error when restarting Burp after an update.

Fixed an issue that meant recorded login sequences were sometimes cut short when testing them.
