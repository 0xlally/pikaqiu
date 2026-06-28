# Enterprise Edition TeamCity plugin 2021.3

Source: https://portswigger.net/burp/releases/enterprise-edition-teamcity-plugin-2021-3
Fetched: 2026-06-28T09:16:21.628630+00:00

This release greatly improves the usability of Burp Suite Enterprise Edition's native TeamCity plugin by adding a new "site-driven scan" integration option. Don't worry, it still includes the legacy "Burp scan" option, which you can use in the same way as before. This means you can upgrade to the new plugin without breaking your existing integrations.

Prerequisites

Please note that in order to use the new site-driven scan option, you also need to upgrade Burp Suite Enterprise Edition to version 2021.3 or higher.

What is the TeamCity plugin?

Our native TeamCity plugin enables you to integrate automated vulnerability scans into your existing pipelines and configure rules for failing the build based on the scan's results. This helps you to catch bugs earlier in your development process by adopting a DevSecOps approach, with minimal disruption to your existing workflow.

The plugin offers all of the same functionality as our generic CI/CD driver, but also adds two custom build step runner types to TeamCity. This allows you to configure the various options using the TeamCity web interface rather than having to use a shell command.

Site-driven scans

The new "site-driven scan" option provides the following key advantages.

Manual site matching

Your sites are automatically fetched from Burp Suite Enterprise Edition via its GraphQL API. This means that when adding a vulnerability scan to your pipeline, you can manually select the exact site that it relates to. Previously, you had to rely on the automated site-matching rules.

Manually matching your sites and scans ensures that all of your scan data is associated with the correct site and that results are seamlessly aggregated from both user-created and TeamCity-generated scans. This allows you to take full advantage of Burp Suite Enterprise Edition's powerful analytics features and accurately monitor changes to your security posture over time.

Greatly simplified integration process

Site-driven scans also have access to most of your site data from Burp Suite Enterprise Edition. This includes the default scan configurations, URL scope, false positive settings, and so on. As a result, you no longer need to manually provide this information in your build step. This makes the integration process much simpler and removes the need to create custom JSON scan definitions.

Instead, you simply create and configure your site as normal using Burp Suite Enterprise Edition's intuitive web UI. You can then test your site and scan configuration by running a few scans manually, tweaking the behavior if necessary. Once you're satisfied with everything, you just select this site from your TeamCity build step and all of these settings will be used automatically. Any subsequent changes you make to your site in the Burp Suite Enterprise Edition web UI will be automatically reflected in TeamCity the next time you run a build.

Burp scans

To provide continued support for any existing integrations that you may have configured, this release also retains the legacy "Burp scan" option in its original form.

This is useful in some cases, such as when you want to run a one-off scan and do not want its results to be linked to a particular site. However, for most new integrations, we recommend using the new site-driven scan option instead.

For more detailed information about the pros and cons of both approaches, please refer to the documentation.
