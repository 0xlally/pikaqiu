# Professional / Community 2022.7

Source: https://portswigger.net/burp/releases/professional-community-2022-7
Fetched: 2026-06-28T09:16:38.668545+00:00

This release introduces tab-specific options in Repeater and client-side prototype pollution reporting in Burp Scanner. It also provides a change to the way Burp's browser handles the User-Agent header and a minor bug fix.

Tab-specific options in Repeater

You can now set tab-specific Repeater options, giving you finer control over how Repeater behaves when sending requests and receiving responses. To configure tab-specific options, click the new settings icon next to the Send button.

If you select specific options for a tab then Repeater ignores the global settings for that tab altogether. You can return a tab to global settings by clicking the new Restore global defaults button. This button is highlighted when a tab has specific settings configured.

Client-side prototype pollution reporting in Burp Scanner

Burp Scanner can now detect client-side prototype pollution. For more information on this vulnerability, see the new "Client side prototype pollution" issue definition that has been added to the Target > Issue definitions page.

Changes to User-Agent header handling

We have amended Burp's browser so that it respects the configured User-Agent header when scanning rather than generating a random User-Agent string. The original approach was used as a means of tracking requests, but is no longer needed.

Browser upgrade

We have upgraded Burp's browser to Chromium 103.0.5060.114.

Bug fix

We have fixed a bug whereby dynamic analysis was frequently timing out due to the system not factoring in the time that the page took to load. The dynamic analysis timer now starts once the page is loaded and the analysis itself starts.
