# Enterprise Edition 2023.8

Source: https://portswigger.net/burp/releases/enterprise-edition-2023-8
Fetched: 2026-06-28T09:16:19.771342+00:00

This release includes the introduction of user activity logging, and a number of other improvements.

User activity logging

You can now enable user activity logging to record user actions throughout Burp Suite Enterprise Edition. You can then download this log as a CSV file that contains a list of timestamped actions and successful logins.

Changes to scan settings

We've surfaced the Platform authentication and Upstream proxy servers settings in Scan settings to make them easier to find. Previously, these settings were available only for custom scan configurations.

Java update

Burp Suite Enterprise Edition now uses Java version 17.0.8.

Bug fixes

We've also fixed the following bugs:

Fixed an issue where the Linked tickets tab would not appear under some circumstances.

Fixed an issue that sometimes prevented Burp Suite from launching new scans.
