# Best practices for managing false positives

Source: https://portswigger.net/burp/documentation/dast/user-guide/working-with-scans/false-positives-best-practice
Fetched: 2026-06-28T09:15:43.937181+00:00

DAST

Best practices for managing false positives

Last updated:

June 18, 2026

Read time:

2 Minutes

All automated scanners can generate false positives, which are issues flagged as vulnerabilities that don't pose actual risks.

Managing false positives enables you to reduce noise, avoid wasting resources, and focus on genuine threats. This section outlines some best practices for identifying and addressing false positives, so that you can integrate them into your workflows.

Use the Dashboard for your scan to review the issues found by Burp Scanner. We recommend the following workflow for managing false positives.

Review the confidence ratings

The Issues tab shows you the confidence rating for each issue.

Issues rated as Certain are highly likely to be valid vulnerabilities.

Issues rated as Tentative or Firm may require further investigation.

Prioritize a deeper analysis for any rating below Certain.

Understand the issue type

In the Issues tab, click on an issue and go to the Advisory tab.

Expand the headings to see detailed information about the issue and possible steps for remediation.

Understand the issue context

Cross-check flagged issues against your application's architecture and configurations.

Use historical scan data to identify recurring patterns that might indicate false positives.

Use manual testing to validate issues

For issues flagged with lower confidence ratings, manually validate them to confirm whether they pose an actual risk.

You can use tools in Burp Suite Professional such as Repeater or Intruder to replicate the vulnerability and assess its impact.

Collaborate with development teams

Work with your development team to determine whether flagged issues align with the intended functionality of the application.

Generate reports in Burp Suite DAST to share with your development team, streamlining this process.

Fine-tune your scanning configurations

Regularly review and update your scanning configurations to minimize noise.

Modify scan settings to exclude known false positives or non-applicable checks for your application environment.

Explore the scan accuracy options within custom scan configurations. For more information, see Audit settings.

Document and refine your process

Create internal documentation to record common false positives and describe how they are handled.

Regularly review and refine your process for handling false positives, based on feedback from your team and your evolving business needs.

Related pages

Managing issues in Burp Suite DAST

Configuring issue management settings
