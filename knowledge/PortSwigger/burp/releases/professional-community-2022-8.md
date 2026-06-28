# Professional / Community 2022.8

Source: https://portswigger.net/burp/releases/professional-community-2022-8
Fetched: 2026-06-28T09:16:38.796670+00:00

This release introduces the ability to send all of the requests in a group of Repeater tabs sequentially with a single click. It also updates the Scanner's listed issue severity for External service interaction (DNS) issues and provides various minor bug fixes.

Send a sequence of requests in Burp Repeater

You can now send the requests from a group of Repeater tabs as an automated sequence. When you select a tab that is in a group, the Send button now displays a drop-down menu from which you can choose how your requests are sent. You can either send all of the requests over one single connection or use a separate connection for each request.

Sending over a single connection is useful for timing-based attacks that rely on being able to compare responses with very small differences in timings, as it reduces the "jitter" that can occur when establishing TCP connections.

Sending over separate connections is primarily useful when testing for vulnerabilities that require a multi-step sequence to be performed.

Adjusted issue severity - External service interaction (DNS)

Burp Scanner uses OAST techniques to identify critical vulnerabilities via DNS pingbacks to Burp Collaborator. Both the DNS interaction itself and the identified vulnerability are reported as separate issues. In some cases, such as when testing for SSRF, we may induce the application to perform a DNS lookup without this leading to the discovery of any further vulnerability. To better reflect this latter scenario, we have adjusted the severity of the External service interaction (DNS) issue.

We previously classed this as a high-severity issue on the assumption that a corresponding HTTP request was probably sent by the server, but subsequently blocked by a firewall's egress filters. Although we can't detect this externally, it could still provide a vector for pivoting attacks against the internal network.

However, we've increasingly encountered cases where systems perform a DNS lookup with no intention of ever connecting to the remote host, meaning that no HTTP request ever existed. For example, this could be triggered simply by adding a URL as the key of a Java Map.

This behavior can still indicate a serious vulnerability, and is worthy of further investigation, but we have reduced the reported severity to reflect the typical impact.

Browser upgrade

We have upgraded Burp's browser to Chromium 103.0.5060.134.

Bug fixes

This release also provides some minor bug fixes, including:

You can now use shift-click to select any tabs on the Create new group dialog. Previously, this functionality did not work with preselected tabs.

We have fixed an issue whereby tab groupings were being lost if you selected Save in-scope items only on projects with groups where some of the group's tabs were in-scope and some were not.

We have fixed a bug whereby under certain circumstances Burp Scanner was not detecting a multiple content type issue for responses with multiple Content-Type headers.

We have fixed a bug whereby scans were hanging during the crawl phase if they could not find any reachable destinations to scan.
