# Scans page

Source: https://portswigger.net/burp/documentation/dast/user-guide/reference/scans-page
Fetched: 2026-06-28T09:15:39.689337+00:00

DAST

Scans page

Last updated:

June 18, 2026

Read time:

2 Minutes

In Burp Suite DAST, the Scans page shows a list of all the scans that have already run, are currently running, or are scheduled to run. It is the central point of access for managing all of the scans in your landscape. The Scans page has two tabs:

Scans

The Scans page shows details for each scan, including the start time, status, and a summary of the results. The filter bar enables you to show or hide scans based on their status. You can click on a scan to view more detailed scan results.

You can also cancel or delete scans from the list using the icons to the right of each scan.

To create a new scan, click the New scan button.

Scheduled scans

The Scheduled scans tab shows a list of all your scheduled scans, along with some basic details. To view and edit the scheduled scan, click it.

Schedule scan configurations

Burp Suite DAST 2022.4 included significant changes to the way that scan configurations work. Prior to this release, you could assign scan configurations when scheduling a scan. After this release, scan configurations can usually only be administered at site level (so that scans inherit their configuration from the site to be scanned).

For schedules created before this release that already have scan configurations assigned, you can still view and edit scan configurations at schedule level via the Scan configuration panel. Scan configurations defined at schedule level override those defined at site level.

For more information on how scan configurations work in Burp Suite DAST, see the Custom scan configurations page.

Note

To ensure backward compatibility with longstanding scans, we've retained the ability to specify configurations when scheduling a scan. However, for ease of management and more accurate reporting across scans, we recommend that you replace these configurations with site level configuration.
