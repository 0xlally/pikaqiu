# Professional / Community 2020.12

Source: https://portswigger.net/burp/releases/professional-community-2020-12
Fetched: 2026-06-28T09:16:33.920689+00:00

This release provides the following improvements and bug fixes:

Dynamic switching between UI themes

When switching between the new light and dark themes in the display settings, you no longer have to restart Burp before this change is applied.

Scan URLs with fragments

You can now include fragments (#) in the seed URLs you specify for a scan. Note that this is only supported by browser-powered scans. If the "Use embedded browser for Crawl and Audit" option is disabled in your scan configuration, you will not be able to start a scan with seed URLs containing fragments.

Embedded browser upgrade

Burp’s embedded browser has been upgraded to Chromium 87.0.4280.88.

User interface improvements

The icons and icon colors for issue severity levels have changed. We've also adjusted the background color for the Suite tab bar, in both the light and dark themes.

Security fix

We have fixed a vulnerability that could result in Burp Suite issuing requests that do not respect its upstream proxy configuration and could leak NetNTLM hashes on Windows systems that fail to block outbound SMB.

This issue was reported through our bug bounty program.

Bug fixes

This release also provides the following bug fixes:

Copying an intercepted request as a curl command no longer introduces duplicate Cookie headers.

As long as your user has permission to use the selected port, you are no longer prevented from binding the proxy listener to ports < 1024. Previously, a bug meant that only root / super users could bind the listener to these ports.

During scans, the crawler no longer uses cookies from Burp's cookie jar when sending requests.

Users can once again paste content into the message editor of the Extensions tab.
