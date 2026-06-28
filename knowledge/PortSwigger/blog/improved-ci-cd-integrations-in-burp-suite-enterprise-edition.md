# Improved CI/CD integrations in Burp Suite Enterprise Edition

Source: https://portswigger.net/blog/improved-ci-cd-integrations-in-burp-suite-enterprise-edition
Fetched: 2026-06-28T09:15:18.224318+00:00

Improved CI/CD integrations in Burp Suite Enterprise Edition

Dayna Shoemaker |

Tuesday, 23 March 2021 at 15:15 UTC

Burp Suite Enterprise Edition was designed to support your DevSecOps needs. One of the ways it does this is via our pre-built and generic CI/CD driver. This allows users to integrate with tooling of their choice, because we believe that being more agile shouldn't mean being less secure.

Integrating different technologies is never without its challenges. Recently though, we've had a focus on reducing the technical complexity involved when integrating Burp Suite Enterprise Edition with CI/CD pipelines.

We are happy to announce the availability of our new CI/CD Driver version 2021.3 offers the new “Burp site-driven scan” functionality. The new "Burp site-driven scan" option will enable you to browse your site tree directly from your CI/CD system and use the site-specific settings from Burp Suite Enterprise Edition in your CI triggered scans This behavior is built on the Burp Suite Enterprise Edition GraphQL API. This additional configuration will allow you to build more flexible and more powerful integrations with your CI/CD tooling.

How might you use Burp site-driven scanning?If you run continuous scans across your site(s) after certain events, such as new commits, pull requests, or on a regular fixed schedule - e.g. a nightly build, why not try out site-driven scanning to achieve the following outcomes.

Improve site-matchingIn the past, scanning an existing site from Burp Suite Enterprise Edition was a manual process - requiring details about the site to be entered at the CI/CD build step. This manual process then relied on automated site-matching, to pair the scan with the intended site. If the tooling couldn't decide which existing site was a match, the CI/CD driver would create a separate, new site entry to scan instead. As scan results are stored under a new site entry each time, if the CI/CD driver had been forced to create a new separate site, trend analytics features/charts would be unavailable.

With the new site-driven scanning functionality, users can manually select the exact site they want to scan from their site tree within Burp Suite Enterprise Edition. This will enable more effective use of the advanced analytics and reporting features. From the dashboard you will now be able to track new, resolved, and regressed issues. The new site-matching functionality ensures that all the data and scan results, from both user-created scans and CI-created scans, are combined correctly for trend analysis.

User-friendly configurationWe always listen to user feedback. Recently, a few subscribers outlined to us that they felt the scan setup process was overly complicated. To remedy this, instead of manually entering site details like included/excluded URLs directly in the build step, you can now import the site tree and select the site you want to scan. This makes the process much faster and more efficient. There is also an option to run initial scans - these check that the configuration is successful and correct, and ensure that it's working as expected. Once confirmed, your configuration can import the site and its settings into the CI/CD build step for regular scanning.

Integrate to your CI/CD toolingIntegration with other apps (e.g. custom apps, Azure DevOps) has been limited to date. To improve this functionality, we have made some technical changes that enable you to integrate with a wider range of CI/CD pipeline tools. Moving forward, you can configure a whitelist of domains that are allowed to make cross-origin requests via the GraphQL API to access your Burp Suite Enterprise Edition data.

If you are already using Jenkins or TeamCity you will need to whitelist the corresponding domains in order to use the new CI/CD "Burp site-driven scan" option.

Download the CI/CD driver for Burp Suite Enterprise Edition and try out Burp site-driven scanning.

Ever dreamed of being a Product Manager for Burp Suite Enterprise Edition?

Take our Roadmap Survey and tell us what features you want to see in the product next.

Dayna Shoemaker

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
