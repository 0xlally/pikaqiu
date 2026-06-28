# Downloading logs and debug packs

Source: https://portswigger.net/burp/documentation/dast/user-guide/working-with-scans/generate-logs
Fetched: 2026-06-28T09:15:44.168550+00:00

DAST

Downloading logs and debug packs

Last updated:

June 18, 2026

Read time:

1 Minute

Cloud

Self-hosted

This section describes how to download event logs and debug packs.

Downloading the event log

Cloud

Self-hosted

The event log can be useful for debugging. To download the event log in CSV format:

Open the Scans tab and select a scan.

Select the Logging tab.

Click Download event log.

Downloading the scan debug pack

Self-hosted

If you require assistance, our Support team may ask you for the scan debug pack.

To download the scan debug pack:

Open the Scans tab and select a scan.

Go to Logging > Scan debug pack.

Click Download.

Downloading the verbose debug pack

In some circumstances, our Support team may ask you for the verbose debug pack. It contains a Burp Suite DAST project file that holds a scan's data and configuration settings.

This is only available to download for scans that were performed with verbose logging enabled.

To download the verbose debug pack:

Open the Scans tab and select a scan.

Go to the Logging tab.

Click Download verbose debug pack.

Note

You can enable user activity logging to record user actions throughout Burp Suite. You can then download this log as a CSV file that contains a list of timestamped actions and successful logins.

For more information, see User activity log.
