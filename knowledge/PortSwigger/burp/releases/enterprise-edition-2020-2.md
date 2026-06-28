# Enterprise Edition 2020.2

Source: https://portswigger.net/burp/releases/enterprise-edition-2020-2
Fetched: 2026-06-28T09:16:16.181967+00:00

This release adds a number of new features to help simplify and streamline your post-scan activities. You can now:

Choose to download a detailed scan report instead of just a summary.

Tailor scan reports to your needs by choosing which severity of issues to include.

Specify email addresses that should automatically receive an end-of-scan summary when a scan is completed for a particular site. Note that configuring your email server is a prerequisite for enabling this feature.

Download a summary of aggregated issues in CSV format.

Automatically create Jira tickets for issues based on their severity and confidence.

The scan tidy-up feature has also been adjusted so that it now always retains the most recent scan for a site, even if this scan is older than the configured threshold.

Client-side certificates have also been added for custom scan configurations.

In addition, this release contains the following bug fixes:

Update should no longer fail for Enterprise users running on an Oracle database.

Scan results should now be displayed correctly in IE11.

Dynamic analysis should now behave more consistently.
