# Assigning scan limits

Source: https://portswigger.net/burp/documentation/dast/user-guide/managing-scanning-resources/assigning-scan-limits
Fetched: 2026-06-28T09:15:37.097994+00:00

DAST

Assigning scan limits

Last updated:

June 18, 2026

Read time:

1 Minute

Self-hosted

To avoid placing too much load on your scanning machines, you can limit the maximum number of concurrent scans that they can run. For newly added scanning machines, the default scan limit is 1. If the scanning machine has enough RAM and CPU cores, you can increase the scan limit. For more information, refer to the System requirements.

Note

This page explains how to configure fixed scanning machines for a standard instance of Burp Suite DAST. For information on how to use cloud-based auto-scaling scanning, see the Managing auto-scaling scan resources page.

If you decide to change the scan limits, increase the number slowly and monitor the effect this has on performance.

To assign scan limits, do the following steps:

From the settings menu select Scanning resources.

Under Scanning machines, click Manage scanning machines.

Make sure the Scanning machines tab is selected.

To change the Concurrent scan limit, click the plus or minus icons.

If you have a Classic license for a specific number of concurrent scans, go to the Licensing tab to view this total number, and the remaining number of concurrent scans that you are licensed to run.

Additional scans

If you have a Classic license for a specific number of concurrent scans, you can increase the number of concurrent scans at any time from your account page on portswigger.net.
