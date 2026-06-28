# Enterprise Edition 2020.1

Source: https://portswigger.net/burp/releases/enterprise-edition-2020-1
Fetched: 2026-06-28T09:16:16.286494+00:00

This release contains a number of valuable enhancements.

There is a new scan configuration library that replicates the Burp Suite Pro feature. You can:

View and manage built-in and custom scan configurations.

Configure detailed settings for crawling and auditing, as well as platform authentication and upstream proxy settings.

Import and export configurations in JSON format.

For each scan, you can now view full details of the individual URLs that were scanned, together with the numbers of issues, requests, and insertion points. You can drill into each URL to view the details of individual issues:

You can now download the scan event log, via the "More actions" button on the scan results page.

There is a new database migration tool that lets you migrate from the bundled database to an external database. See documentation on database migration.

There are various other enhancements and bug fixes:

Estimates of scan time remaining are now based on the duration of the preceding scan where applicable.

Scans that have not made any progress for 24 hours will be automatically canceled.

Issue details can now be retrieved from the aggregated issues list for scans created through the REST API when the site is not saved in the Sites tree.

Hover action buttons on the Sites tree are now available for users belonging to groups that have site restrictions configured.
