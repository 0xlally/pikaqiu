# Folder-level view

Source: https://portswigger.net/burp/documentation/dast/user-guide/reference/folders
Fetched: 2026-06-28T09:15:39.306336+00:00

DAST

Folder-level view

Last updated:

June 18, 2026

Read time:

3 Minutes

Users with the corresponding roles can create folders to organize the site tree into a hierarchical structure. For example, your organization might choose to create folders to group sites based on their geographical location or based on the development team that is responsible for them.

You can also restrict user access based on specific folders.

Just like sites, you can click on any folder to view more details. Within a folder, the following tabs are available.

Folder-level dashboard

The folder-level dashboard shows you various metrics about the sites contained in this folder and its subfolders. For example, you can see the number of current issues of each severity level.

You can also use the dashboard to keep track of how the security of the folder's sites is progressing over time. The New and resolved issues over time chart shows the number of issues that are new, resolved, and regressed as compared to the previous scan. This enables you to monitor your progress over time

You can hover over different areas of the charts to get more information and click on some of them to drill down into the results. For example, clicking on an issue severity in the Current issues chart opens the Issues tab, filtered based on the selected severity. To download charts in JPG or PNG format, click the three vertical dots in the upper-right corner of the chart.

Scans

The Scans tab shows the scans that have been performed on all sites within this folder and its subfolders. It provides an overview of basic information, such as the current status of each scan and how many issues it has found for each severity level. You can click on each scan to open the scan details.

Depending on your permissions, you can also perform the same actions on sites and folders as you can from the main Sites page.

Scheduled scans

The scheduled scans tab shows the scans scheduled for all sites within this folder and its subfolders. It enables you to create or edit a scheduled scan.

Issues

The Issues tab shows all issues from the latest scan of all sites within this folder and its subfolders. Issues are grouped by their type. The number next to each issue indicates the number of instances of this issue type that were found. You can expand any issue type to see the individual URLs where this issue type was found.

Clicking the URL opens the issue details page, which provides an issue description, remediation advice, as well as the HTTP

request and response where the issue was found. You can also mark the issue as a false positive, mark the issue as an accepted

risk, and edit the severity of the issue.

You can download the issues list as a CSV file in order to continue analyzing the data in another application, for example.

Details

Details shows you the folder ID and parent folder. You can also see the following information:

Scan configuration shows you which configuration or scan mode is selected.

Authentication shows you the platform authentication credentials for the site. See Configuring authentication.

Connections shows you any configured upstream proxy servers. See Configuring upstream proxy servers.

Extensions shows you any extensions that are applied. The extensions applied are used during all scans of the site.

This enables you to implement additional, custom capabilities, such as new scan checks. You can only select

extensions that have been added to your organization's extension library.

Notifications shows you any automated Slack notifications that are set up for the site.

To edit the content, click Edit.
