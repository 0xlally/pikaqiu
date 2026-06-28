# Troubleshooting a Kubernetes instance

Source: https://portswigger.net/burp/documentation/dast/user-guide/troubleshooting/self-hosted/kubernetes-deployment
Fetched: 2026-06-28T09:15:41.663844+00:00

DAST

Troubleshooting a Kubernetes instance

Last updated:

June 18, 2026

Read time:

3 Minutes

Self-hosted

Kubernetes instances of Burp Suite DAST provide the following types of troubleshooting information. Our support team may ask you for these, if you contact them for help:

Support pack - This is a collection of different log files. You can download this from the help center.

Event log - This is a log of events for an individual scan.

Scan debug pack - This includes the event log, and the detailed debugging pack.

Help center

You can access the help center by selecting the icon in the upper-right corner of the screen. This provides links to:

The support pack.

The documentation for Burp Suite DAST.

The Burp Suite Support Center.

The user forum.

Support pack

The support team may ask you for the support pack to help troubleshoot your issue. The support pack contains the following information:

Diagnostics. This contains information about your installation.

The integration logs for integrations such as SAML or Jira, for the last 10 days.

The DAST server logs for the last 10 days.

The webserver logs for the last 10 days.

Metrics for each installed component, for the last 7 days.

The log files for the current day do not contain a date.

Event log

Our support team may ask you for the event logs for scans. You can download an event log for scans that are less than 10 days old.

To download the event log for a scan:

From the Scans menu, select the scan you want to troubleshoot.

In the Logging tab, click Download event log.

The event log downloads as a .csv file.

Scan debug pack

You can download a scan debug pack to access various different log files for scans that are less than 10 days old, and were successfully assigned to a scanning machine. The scan debug pack contains:

The event log.

A copy of the support pack for the last 10 days.

The scan debug log. The support team uses this to troubleshoot Burp scanner.

If verbose logging was enabled for the scan, you can also download the detailed debugging pack. This contains the project file.

To download the scan debug pack:

From the Scans page, select the scan you want to troubleshoot.

In the Logging tab, select Scan debug pack.

Click Download.

The scan debug pack downloads as a .zip file.

Enabling verbose logging

Our support team may ask you to enable verbose logging to help troubleshoot any issues. When verbose logging is enabled, the scan debug is more verbose and an additional, detailed debugging pack becomes available.

Note

Only use verbose logging when requested by the support team. Verbose logging can slow down scanning performance, and it uses more storage space.

To enable verbose logging for a scan:

From the Scans menu, select the scan you want to troubleshoot.

From the top right corner of the window, click Scan again.

Select Enable verbose logging for this scan, and click Scan.

Downloading logs manually

If the web interface is unavailable, you can download logs directly from your Kubernetes instance. There is a separate log file for each day. The log file for the current day does not contain a date.

To compress the log files, run this command:

kubectl exec -n <namespace> <enterprise-server-pod-name> -- sh -c 'tar cvzf /home/burpsuite/logs/SupportPack.tar.gz -- /home/burpsuite/logs/*Server*.log'

To download the .tar.gz file containing the log files, run this command:

kubectl cp <namespace>/<enterprise-server-pod-name>:/home/burpsuite/logs/SupportPack.tar.gz /local/path/SupportPack.tar.gz
