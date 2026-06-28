# Professional / Community 2022.9

Source: https://portswigger.net/burp/releases/professional-community-2022-9
Fetched: 2026-06-28T09:16:38.921950+00:00

This release introduces an all-new API. It also includes improvements to the Burp Collaborator client and active request throttling for Burp Scanner.

Montoya API

We have released the Montoya API, an all-new API that enables you to develop extensions for Burp Suite. The new API offers a more modern design than the existing Wiener API, making it easier to use and enabling us to add future features that we could not have supported with the old API.

This change will not affect any current BApps, and the existing Wiener API will continue to work as normal for the immediate future. However, we strongly recommend that you write any new extensions using the new Montoya API, as we will eventually end support for the Wiener API.

The Montoya API offers all of the same features as the existing version. For reference information, see the API GitHub page.

Collaborator client improvements

This release introduces various usability improvements for the Burp Collaborator client, including:

We have moved the client from the Burp menu to its own top-level tab.

You can now open multiple Collaborator client tabs, enabling you to track interactions from multiple payloads in separate tables.

Collaborator interactions are now persisted in the project file, meaning that any interactions in the table are retained if you close and reopen your project. You can also now save Collaborator interaction data directly to your project file.

You can now insert a Collaborator payload in the message editor by selecting Insert Collaborator payload from the context menu. This pastes in a new ID from the most recently-created Collaborator client tab.

The interaction table now displays interaction timings in milliseconds and the source IP of the interaction.

Automatic license key updates

Renewed license keys now update automatically. If your existing license is expiring or has expired altogether, Burp Suite automatically checks your account for a renewed license key. If you have a renewed key associated with your account, then the system retrieves and activates that key.

Please note that you will need to allow network access to https://portswigger.net for this process to work.

Adaptive request throttling for Burp Scanner

When Burp Scanner receives a 429 response due to sending too many requests in quick succession, it now incrementally adds a short delay between requests until it complies with the server's rate limit. This enables the scan to continue as normal, albeit with an increased duration.

If you prefer, you can disable this behavior using a custom scan configuration - just go to Request throttling configuration and deselect Adaptive request throttling.
