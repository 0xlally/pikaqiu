# Managing issues in Burp Suite DAST

Source: https://portswigger.net/burp/documentation/dast/user-guide/work-with-scan-results/managing-issues
Fetched: 2026-06-28T09:15:43.373166+00:00

DAST

Managing issues in Burp Suite DAST

Last updated:

June 18, 2026

Read time:

4 Minutes

Cloud

Self-hosted

This topic explains how to mark issues as false positives, mark issues as accepted risks, and edit issue severity.

Marking an issue as false positive

If Burp incorrectly identifies an issue, you can mark that issue as a false positive. By default, Burp remembers issues you mark as false positives, and automatically marks them in future scans of the site.

To mark an issue as false positive:

Select the scan you want to view.

Go to the Issues tab.

Select the issue you want to mark as a false positive. If multiple instances of the same issue were found, expand the issue, then select the instance you want.

Click Manage issue, then Mark as false positive.

In the Mark as false positive dialog, choose one of the following options:

This issue: Marks only this specific issue instance as a false positive.

This issue and all existing issues with the same type for the site: Marks all issues of the same type across the site as false positives.

This issue and all existing issues with the same type and URL for the site: Marks all issues of the same type that were found at the same URL as false positives.

All issues of this type in the current scan only: Marks all issues of the same type as false positives for the selected scan only.

(Optional) Add a Note.

Click Mark as false positive.

False positive issues are moved to the bottom of the list on the Issues tab, labeled as false positive and grayed out. They are also removed from the statistics and charts on the dashboards.

When you mark an issue as a false positive, Burp Suite DAST logs the time, date, and your username. You can view this information on the issue's Advisory tab.

To remove a false positive label, click it, select the relevant option from the list, then click Unmark as false positive.

Note

For more information on configuring default false positive settings, see Configure false

positive settings.

Marking an issue as accepted risk

Marking an issue as an accepted risk is useful if a known issue doesn't require immediate action, such as when it's mitigated by other security measures. To mark an issue as an accepted risk:

Select the scan you want to view.

Go to the Issues tab.

Select the issue you want to mark as an accepted risk. If multiple instances of the same issue were found, expand the issue, then select the instance you want.

Click Manage issue, then Mark as accepted risk.

In the Mark as accepted risk window, choose one of the following options:

This issue: Marks only this specific issue instance as an accepted risk.

This issue and all existing issues with the same type for the site: Marks all issues of the same type across the site as accepted risks.

This issue and all existing issues with the same type and URL for the site: Marks all issues of the same type that were found at the same URL as accepted risks.

All issues of this type in the current scan only: Marks all issues of the same type as accepted risks for the selected scan only.

(Optional) Add a Note.

Click Mark as accepted risk.

When you mark an issue as an accepted risk, Burp Suite DAST logs the time, date, and your username. You can view this information on the issue's Advisory tab.

To remove an accepted risk label, click it, select the relevant option from the list, then click Unmark as accepted risk.

Note

For more information on configuring default accepted risk settings, see Configure

accepted risk settings.

Editing issue severity

Editing the severity of an issue can be useful if the real-world impact it poses is different from how Burp has rated it. By default, Burp remembers issues you edited the severity of, and automatically edits them in future scans of the site.

To edit the severity of an issue:

Select the scan you want to view.

Go to the Issues tab.

Select the issue you want to edit the severity of. If multiple instances of the same issue were found, expand the issue, then select the instance you want.

Click Manage issue, then Edit issue severity.

In the Edit issue severity window, choose one of the following options:

This issue: Edits the severity of this specific instance only.

This issue and all existing issues with the same type for the site: Edits the severity of all issues of the same type across the site.

This issue and all existing issues with the same type and URL for the site: Edits the severity of all issues of the same type that were found at the same URL.

All issues of this type in the current scan only: Edits the severity of all issues of the same type for the selected scan only.

(Optional) Add a Note.

Click Change issue severity.

The issue severity has now been edited. When you edit an issue's severity, Burp Suite DAST logs the time, date, and your username. You can view this information on the issue's Advisory tab.

Note

By default, Burp remembers issues you edited the severity of, and automatically edits them in future scans of the site. For more information, see Configure issue severity settings.

For more information about managing false positives, see Best practices for managing false positives.
