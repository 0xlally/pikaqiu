# Professional / Community 2024.7.5

Source: https://portswigger.net/burp/releases/professional-community-2024-7-5
Fetched: 2026-06-28T09:16:48.619067+00:00

This release introduces major performance upgrades, significant enhancements to our Intercept feature, and a new Scanned insertion points column to the Audit items table. We’ve expanded our OpenAPI scanning to include endpoints that require HTTP headers, and added a toggle for Site map views. We've also made some quality of life improvements, fixed some bugs, and updated the Montoya API.

Major performance improvements

We've made the following substantial performance improvements:

Large responses now display much faster and use less memory.

Burp Suite's interface is no longer laggy when working with project files containing large numbers of Repeater tabs. This change also reduces memory consumption and project load time.

We've optimized page info retrieval from Chromium, reducing scan times and resource usage.

Improved Proxy Intercept

We’ve given Burp’s Intercept feature a major upgrade. Now, intercepted messages are listed in the order they were sent, making it easier to manage high volumes of traffic. You can edit, forward, or drop messages in any order you like, and even manage them in bulk. Working with intercepted traffic is now much quicker and easier.

Scanned insertion points column added to Audit items table

We've added a Scanned insertion points column to the Audit items table, showing the count of audited and light audited insertion points. This helps keep track of scan progress and provides more information about the insertion points that have been audited.

Scanning API endpoints with required HTTP headers

We've expanded Burp Scanner's OpenAPI scanning capabilities to include endpoints with required HTTP headers.

Updated site map: URL view and Crawl paths view

We've integrated Crawl paths into the Site map tab and added a toggle, enabling you to switch between the URL view and the Crawl paths view within the same tab. We've also added icons to the Crawl paths view to represent the different actions taken by Burp Scanner during a crawl. This makes it easier to read as it feels less cluttered.

Quality of life improvements

We've made the following quality of life improvements:

JSON editing in the Message editor's Pretty tab is now easier as we've improved JSON text completion to avoid unnecessary insertions.

Burp can now parse poorly formed JSON in OpenAPI definitions better, including comments and trailing commas.

Montoya API

We've made the following improvements to our Montoya API:

Added new utility methods to enable JSON parsing.

Added RedirectionMode to RequestOptions so that redirection behavior can be specified for Montoya-issued requests.

Added functionality for retrieving the current project file name.

Added bulk management of headers in HttpRequest and HttpResponse.

Added functionality to check if intercept is currently on or off.

Added support for line wrapping and displaying non-printable characters in the Message editor's Raw tab.

Added functionality to specify the new tab name when sending requests to Intruder.

Included a Changelog to the Montoya API repository.

Bug fixes

We've fixed the following bugs:

A bug causing long parsing times and high memory usage for OpenAPI definitions with deeply nested schemas.

A bug causing Burp Scanner to report CSP headers with sandbox directive values as malformed.

A bug preventing Boolean parameters at an API endpoint from being populated when scanning - they will now be assigned a random true or false value.

The Proxy > Intercept table no longer fails to select the next message after dropping or forwarding a message.

Content is no longer removed from responses in Repeater when pretty print is disabled.

We fixed a bug where Repeater tabs created through the Montoya API were sometimes blank or missing the message editor.

We fixed a bug where hotkeys sometimes didn't work in the message editor.

Java update

We've updated Java from 21.0.3 to 21.0.4.
