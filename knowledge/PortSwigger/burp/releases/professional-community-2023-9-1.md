# Professional / Community 2023.9.1

Source: https://portswigger.net/burp/releases/professional-community-2023-9-1
Fetched: 2026-06-28T09:16:44.410596+00:00

This release introduces new Repeater functionality based on the techniques discussed in James Kettle's talk "Smashing the State Machine: The True Potential of Web Race Conditions", first presented at Black Hat USA 2023. Repeater's new single-packet attack feature nullifies network jitter, enabling you to send multiple requests in parallel. These requests are synchronized to arrive within a very small time window, making it much simpler to test for race conditions.

We have also introduced various other improvements for Burp Suite Professional and Burp Scanner, including the ability to reuse HTTP/1 connections in Intruder, a new project-level Crawl paths tab in the Target tool, and support for GraphQL introspection during scans.

Repeater send group in parallel

We have added a Send group (parallel) option to Repeater's Group send options menu. When you select this option for a tab group, Repeater sends the requests from all of the group's tabs at once.

Repeater synchronizes parallel requests to ensure that they all arrive in full at the same time. It uses different synchronization techniques depending on the HTTP version used:

When sending over HTTP/2, Repeater sends the group using a single packet attack. This is where multiple requests are sent via a single TCP packet.

When sending over HTTP/1, Repeater uses last-byte synchronization. This is where multiple requests are sent over concurrent connections, but the last byte of each request in the group is withheld. After a short delay, these last bytes are sent down each connection simultaneously.

Sending synchronized requests in parallel makes it much easier to test for race conditions. For more information about how to do this, as well as some deliberately vulnerable labs for you to practice on, check out the Race conditions topic on the Web Security Academy.

For more information on sending Repeater groups in parallel, see Sending grouped HTTP requests.

Montoya API changes

As part of these new Repeater features, we have added two sendRequests methods to the Http interface. These methods enable you to build extensions that can send HTTP requests in parallel and retrieve their responses. You can also explicitly specify the HTTP mode that the requests should use, if required.

Reuse HTTP/1 connections in Intruder to speed up attacks

You can now control whether Intruder reuses connections to issue multiple HTTP/1 requests. This can greatly increase the speed of your attacks when using HTTP/1, as Burp does not need to open a new connection for each request and close it after receiving a response. Find this in Intruder > Settings > HTTP/1 connection reuse. For more information, see HTTP/1 connection reuse.

Safely open third-party project files

We've introduced a new startup setting that enables you to trust or untrust projects. If you deselect Trust this project, Burp can now remove potentially harmful settings that could be configured within project files.

This is especially useful if you are opening project files that came from unknown or untrusted sources. Find this setting on the startup wizard, or in Settings > Suite > Startup behavior > Unrecognized project files. For more information, see Startup behavior.

Specify intermediate CA certificates for hardware tokens and smart cards

You can now set intermediate certificates when you add a new PKCS#11 certificate for hardware token and smart cards. This enables you to test target applications that don't directly trust your intermediate CA. For more information, see Client TLS certificates.

Set custom SNI values in Repeater

You can now set custom SNI values in Repeater. This enables you to reproduce external service interaction issues detected by Scanner using Collaborator payloads within the SNI. For more information, see HTTP Repeater tab.

Project-level scan crawl paths

All scans in a project can now share crawl path information. This improves scan efficiency, enabling Burp Scanner to build on the paths it has already discovered as new scans are run.

As a result of this, we have added a new Crawl paths tab to the Target tool. This tab displays path information in the same way as the existing scan results Crawl path tab, but is populated by all scans rather than one individual scan. Any new scans that you run can draw on and add to the information displayed in this tab.

Isolated scans

As part of the global crawl path work, we have added a Run isolated scan option to the scan launcher. Results from isolated scans do not appear in the Target > Site map or Target > Crawl paths tabs. This feature is useful if you want to test settings without impacting "live" scan results, for example.

You can view site map and crawl path information for isolated scans from the Tasks > View details > Target tab. The information displayed on this tab applies to the selected scan task only.

GraphQL introspection

Burp Scanner can now run introspection queries on GraphQL endpoints to gain information on available queries and mutations. If the introspection query is successful, Burp Scanner sends further requests to each query and mutation discovered in an attempt to discover as much attack surface as possible. To enable GraphQL introspection, select the new Perform GraphQL introspection setting in the Miscellaneous section of the scan configuration.

If it does not find any GraphQL endpoints in the crawl, Burp Scanner can also now attempt to guess GraphQL endpoints using a list of common endpoint suffixes. To enable GraphQL endpoint guessing, select the new Test common GraphQL endpoints setting in the Miscellaneous section of the scan configuration.

Automatic scan throttling

We have added a new Automatic throttling setting to the Resource pool section of the scan launcher. You can now configure which HTTP response codes should cause Burp Scanner to introduce a short delay between requests. Previously, Burp Scanner could only throttle requests when the server responded with a HTTP 429 code.

Other Burp Scanner improvements

We have improved crawl optimization to reduce the chance of interesting content being missed. Specifically, Burp Scanner now treats clickables that are using the same event listener with different visible text as separate entities, and visits them all.

Bug fixes

We've fixed a number of minor bugs, including:

We've fixed an issue that was causing the Proxy response panel to freeze when inspecting a 200 response after inspecting a 302/400 response.

We've improved the reliability of the Send to Organizer function.

We've fixed an issue where requests / responses generated by Intruder in some older versions of Burp could not be seen in newer versions.

We have fixed a bug whereby the crawler was not always waiting for slow asynchronous queries that cause a DOM mutation to return. This was resulting in slow page loads and missing elements in certain circumstances.

We have fixed a bug whereby Burp Organizer items weren't retained when Burp was upgraded to the latest version.
