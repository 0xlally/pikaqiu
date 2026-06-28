# Configuring issue management settings

Source: https://portswigger.net/burp/documentation/dast/user-guide/working-with-scans/config-issue-management
Fetched: 2026-06-28T09:15:44.012954+00:00

DAST

Configuring issue management settings

Last updated:

June 18, 2026

Read time:

2 Minutes

Cloud

Self-hosted

This section explains how to configure the way Burp Suite DAST handles false positives, accepted risks, and issues with edited severities.

You can configure whether Burp Suite DAST remembers these issues, and the criteria it uses to recognize them.

By default, Burp Suite DAST remembers false positives, accepted risks, and issues with edited severities in future scans of the same site.

If the same issue is reported again, your previous changes are applied automatically.

Configure false positive settings:

From the settings menu , select Issue management.

In the Configure false positive settings section, use the toggle to select whether Burp Suite DAST will Remember false positives for future scans of the site.

Choose how Burp Suite DAST matches newly reported issues with past issues that were flagged as false positives:

Anywhere on this site: Matches issues with the same issue type anywhere on the site.

Only at the exact same URL: Matches issues with the same issue type and URL.

Note

Use Anywhere on this site with caution. For example, if you enable it, and you flag an SQL

injection issue as being a false positive, then all future SQL injection issues reported for the site will automatically be flagged as false positives, even if they are found at different URLs.

For more information about managing false positives, see Best practices for managing false positives.

Configure accepted risk settings:

From the settings menu , select Issue management.

In the Configure accepted risk settings section, use the toggle to select whether Burp Suite DAST will Remember accepted risks for future scans of a site.

Choose how Burp Suite DAST matches newly reported issues with past issues that were flagged as accepted risks:

Anywhere on this site: Matches issues with the same issue type anywhere on the site.

Only at the exact same URL: Matches issues with the same issue type and URL.

Note

Use Anywhere on this site with caution. For example, if you enable it, and you flag an SQL

injection issue as being an accepted risk, then all future SQL injection issues reported for the site will automatically be flagged as accepted risks, even if they are found at different URLs.

Configure edit issue severity settings:

From the settings menu , select Issue management.

In the Configure edit issue severity settings section, use the toggle to select whether Burp Suite DAST will Remember severity changes for future scans of a site.

Choose how Burp Suite DAST matches newly reported issues with past issues that had their severity edited:

Anywhere on this site: Matches issues with the same issue type anywhere on the site.

Only at the exact same URL: Matches issues with the same issue type and URL.

Note

Use Anywhere on this site with caution. For example, if you enable it, and you flag an SQL

injection issue as low severity, then all future SQL injection issues reported for the site will automatically be edited to low severity, even if they are found at different URLs.
