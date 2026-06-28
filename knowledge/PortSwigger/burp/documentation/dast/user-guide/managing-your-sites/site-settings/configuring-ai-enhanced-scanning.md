# Configuring AI-enhanced scanning

Source: https://portswigger.net/burp/documentation/dast/user-guide/managing-your-sites/site-settings/configuring-ai-enhanced-scanning
Fetched: 2026-06-28T09:15:38.809714+00:00

DAST

Configuring AI-enhanced scanning

Last updated:

June 18, 2026

Read time:

3 Minutes

Cloud

AI-enhanced scanning uses Burp AI to automatically investigate issues found during a scan. Burp AI checks each issue to determine whether it represents a real and exploitable risk, and returns detailed evidence and remediation steps. This makes it quicker and easier for you to triage issues and understand how to handle them.

This page explains how to enable and configure AI-enhanced scanning for your sites and folders.

Note

Burp AI in Burp Suite DAST is currently in a limited access beta and is not available to all customers.

How does AI-enhanced scanning work?

AI-enhanced scanning is designed to fit easily into your existing scanning process. The workflow is:

Use site settings to configure which issues you want Burp AI to investigate.

Run a scan as normal.

When the crawl and audit phases of the scan finish, Burp AI automatically investigates any issues that match the criteria you set.

Examine the results of Burp AI's investigation from the Issues tab.

Enabling AI-enhanced scanning

You can enable and configure AI-enhanced scanning for all Burp Suite DAST sites. You must have the Configure Burp AI features permission to enable AI-enhanced scanning.

Burp AI selects issues to investigate based on severity and confidence. There are three options:

Standard - Burp AI investigates all High severity findings, and Medium severity findings with Tentative confidence.

Extended - Burp AI investigates all High and Medium severity findings, plus Low severity findings with Firm or Tentative confidence.

Custom - Enables you to select which severity and confidence combinations Burp AI should investigate.

AI-enhanced scanning does not affect the crawl or audit phases of the scan. However, if you select more issue combinations Burp AI will investigate more issues. This may increase the overall scan time.

Note

Burp AI cannot investigate issues that were discovered using Burp Collaborator or Infiltrator.

Enabling AI-enhanced scanning for new sites

To enable AI-enhanced scanning when you add a new site:

In the Scan settings section, select Burp AI and automation.

Toggle the Burp AI enhanced scan setting to On. By default, this is disabled for new sites.

In the Issues to investigate section, select Standard, Extended, or Custom. If you select Custom, use the checkboxes to select the severity and confidence combinations you want Burp AI to investigate.

Related pages

There are various other settings you need to configure when adding a new site. For more information on how to add new sites in Burp Suite DAST, see:

Scanning web apps

Scanning APIs

Enabling AI-enhanced scanning for existing sites

To enable AI-enhanced scanning for an existing site:

On the top menu, select Sites to display the site tree.

Select the site you want to configure AI-enhanced scanning for.

Select the Details tab and click Edit.

In the Scan settings section, select Burp AI and automation.

Toggle the Burp AI enhanced scan setting to On.

In the Issues to investigate section, select Standard, Extended, or Custom. If you select Custom, use the checkboxes to select the severity and confidence combinations you want Burp AI to investigate.

Click Save.

Note

You can configure AI-enhanced scanning at the folder level.

Viewing AI-enhanced scan results

You can view the results of an AI-enhanced scan from the Issues tab. For more information, see Viewing AI-enhanced scan results.

If you disable AI-enhanced scanning, you can still view any existing AI results from previous scans. However, if you disable Burp AI entirely from the Settings menu, then all previous results are hidden.

Related pages

Viewing AI-enhanced scan results - explains how to find and review AI-enhanced scan results.

Burp AI trust and compliance FAQ - explains how PortSwigger keeps your data safe when using AI features.
