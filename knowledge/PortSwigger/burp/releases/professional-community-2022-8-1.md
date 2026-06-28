# Professional / Community 2022.8.1

Source: https://portswigger.net/burp/releases/professional-community-2022-8-1
Fetched: 2026-06-28T09:16:38.998814+00:00

This release provides new scan checks based on James Kettle's Browser-Powered Desync Attacks, first presented at Black Hat USA 2022. It also introduces the new capabilities for Burp Repeater that enable you test for these vulnerabilities manually.

New scan checks for client-side desync and CL.0 request smuggling

Burp Scanner now reports client-side desync vulnerabilities. We've also upgraded our existing HTTP request smuggling checks to detect CL.0 vulnerabilities.

For more details on both of these issues, check out James's whitepaper and the new Web Security Academy content.

Send a sequence of requests in Burp Repeater

You can now send the requests from a group of Repeater tabs as an automated sequence. When viewing a tab that belongs to a group, there is now a drop-down menu next to the Send button that lets you choose how your request sequence is sent. You can either send all of the requests over a single connection or use a separate connection for each request.

Sending requests over a single connection enables you to test for client-side desync vulnerabilities. For more information about how to do this, as well as some deliberately vulnerable labs for you to practice on, check out the new content on the Web Security Academy.

Sending over a single connection is also useful for timing-based attacks that rely on being able to compare responses with very small differences in timings as it reduces the "jitter" that can occur when establishing TCP connections.

Sending requests over separate connections is primarily useful when testing for vulnerabilities that require a multi-step process.

Adjusted issue severity - External service interaction (DNS)

Burp Scanner uses OAST techniques to identify critical vulnerabilities via DNS pingbacks to Burp Collaborator. Both the DNS interaction itself and the identified vulnerability are reported as separate issues. In some cases, such as when testing for SSRF, we may induce the application to perform a DNS lookup without this leading to the discovery of any further vulnerability. To better reflect this latter scenario, we have adjusted the severity of the External service interaction (DNS) issue.

We previously classed this as a high-severity issue on the assumption that a corresponding HTTP request was probably sent by the server, but subsequently blocked by a firewall's egress filters. Although we can't detect this externally, it could still provide a vector for pivoting attacks against the internal network.

However, we've increasingly encountered cases where systems perform a DNS lookup with no intention of ever connecting to the remote host, meaning that no HTTP request ever existed. For example, this could be triggered simply by adding a URL as the key of a Java Map.

This behavior can still indicate a serious vulnerability, and is worthy of further investigation, but we have reduced the reported severity to reflect the typical impact.

Handling changes for Unknown Host errors

Previously, Burp Scanner automatically terminated audits if it encountered Unknown Host errors, even if the scan scope also included separate, valid domains. Unknown host errors are now treated in the same way as other scanner errors, and the audit does not automatically terminate if one is encountered.

Browser upgrade

We have upgraded Burp's browser to Chromium 104.0.5112.79.

Bug fixes

This release also provides some minor bug fixes, including:

You can now use shift-click to select any tabs on the Create new group dialog. Previously, this functionality did not work with preselected tabs.

We have fixed an issue whereby tab groupings were being lost if you selected Save in-scope items only on projects with groups where some of the group's tabs were in-scope and some were not.

We have fixed a bug whereby under certain circumstances Burp Scanner was not detecting a multiple content type issue for responses with multiple Content-Type headers.

We have fixed a bug whereby scans were hanging during the crawl phase if they could not find any reachable destinations to scan.
