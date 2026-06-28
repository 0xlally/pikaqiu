# Creating scans

Source: https://portswigger.net/burp/documentation/dast/user-guide/working-with-scans/creating-new-scan
Fetched: 2026-06-28T09:15:44.490741+00:00

DAST

Creating scans

Last updated:

June 18, 2026

Read time:

2 Minutes

Cloud

Self-hosted

Burp Suite DAST enables you to scan your sites for security issues. You can create one-off scans or schedule recurring scans for one or more of your sites and folders.

Note

Before you can create any scans, you need to create a site. Sites can contain web apps or APIs that you want to scan.

Your scanning machines must be able to access the sites you want to scan. For information on allowing access, see Configuring your environment network and firewall settings.

Scheduling scans for a folder

When you schedule a recurring scan for a folder, you create a scan for each of the sites in the folder.

If you move a site out of the folder, you remove the scheduled scan for the site.

If you add a site to the folder, you add the scheduled scan to the site.

Creating a new scan

To create a new scan:

From the Sites menu, select the sites and folders that you want to scan.

From the menu at the bottom of the screen, click Scan.

Choose when you want the scan to start. By default, scans start immediately.

Choose how often the scan should repeat. By default, scans repeat weekly.

When you're happy with your scan settings, click Save.

Go to Scans > Scheduled scans to see your new scan in the list.

Note

If you select a folder that contains one or more sites that you don't have permission to view and scan, you won't be able to create the scan.

To create a scan for the sites that you do have permission to view and scan, deselect the folder, and select the sites individually.

CI-driven scans

You can create scans in external environments, such as in your CI/CD pipeline. For more information, see Integrating CI-driven scans.

Related pages

Managing scheduled scans - explains how to set up regularly-scheduled scans.
