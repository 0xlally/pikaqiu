# Enterprise Edition 2023.2

Source: https://portswigger.net/burp/releases/enterprise-edition-2023-2
Fetched: 2026-06-28T09:16:18.838906+00:00

This release enables you to configure the scan settings for all the sites in a folder at once. We've also made some other improvements.

If you're using a Kubernetes deployment, you'll need to upload your license key after you install this update. This is a one-time action and won't be necessary for future updates. For more information, see Activating your license.

Configure scan settings for sites at the folder level

We've enabled you to configure scan settings for sites at the folder level. You can apply these settings to all the subfolders and sites in the folder, which means you can quickly make adjustments to a large number of sites. You can then fine-tune the scan settings for individual subfolders or sites.

Burp Scanner combines any scan configurations that you set at the folder, subfolder, and site levels. To get the most out of this new functionality, it's important to understand exactly how Burp Scanner combines scan configurations. For more information, see Defining the scan configuration for a folder.

Improvements to Burp Scanner

This release includes several minor improvements to authenticated crawling with popup-based login mechanisms:

We have added a wait after the final event in a recorded sequence. This means that the sequence now captures links that are added by the final page after a delay.

When you log in after receiving a temporary failure status code, Burp Scanner now authenticates subsequent requests for the same resource.

Other improvements

We've also made the following improvements:

We've added a Create custom configuration button. This enables you to quickly create a new configuration when you go to Scan settings > Scan configuration.

We've added support for SQL Server 2022, for external databases.

We've reduced the amount of noise that recorded logins produce in the health check logs.
