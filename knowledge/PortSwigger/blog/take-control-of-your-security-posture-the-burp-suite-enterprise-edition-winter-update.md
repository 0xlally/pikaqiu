# Take control of your security posture: The Burp Suite Enterprise Edition winter update

Source: https://portswigger.net/blog/take-control-of-your-security-posture-the-burp-suite-enterprise-edition-winter-update
Fetched: 2026-06-28T09:15:25.143208+00:00

Take control of your security posture: The Burp Suite Enterprise Edition winter update

Rob Samuels |

Wednesday, 30 October 2024 at 09:12 UTC

Manage your security, your way.

Managing a complex, enterprise-level web estate requires robust compliance, streamlined management of audits, and visibility of your security coverage.

In other words - effective web app and API security requires control.

However, meeting these needs becomes difficult when you can't easily identify and prioritise the vulnerabilities that matter most. Additionally, limited visibility of scanned URLs can leave you uncertain of your scan coverage, while restrictions to API scanning make it even harder to manage security efficiently.

Yes, tools surface plenty of vulnerabilities - but there's a lot of manual work that goes on in terms of prioritizing. What is critical for a tool might not be critical for us. We would like Enterprise to help us prioritize vulnerabilities based on our context. Senior AppSec Manager at a FinTech company

We’ve been working on a number of new features for Burp Suite Enterprise Edition to alleviate these challenges, empowering you to:

Take control of your priorities by managing your own issue severity ratings.

Simplify auditing by marking issues as accepted risks.

Integrate Burp Suite Enterprise Edition with Splunk for seamless security analytics and threat response.

Gain full visibility of URLs discovered by your scans, with additional context for URLs that have not been included in the audit.

Enhance your scan capability with extensions for CI-driven scans.

Extend your security coverage with support for SOAP APIs.

These features are being launched across three updates - version 2024.9 (launched in September), version 2024.10 (launched at the end of October), and version 2024.11 (due for launch later in November).

Interested in Burp Suite Enterprise Edition for your organization? Click here to request your free, fully-featured trial.

Available now in Burp Suite Enterprise Edition

Take control of your priorities by managing your own issue severity ratings

In Burp Suite Enterprise Edition version 2024.9 we introduced two important issue management options to help enhance your audit prioritization.

Firstly, severity ratings have been pre-defined in Burp Suite Enterprise Edition previously, making it harder to prioritise vulnerabilities based on your unique environment and security management framework.

Editable issue severity has been a highly-requested feature in Burp Suite Enterprise Edition - and you can now increase or decrease the severity rating of issues identified during a scan. You can also leave notes on the issue record to add further context and keep track of why decisions have been made.

This feature will help you manage vulnerabilities more efficiently and ensure your team remains focused on what matters most. See it below:

Simplify auditing - mark issues as accepted risks

Secondly, in addition to editing issue severity, you can also mark an issue as an accepted risk. This feature allows greater control of vulnerability management for issues that don’t require further action, or where you may have other mitigating security measures in place:

You can also leave notes in the same way as editing issue severity - ensuring you have a clear record log for auditing purposes. See how it works below:

These two issue severity improvements supplement the existing false positive option to provide greater customisation of your issue management, helping simplify your processes.

Integrate Burp Suite Enterprise Edition with Splunk for seamless security analytics and threat response

Splunk is a vulnerability management platform used by many enterprises to manage their Security Information and Event Management (SIEM).

Burp Suite Enterprise Edition 2024.10 offers a native integration, which streams issues directly into Splunk for advanced analysis. This streamlines security operations using real-time data instead of relying on manually exporting and importing data between platforms.

Gain full visibility of URLs discovered by your scans

When running scans in prior versions of Burp Suite Enterprise Edition, the scan results display only the URLs that have been put forward to audit. This means that URLs which have not been audited due to scope, crawl limits or consolidation were not displayed in the results page.

A number of Burp Suite Enterprise Edition customers have fed back that enhanced visibility of which URLs are being scanned would help increase confidence in the scan results.

From Burp Suite Enterprise Edition 2024.10 the scan results page now displays all discovered URLs in the crawl path, with additional statuses so you can identify what has and hasn’t been included in the scan. You can also filter issues by status - allowing easier follow up if required.

You can see the new statuses and a description of each below:

This feature provides greater visibility and increased confidence in the security of your web app estate.

Enhance your scan capability with extensions for CI-driven scans

In Burp Suite Enterprise Edition version 2024.10, you also have access to trusted extensions and BChecks with CI-driven scans.

This enables you to leverage custom scan behaviours and capabilities, further enriching your scan coverage.

All of these features are now available in Burp Suite Enterprise Edition version 2024.10. Update to the latest version to try them out.

Coming soon to Burp Suite Enterprise Edition

Extend your security coverage with support for SOAP APIs

In July 2024, we introduced enhanced API scanning, providing a built-in solution to API security. Burp Suite Enterprise Edition will soon also support SOAP APIs, alongside OpenAPI and GraphQL APIs.

This support for SOAP APIs will be available in Burp Suite Enterprise Edition version 2024.11, helping you extend your security coverage even further, increasing control of your API estate. This release is expected to be available in November.

Next steps

Managing a complex, enterprise-level web estate is challenging when you can't easily identify, manage and prioritise the security threats that matter most.

Take control of your security posture by editing issue severity, marking accepted risks, and integrating with Splunk for real-time updates. With enhanced URL scanning visibility, ability to use extensions in CI-driven scans, and support for SOAP APIs, you can be confident in the coverage of your DAST scans.

Work smarter, simplify audits, and stay ahead of security risks with Burp Suite Enterprise Edition.

Considering Burp Suite Enterprise Edition for your organization? Click here to request your free, fully-featured trial.

We’d love to hear your feedback

Are these new features improving your work? Are there any other features you’d like to see next? Share your thoughts on LinkedIn, X, or in our Discord community.

Rob Samuels

Latest Posts

Burp Extensibility 2026: Awards, Talks, and Highlights

19 June 2026

Burp Extensibility 2026: Awards, Talks, and Highlights

The beast needs a cage: What's next for AppSec post-Mythos

12 May 2026

The beast needs a cage: What's next for AppSec post-Mythos

3 ways custom scan checks turn practitioner knowledge into scalable automation

01 May 2026

3 ways custom scan checks turn practitioner knowledge into scalable automation

Senior pentesters have a deeply refined intuition about what is vulnerable in an environment. The problem? That expertise is often siloed with an individual and trapped in their notes or Python scripts.
