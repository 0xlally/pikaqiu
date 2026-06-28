# Enterprise Edition 2020.12

Source: https://portswigger.net/burp/releases/enterprise-edition-2020-12
Fetched: 2026-06-28T09:16:16.492853+00:00

This release provides the following improvements and bug fixes.

UI refresh

The UI now has a more modern look and feel. We hope you like the new design as much as we do.

New Help center and troubleshooting features

Users with permission to modify the settings can access the new "Help center" by clicking the ? icon in the upper-right corner of the screen. This provides a range of new features to help troubleshoot issues with your setup:

Diagnostics - This page provides quick access to all the background information our support team needs to know when you report an issue. It contains some basic details about your installation, memory usage, operating system, and so on. This enables you to quickly copy and paste all of this information from one place, rather than having to track it down across your system.

Debug - From time to time, the support team may ask you to enable detailed debugging for specific areas of Burp Suite Enterprise Edition. In this case, they will provide a series of values that you should enter on this page. This temporarily increases the level of detail that is included in the logs, which will help our support team get to the bottom of any issues.

Support pack - The support team may occasionally ask you to provide a collection of log files to help them troubleshoot an issue that you've reported. This page enables you to download various different logs as a single file so that you can easily send them to our support team.

This release also adds the following new options for downloading logs:

You can now download the logs for an individual scan. To do this, go to the scan details page for the relevant scan and select "More actions" > "Download scan log". Note that the log is only available for scans that:

Were successfully assigned to an agent

Have run or started running since you upgraded to Burp Suite Enterprise Edition 2020.12

Are less than 10 days old

You can now download the logs for an individual agent machine. To do this, go to the "Agents" page and select the relevant agent machine. In the upper-right corner, click "Download logs".

Bug fixes

When trying to connect to Jira, receiving a response that is larger than 2 MB no longer triggers an exception.

In the "Database backup" settings, specifying a save location with dots in the path no longer causes issues. Previously, you would be prevented from saving your changes if you entered a path such as /home/user/example.directory/.

When transferring a SQL Server database with the transfer tool, you can now successfully use any target database name. Previously, the transfer would fail if the target name was anything other than burp_enterprise.

Cloud deployment links

We no longer provide AWS CloudFormation or Azure Resource Manager templates. We're releasing an improved, much simpler deployment method soon and recommend waiting for this instead.
