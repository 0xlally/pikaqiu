# Viewing scan results

Source: https://portswigger.net/burp/documentation/dast/user-guide/work-with-scan-results/viewing-scan-results
Fetched: 2026-06-28T09:15:44.860085+00:00

DAST

Viewing scan results

Last updated:

June 18, 2026

Read time:

4 Minutes

Cloud

Self-hosted

To view the results of a scan:

From the top menu, select Scans to see a list of scans.

Click the relevant scan.

Use the following tabs to view details about the scan:

Dashboard

Issues

Discovered URLs

Scan statistics

Viewing the dashboard

Select the Dashboard tab to view graphs that show key information about the scan. You can see the following information:

The issues found grouped by risk and confidence level.

The number of URLs audited.

A list of the most serious issues found.

A chart of the issue severity over time.

Viewing issues

Select the Issues tab to see a list of security issues that were found by the scan. Select an issue from the list to view detailed information about it, including remediation advice and a log of the request that the issue was found in.

The issues are grouped by type. The number next to each issue indicates how many instances of this issue type were found. If a particular issue type is found on more than one URL, you can click on the issue to see a list of the relevant URLs. Click a URL to view detailed information for that particular issue instance.

Issues that have been investigated as part of an AI-enhanced scan have an AI sparkle icon next to them.

You can also perform the following actions:

Mark an issue as a false positive. For more information, see Managing issues.

If you've configured an integration with an issue tracking platform, use the Raise ticket drop-down to raise Jira tickets, GitLab issues, and Trello cards for the issue. For more information, see Raising tickets.

Related pages

Viewing issue details.

Reviewing discovered URLs

Select the Discovered URLs tab to see:

Which URLs Burp Scanner discovered.

Which URLs Burp Scanner attempted to audit.

Reasons why some URLs were not audited.

The issues Burp Scanner found at each URL.

To see which URLs were audited, review the Status column. You can also see why some URLs may not have been audited:

Audited - The URL was crawled and audited successfully.

Crawled - We crawled the URL but we didn't audit it. Some common reasons for this are:

The URL was loaded by a client-side JavaScript framework, and has no server-side traffic that we can audit.

The URL was only seen in a recorded login, so it was identified as being out of scope.

The URL is a redirect to another page that can no longer be accessed.

Crawl limit - The URL wasn't audited, because the crawl limit set by the scan configuration was reached.

Consolidated - The URL wasn't audited individually because it was consolidated with others. Burp Scanner groups similar URLs to avoid redundant checks.

Low value - The URL appears to link to static resources that don't need to be audited.

Inaccessible - Burp Scanner couldn't find a reliable route back to this URL. This can happen if dynamic resources on the original path have changed.

Out of scope - The URL was out of scope. If you want to change the site scope, see Setting the site scope.

Network error - The URL wasn't audited due to a network error. For example, the website might be down or have an internal error, or a firewall may be blocking access from the scanner.

Audited but with errors - The URL was audited but there were one or more errors. This audit may still have discovered some issues. Click the URL to see information about the errors, and any issues found.

To change how the list of URLs is displayed, click Tree or List. You can also use the filter to refine your results.

Reviewing statistics about your scan

Use the Scan statistics tab to see detailed information about the issues found by the scan, including:

A list of issues found, grouped by severity.

A Changes section showing how many of those issues were new, repeated, regressed, or resolved.

A Traffic section showing:

The requests made.

The discovered URLs.

Audited URLs without errors.

Audited URLs with errors.

Details of the scanning machines and scanner version used.

Reviewing the settings used for your scan

The Settings tab shows you the site-level settings that were used for the scan. These include:

The scan scope - the site scanned, the start URL, and any URLs that were explicitly included or excluded.

Any preset scan modes or custom scan configurations that were applied.

Any application logins that were used.

Any extensions that were used

Details of the schedule (if any) that the scan was run on.

For a more detailed view of scheduling information, click View schedule.

Viewing failed scans

A scan is given a Failed status if it is terminated early. For example, this may occur if the scan never started because Burp Scanner was unable to connect to any of the URLs specified.

If the scan began but was terminated early then the Scan details page shows much of the same information as a completed scan. In this case the Scanned URLs tab lists the URLs that caused the scan to fail.

Related pages

Managing scheduled scans.

Downloading reports.

Reports.

Downloading logs and debug packs.
