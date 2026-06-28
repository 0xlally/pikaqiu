# Professional / Community 2024.4.4

Source: https://portswigger.net/burp/releases/professional-community-2024-4-4
Fetched: 2026-06-28T09:16:47.793228+00:00

This release introduces several new features for Burp Scanner, including prioritization of audit items, the ability to configure authentication on API endpoints, and a new web cache deception scan check. We have also made some performance improvements.

Audit prioritization

Burp Scanner now prioritizes audit items before running an audit. This helps the scan to find key vulnerabilities earlier, improving consistency and coverage even in short, time-limited scans.

Burp Scanner calculates a score for each audit item based on two properties:

Interest level assesses the likelihood of an item requiring further manual investigation based on action type, content type, and whether the item requires authentication.

Attack surface exposure focuses on the number of unique insertion points exposed by the audit item.

Note that because items are now audited in a different order you may notice a change in the appearance of scan results.

For a detailed explanation of how audit prioritization works, see the documentation.

API scanning improvements

This release introduces new features for API scanning that give you the ability to configure endpoint authentication and view the parameters that will be scanned.

Authentication for API scanning

You can now configure endpoint authentication for API scans in the API details > Authentication tab of the API scan launcher. This enables Burp Scanner to access authenticated endpoints, increasing your scanning coverage. Burp Scanner currently supports the following authentication types:

Basic authentication

API key authentication

Bearer authentication

Burp automatically detects authentication methods that are linked to specific endpoints in your OpenAPI definition. In addition, you can add authentication methods that aren't detected in the OpenAPI definition.

For a detailed explanation of how authentication for API scanning works, see the documentation.

Viewing API parameters

For scans initiated with an API specification, Burp Scanner now features a Parameters tab within the API details. This helps you see all the endpoints' parameters, including their names, values, descriptions, and where they appear in an HTTP request. Burp Scanner uses these parameter details to figure out how to properly request information when it's checking an endpoint, making it simpler for you to get a clear picture of what's being scanned. If the API definition doesn't have example values, Burp Scanner will generate them.

Web cache deception scan check

Burp Scanner can now check for web cache deception. Web cache deception is a security vulnerability in which attackers manipulate URL paths to trick web caches into storing and serving dynamic content as if it were static, leading to unauthorized disclosure of sensitive data. This occurs when caches misinterpret URLs that have been manipulated, for example by appending a fake file extension to a dynamic URL, and store sensitive information that can then be accessed by unauthorized users.

Crawler request filtering

The crawler now determines if a request is going to an advertising or tracking domain. These requests are automatically dropped, helping to improve performance by filtering out unnecessary traffic.

If required, you can still crawl these domains by adding them to the scan scope.

Performance improvements

We're working on a number of performance improvements. In this release, we've made the following improvements:

By default, Burp now reuses HTTP/1 connections for outbound requests from the proxy. This may improve browser load times. Please let us know if you experience any issues with this feature. You can also disable Use keep-alive for HTTP/1 if the server supports it in the Settings menu, under Proxy > Miscellaneous.

We've fixed an issue that caused the Proxy history to lag when quickly switching between results in the table.

Quality of life improvements

We've made the following improvements:

We've added an Uninteresting headers user setting. This enables you to choose whether Burp's default behavior is to show or hide uninteresting headers in the Pretty tab of the message editor. You can set this once and it applies to all new editors across all Burp installations on your machine.

We've changed the way the site map organizes content. The tree view is now organized alphabetically, first by root domain and then by subdomain. This places sibling domains beside each other, making it easier to navigate.

Search results in Repeater now show the relevant Repeater tab number and history item number. You can now right-click a result and select Go to Repeater tab to quickly switch to the relevant request / response pair.

Bug fixes

We fixed the following issues:

We fixed a bug where Burp wasn't using its own network settings when fetching URLs in the API scan launcher. This meant that you weren't able to upload API definitions if the host servers required specific network configurations. Burp now applies all network settings that are specified. This enables you to upload API definitions from URLs that use self-signed certificates or an upstream proxy, for example.

We fixed a bug that caused Burp to consume a large amount of memory when dealing with requests with a high number of insertion points.

We fixed a bug that caused isolated scans to use the global host history. This prevented some items from being scanned, if they were scanned due to other tasks.

We re-added the Extensions context menu option to issues on the All issues page. This was removed in error.

We've fixed JavaScript regex checks, which were occasionally timing out on complex regular expressions.

We have fixed a bug whereby custom table columns stopped returning new values after encountering a null value. Null values are now calculated and displayed.

Java upgrade

Burp now uses Java 21.0.2, enhancing both performance and security.

Browser upgrade

We've upgraded Burp's built-in browser to 125.0.6422.60 for Linux, Windows, and MacOS. For more information, see the Chromium release notes.
