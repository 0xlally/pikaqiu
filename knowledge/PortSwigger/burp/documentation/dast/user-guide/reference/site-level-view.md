# Site-level view

Source: https://portswigger.net/burp/documentation/dast/user-guide/reference/site-level-view
Fetched: 2026-06-28T09:15:39.587162+00:00

DAST

Site-level view

Last updated:

June 18, 2026

Read time:

3 Minutes

You can click on any site to view more details. Within a site, the following tabs are available.

Dashboard

The site-level dashboard shows various metrics specific to the site. For example, you can see the current status of scans for the selected site, as well as trend charts for the most recent scans so you can keep track of how your security posture is improving over time.

The New and resolved issues chart shows the number of issues that are new, resolved, and regressed as compared to the previous scan. This enables you to monitor your progress over time.

You can hover over different areas of the charts to get more information. Clicking on some of them allows you to drill down into the results. For example, clicking on an issue severity in the Current issues chart opens the Issues tab, filtered based on the selected severity. To download charts in JPG or PNG format, click the three vertical dots in the upper-right corner of the chart.

Scans

The Scans tab shows a list of scans that have been performed on the site. This includes key information, such as the current status of each scan and how many issues were found by this scan for each severity level. You can click into each scan to open the scan details.

Depending on your permissions, you can also perform the same actions on scans as you can from the main Scans page.

Scheduled scans

The scheduled scans tab allows you to create or edit a scheduled scan.

Issues

The Issues tab shows all issues from the latest scan of the site. Issues are grouped by their type. The number next to each issue indicates the number of instances of this issue type that were found. You can expand any issue type to see the individual URLs where this issue type was found.

Clicking the URL opens the issue details page, which provides an issue description, remediation advice, as well as the HTTP request and response where the issue was found. You can also mark the issue as a false positive, mark the issue as an accepted risk, and edit the severity of the issue.

You can download the issues list as a CSV file in order to continue analyzing the data in another application, for example.

Details

The Details tab shows you the site ID and parent folder. It also enables you to view and edit the scan settings. The following details are displayed:

Site details

Site details shows the following information:

The site ID.

The folder the site is in, if applicable.

Site scope

Site scope shows you the following information:

The Start URLs of the site. These are the URLs that Burp Scanner begins the crawl from.

In-Scope URL prefixes only shows any URL prefixes that you manually set to be in scope. If this field is populated, Burp Scanner only sends requests to URLs that begin with one of these prefixes.

Out-of-scope URL prefixes only shows any URL prefixes that you manually set to be out of scope.

The protocols that are used when scanning your site's URLs. This can be set to scan all URLs using HTTP and HTTPS, or to use protocols that you specify. Any URLs for which no protocol is specified are scanned using HTTP and HTTPS.

Scan settings

Scan settings shows you the following information:

Scan configuration shows you which configuration or scan mode is selected.

Authentication shows you the login and platform authentication credentials for the site. See Configuring

authentication.

Connections shows you any configured upstream proxy servers. See Configuring upstream proxy servers.

Headers & cookies shows you which custom headers and cookies are applied. See Adding headers and

cookies.

Extensions shows you any extensions that are applied. Applied extensions are used during all scans of the site. This enables you to implement additional, custom capabilities, such as new scan checks. You can only select extensions that have been added to your organization's extension library.

Scanning pool shows you the scanning machine pool that the site is assigned to.

Notifications shows you any automated notifications (such as email or Slack messages) that are set up for the site.

Related pages

Adding new sites.

Importing sites in bulk.
