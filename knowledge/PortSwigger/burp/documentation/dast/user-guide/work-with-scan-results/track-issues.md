# Tracking issues over time

Source: https://portswigger.net/burp/documentation/dast/user-guide/work-with-scan-results/track-issues
Fetched: 2026-06-28T09:15:43.627189+00:00

DAST

Tracking issues over time

Last updated:

June 18, 2026

Read time:

2 Minutes

Cloud

Self-hosted

Burp Suite DAST generates statistics and charts to help you track your progress over time. This page explains how to use the trend analysis features to access information about your security posture, and quickly identify areas for improvement.

Viewing the dashboard for a site

Once you've completed a few scans, the dashboard for the site displays several charts that show you how your security issues have changed over time. These include:

Changes by issue type.

Changes by severity.

Security posture.

Audited URLs.

New and resolved issues:

New: Issues that were discovered by a scan that were either not seen before anywhere on this site or were seen before but at a different URL.

Repeated: Issues that were found in a previous scan, and were also found in the latest scan.

Regressed: Issues that were found in a previous scan, were resolved, but have now reappeared in the most recent scan.

Resolved: Issues that were found in a previous scan, but were no longer found by the most recent scan.

Note

You can configure what Burp Suite DAST classifies as "New" from the Sites and scan data settings.

The dashboard populates after you run a few scans. To view the dashboard for a site:

Click Sites > All sites.

From the list of folders and sites, click on the site.

Select the Dashboard tab.

You can download the charts from the dashboard as JPG or PNG images. To download the images, click .

Viewing the dashboard for a folder

Once you've completed a few scans, you can also view a dashboard for each folder. This dashboard displays aggregated scan results for all of the sites within the folder. You might find this useful for tracking a team's progress, for example.

To view the dashboard for a folder, click on the folder from the Sites menu.

Viewing the severity trend

The severity trend chart shows you the change in the number of issues detected, sorted by severity.

To view the Severity trend chart:

Click Scans > All scans.

Click the scan that you want to view.

In the Overview tab, scroll down to the Severity trend chart.

You can download the Severity trend chart as a JPG or PNG image. To download the image, click .

Note

We strongly recommend that you schedule regular scans in order to get the most accurate trend analysis possible. For more information, see Managing scheduled scans.
