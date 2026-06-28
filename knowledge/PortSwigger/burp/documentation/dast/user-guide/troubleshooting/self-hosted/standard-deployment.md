# Troubleshooting a standard instance

Source: https://portswigger.net/burp/documentation/dast/user-guide/troubleshooting/self-hosted/standard-deployment
Fetched: 2026-06-28T09:15:41.876609+00:00

DAST

Troubleshooting a standard instance

Last updated:

June 18, 2026

Read time:

4 Minutes

Self-hosted

Standard instances of Burp Suite DAST provide several types of troubleshooting information. Our support team may ask you for these, if you contact them for help:

Support pack - This is a collection of different log files. You can download this from the help center.

Event log - This is a log of events for an individual scan.

Scan debug pack - This includes the event log, support pack and scanning machine logs for an individual scan.

Help center

You can access the help center by selecting the icon in the upper-right corner of the screen. This provides the following features that are designed to help our support team understand the details of your installation so that they can better assist you with any issues that you report.

Support pack

The support team may ask you for the support pack to help troubleshoot your issue. The support pack contains the following information:

Diagnostics. This contains information about your installation.

The integration logs for integrations such as SAML or Jira, for the last 10 days.

The DAST server logs for the last 10 days.

The webserver logs for the last 10 days.

The database server logs for the last 10 days. This is only applicable if you are using the embedded H2 database.

Service supervisor logs for each installed component.

Metrics for each installed component, for the last 7 days.

The log files for the current day do not contain a date.

To download the support pack, click View and then click Download.

Diagnostics

This page provides quick access to the background information our support team needs to know when you report an issue. It contains details about your installation, memory usage, operating system, and so on.

The diagnostics information is also included in the Support pack.

Debug

The support team may need to see more detailed log files to understand what is causing your issues. They may ask you to temporarily enable detailed debugging for specific areas of Burp Suite DAST. They will provide you with values that you can enter in the Module field. This increases the level of detail that is included in the logs, to help our support team to investigate any issues.

You should disable detailed debugging once the investigation is complete, as it can adversely effect performance.

The setting doesn't persist if you restart the service. For more information, see Managing services.

Documentation

This page has links to our documentation, which includes video tutorials, overviews of the key concepts in Burp Suite DAST, and in-depth explanations of how every feature works.

Event log

To download the event log for a scan:

From the Scans menu, select the scan you want to troubleshoot.

In the Logging tab, click Download event log.

The event log downloads as a .csv file.

Scan debug pack

You can download a scan debug pack to access various different log files for scans that are less than 10 days old, and were successfully assigned to a scanning machine. The scan debug pack contains:

The event log.

A copy of the support pack for the last 10 days.

A copy of the scanning machine logs.

The scan debug log. The support team uses this to troubleshoot Burp scanner.

If verbose logging was enabled for the scan, you can also download the detailed debugging pack. This contains the project file.

To download the scan debug pack:

From the Scans page, select the scan you want to troubleshoot.

In the Logging tab, select Scan debug pack.

Click Download.

The scan debug pack downloads as a .zip file.

Note

If you are unable to run a scan, you can still download the scanning machine logs:

From the settings menu , select Scanning resources.

Under Scanning machines, click Manage scanning machines.

Click on the scanning machine you want to troubleshoot, and then click Download logs in the top right corner.

Enabling verbose logging

Our support team may ask you to enable verbose logging to help troubleshoot any issues. When verbose logging is enabled, the scan debug is more verbose and an additional, detailed debugging pack becomes available.

Note

Only use verbose logging when requested by the support team. Verbose logging can slow down scanning performance, and it uses more storage space.

To enable verbose logging for a scan:

From the Scans menu, select the scan you want to troubleshoot.

From the top right corner of the window, click Scan again.

Select Enable verbose logging for this scan, and click Scan.

Downloading logs manually

If the web interface is unavailable, you can download logs directly from your machine. There is a separate log file for each day. The log file for the current day does not contain a date.

To download a log file from a Windows machine, go to C:\ProgramData\BurpSuiteEnterpriseEdition.

To download a log file from a Linux machine, go to /var/log/BurpSuiteEnterpriseEdition/.

Note

These are the default log directories. Your log directories may be different, depending on the path chosen during installation.
