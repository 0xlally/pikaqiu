# Manually creating issues for reports

Source: https://portswigger.net/burp/documentation/desktop/running-scans/reporting/manual-issues
Fetched: 2026-06-28T09:15:53.108295+00:00

Support Center

Documentation

Desktop editions

Running scans

Reporting scan results

Manually creating issues for reports

Professional

Manually creating issues for reports

Last updated:

June 18, 2026

Read time:

2 Minutes

While manually testing, you may identify vulnerabilities that aren't automatically detected by Burp. You can create issues for these to make sure that they are included in your report.

To create an issue:

[Optional] If you want to highlight part of the message in the issue entry, select the relevant part of a request or response in the message editor.

Right-click the message and select Record an issue > Create an issue. The Create an issue dialog opens.

Fill in the issue details:

Name - A label that identifies the issue.

HTTP service - The protocol, port, and domain for the issue. This is automatically populated from the request.

Path - The URL path to the issue location. This is automatically populated from the request.

Issue severity - High, medium, low, or information.

Issue confidence - Tentative, firm, or certain.

Issue detail - An optional description of the issue.

Remediation - An optional description of the steps that you can take to mitigate the issue.

Click Create issue.

The issue is saved to your project file and can be viewed and managed in the All issues panel, just like automatically generated issues.

Adding multiple request and response pairs to an issue

It may be useful to add multiple request / response pairs to a manually created issue. For example, for a stored issue, you could add both the request that stores the malicious input and the request that retrieves and executes it. To do this, first manually create the issue, then add request / response pairs.

To add request / response pairs to a manually created issue:

[Optional] If you want to highlight part of the message in the issue entry, select the relevant part of a request or response in the message editor.

Right-click the message editor and select Record an issue > Add to manually created issue. The Add to an issue dialog opens.

Use the search box to find the manually created issue that you want to add the request / response pair to.

Select the existing manually created issue from the table.

Click Add to issue.

The request / response pair is saved to the issue.

You can customize and sort the Add to issue table contents. For more information, see Customizing Burp's tables.
