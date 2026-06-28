# Viewing AI-enhanced scan results

Source: https://portswigger.net/burp/documentation/dast/user-guide/work-with-scan-results/ai-enhanced-results
Fetched: 2026-06-28T09:15:43.186082+00:00

DAST

Viewing AI-enhanced scan results

Last updated:

June 18, 2026

Read time:

2 Minutes

Cloud

This page explains how to review AI-enhanced scan results in Burp Suite DAST.

Once Burp AI has investigated an issue, it adds its findings to the Details section of the Issues tab. For information on how to access this page, see Viewing issue details.

Note

Burp AI in Burp Suite DAST is currently in a limited access beta and is not available to all customers.

Burp AI outcomes

When Burp AI investigates an issue, it returns a Burp AI outcome. This is displayed on the Issues page and in the Severity section of the Advisory tab.

There are two possible outcomes:

Issue confirmed - Burp AI confirmed that the issue is real and exploitable.

Inconclusive - Burp AI couldn't confirm that the issue is real and exploitable. This does not necessarily mean the issue is a false positive. In this case, further manual testing is required to fully validate the severity and impact of the issue.

You can filter the Issues tab by Burp AI outcome.

Viewing details of Burp AI's investigation

Issues that Burp AI has explored also display a Burp AI results section on the Advisory tab. This is separate from the Scanner results section:

Scanner results: This shows the original findings discovered when Burp Scanner detected the issue.

Burp AI results: This shows the AI's independent investigation, including its own testing and conclusions.

The Burp AI results section contains the following information:

Summary: A short description of what Burp AI tested and observed.

Impact: An overview of the potential security impact. This helps you assess risk and prioritize next steps.

Evidence: The proof of the issue found by Burp AI. This may include requests and responses, payloads, or observed behavior.

Details: Full technical details of what Burp AI observed when investigating the issue.

Reproduction steps: A guide on how to manually reproduce Burp AI's findings.

You can use the Copy buttons to copy the contents of the Burp AI results section. This makes it easy to share these results with security teams or other stakeholders.

Running an AI investigation manually

You can manually run a Burp AI investigation on an issue after a scan has finished. This can be useful if Burp AI originally skipped the issue due to your scan settings.

To do this, open the issue details page for the issue and click Investigate issue.

You can manually investigate any issue, except Collaborator or Infiltrator issues. If an issue already has Burp AI results, running Investigate issue overwrites the current AI investigation for that issue.

Reporting on AI-enhanced results

AI-enhanced results are included in all report types. Detailed reports and compliance reports include the full Burp AI results section for each issue.

You cannot generate a report for a scan while Burp AI is still investigating issues.

Related pages

Configuring AI-enhanced scanning.

Viewing issue details.

Downloading reports.
