# Enterprise Edition 2022.10

Source: https://portswigger.net/burp/releases/enterprise-edition-2022-10
Fetched: 2026-06-28T09:16:17.747630+00:00

This release enables you to view a replay of your recorded login sequences, so that you can make sure that Burp Scanner can log in successfully. We've also introduced improvements to license key renewals, so you don't have to enter them manually.

Recorded login replays

We've introduced recorded login replays as part of a site health check. When you run a health check, Burp Suite Enterprise Edition performs a connection check for your site URLs and runs any recorded login scripts that you've saved.

We capture screenshots when the recorded login scripts run, which you can manually review to make sure that each script logs in successfully.

Rolling license key renewals

If you renew your Burp Suite Enterprise Edition license before it expires, we now automatically update your license key information. You no longer need to enter the details manually.

Bug fixes

We've fixed some minor bugs.
