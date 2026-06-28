# Reports

Source: https://portswigger.net/burp/documentation/dast/user-guide/reference/reports
Fetched: 2026-06-28T09:15:39.471158+00:00

DAST

Reports

Last updated:

June 18, 2026

Read time:

4 Minutes

You can generate offline reports to share with other members of your organization, even if they do not have access to Burp Suite DAST.

There are two categories of report available:

Standard reports give a general overview of scan details, such as the included URLs, scan configurations used, and the duration of the scan.

Compliance reports help to show whether a site meets a specific compliance standard or framework. We currently offer compliance reporting for the OWASP Top 10 2025 list and the PCI DSS v4.0.1 security compliance standard.

You can download reports for completed or failed scans. The reports are available in HTML and PDF formats.

Standard reports

Burp Suite DAST offers two standard reports: Summary and Detailed.

The Summary reports contains the following information:

An overview of the scan details.

Issues by severity.

Scanned URLs and URLs with problems.

Requests made.

Locations.

Network errors.

The Summary report contains a list of issue types, along with the corresponding URLs where these issues were identified. Burp Scanner's confidence and estimated severity level are indicated for each issue.

The Detailed report contains the same information as the Summary report and the following additional information:

A brief description of the issue type.

Background information about the issue type.

High-level remediation advice.

Links to additional resources, to learn about the issue type.

The Detailed report also provides evidence of the location in which the issue was detected. For example, this could be a series of HTTP requests and responses. For DOM-based issues, the results of Burp Scanner's dynamic JavaScript analysis is also provided.

Included severities

You can choose the issue severity that you want to include for both Summary and Detailed reports. By default, all severities are included.

False positives

By default, scan reports exclude issues that are marked as false positives. However, you can choose to include them.

Compliance reports

Burp Suite DAST offers reporting for the OWASP Top 10 2025 list and the PCI DSS v4.0.1 security compliance standard. These reports use your existing scan data to generate a report that indicates whether a given site would meet compliance standards, and to highlight where work may be needed in order to meet those standards.

The following reports are available:

OWASP Top 10: 2025 - This report highlights any issues found by the scan that correspond to issue categories in the OWASP Top 10 2025.

PCI DSS v4.0.1 - This report highlights any issues found by the scan that break the requirements set out in the PCI DSS v4.0.1 standard.

Note

Burp Suite DAST's compliance reports do not guarantee compliance or non-compliance with any specific security standard.

You cannot specify severities to report on or choose whether to include false positives when running a compliance report. Compliance reports always include all issue severities and exclude false positives.

If the selected scan did not run all the necessary checks for the selected report type, or if the scan was run before support for compliance reporting was introduced, you'll see a warning message. You can still download the report but be aware that the results may not fully reflect your security posture.

Any compliance reports generated from incompatible scans display a warning at the top of the report body.

Compliance report contents

The reports detail each category of compliance issue that the scan found an example of, including:

The Burp Suite issue type.

The URL at which the issue was found.

The severity of the issue.

Scan confidence levels.

Click View to see more information about each issue, including a brief description of what the issue type means, background information, and some high-level remediation advice.

Note:

OWASP Top 10 2025 and PCI DSS v4.0.1 categories are broader than Burp Suite issue types. As such, the report may display several issue types under the same compliance category. For example, SQL Injection and PHP Code Injection are two separate issue types within Burp Suite. However, in the OWASP Top 10 2021 they both fall under the category of "A03:2021 - Injection".

The PCI DSS v4.0.1 report also contains a typical Common Vulnerability Scoring System (CVSS) score for each issue found. CVSS scores give a standardized indication of the severity of a vulnerability.

Note that the CVSS score provided in the report is an example score based on the type of issue found, and is provided for information purposes only. The system does not take any details of the specific issue into account when displaying a CVSS score.

Uncategorized issues

The reports display details of any issues found by the scan that do not correspond to a category in the relevant compliance standard. These issues are referred to as "uncategorized" issues, and are detailed in the Uncategorized section at the bottom of the report. The information displayed for uncategorized issues is the same as that displayed for categorized ones.

Viewing scan details

The Scan Details section at the bottom of the report lists information about the scan itself, including the time of the scan, its duration, and a full list of all checks that were run.

Automatic scan summary reports

As well as being able to generate scan reports on demand, you can also configure Burp Suite DAST to automatically send scan summary reports.

Note

To use this feature, your administrator must have configured a connection to an SMTP server.

Related pages

Downloading reports.
