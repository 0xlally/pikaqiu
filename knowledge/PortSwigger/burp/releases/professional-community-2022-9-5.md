# Professional / Community 2022.9.5

Source: https://portswigger.net/burp/releases/professional-community-2022-9-5
Fetched: 2026-06-28T09:16:39.527772+00:00

This release introduces the Montoya API, an all-new replacement for the Wiener API. It also includes improvements to the Burp Collaborator client and adaptive request throttling for Burp Scanner.

Montoya API

We have released the Montoya API, an all-new API that enables you to develop extensions for Burp Suite. The new API offers a more modern design than the existing Wiener API, making it easier to use and enabling us to add future features that we could not have supported with the old API.

This change will not affect any current BApps, and the existing Wiener API will continue to work as normal for the immediate future. However, we strongly recommend that you write any new extensions using the new Montoya API, as we will eventually end support for the Wiener API.

The Montoya API offers all of the same features as the existing version. It also includes several new features, such as:

New methods to create, modify, and delete request / response headers.

The ability for an extension to query which edition of Burp (that is, Professional, Community Edition, or Enterprise Edition) it is currently running in.

The ability to generate Collaborator payloads from your own custom data.

The ability to export the secret key that the Collaborator uses for extensions and restore a previous Collaborator client session from it.

New utilities to generate random sequences and manipulate byte arrays.

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

If you prefer, you can disable this behavior using a custom scan configuration - just go to Request throttling configuration and deselect Automatic backoff.

Security patch

We have fixed an HTML injection vulnerability that could be triggered by attackers with direct access to the proxy listener. Note that the proxy listener only accepts connections from localhost by default. This issue was privately reported via our bug bounty program.

Browser upgrade

We have upgraded Burp's browser to Chromium 107.0.5304.62, which fixes a number of high-severity security issues.

Bug fixes

We have also fixed some minor bugs, including:

Previously, you could still use the Collaborator client to generate payloads and poll manually even if the Collaborator was disabled in the project options. We have now amended this so that disabling the Collaborator disables all of the Collaborator client's functions.

We have fixed a bug whereby disabling the Collaborator did not stop the Collaborator client from polling for payloads that had already been created.

We have fixed a bug whereby the Learn More link on the Collaborator client tab was pointing to an invalid URL.

We have fixed a bug that prevented the crawler from handling links that are added to a page by JavaScript following a delay.

We have fixed a bug whereby Burp Scanner was failing to find CSRF vulnerabilities on sites that return a 302 response when CSRF is exploited.

We have fixed a bug whereby Repeater was not identifying streaming responses correctly, meaning that the affected responses would never complete.

We have fixed a UI issue whereby checkboxes and radio buttons were not displaying correctly on the Extensions tab when using the Light display theme.
