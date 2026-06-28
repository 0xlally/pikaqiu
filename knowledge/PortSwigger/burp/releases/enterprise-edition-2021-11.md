# Enterprise Edition 2021.11

Source: https://portswigger.net/burp/releases/enterprise-edition-2021-11
Fetched: 2026-06-28T09:16:16.643093+00:00

This release provides a new option for preconfiguring and adding a large number of sites in bulk, adds support for Slack integration, and enables user provisioning and decommissioning via SCIM. It also contains a number of minor improvements and bug fixes.

Add multiple sites in bulk

Instead of adding and configuring sites in Burp Suite Enterprise Edition one by one, you can now preconfigure and import a large number of sites at once from a CSV file.

You can download our template from the Sites page by clicking Import Sites.

For more information, please refer to the documentation.

Receive automated scan notifications via Slack

You can now connect Burp Suite Enterprise Edition to Slack. Once configured, this enables you to automatically notify teams via their Slack channels whenever a scan starts, fails, or finishes for a given site.

As you assign Slack channels on a site-by-site basis, you can ensure that channels only receive notifications about sites that are relevant to them.

For details on how to configure the integration, please refer to the documentation.

Improved user lifecycle management via SCIM (on-premise only)

For on-premise installations of Burp Suite Enterprise Edition, you can now enable SCIM in order to simplify the process of provisioning and decommissioning users and groups from a central identity provider (IdP).

SCIM is typically integrated in conjunction with SAML. This means you can create, update, and delete your users and groups using SCIM, while SAML is reserved exclusively for authentication via your IdP.

We have fully tested SCIM integrations with the following IdPs:

Okta

OneLogin

For more information, please refer to the documentation.

Add new sites to a new folder

When adding a new site, you now have the option to create a new folder for it at the same time. Previously, you could only add sites to existing folders.

Security fix for Windows

We have fixed a permissions issue present on the local filesystem when running Burp Suite Enterprise Edition with the embedded H2 database on a Windows machine. Note that deployments on other operating systems or using an external database are unaffected.

This issue can only be exploited by an attacker who has already compromised a valid Windows account on the server via separate means. In this scenario, the compromised account may have inherited read access to sensitive configuration, database, and log files.

If you perform a brand new installation of Burp Suite Enterprise Edition 2021.11 or higher, this issue is automatically resolved.

If you want to harden an existing installation, you can make the following changes to your Burp Suite Enterprise Edition installation and data directories:

Disable inheritance to ensure that the Users group has no permissions for either directory.

Make sure that both the Administrators group and NETWORK SERVICE user have Full control access to both of these directories.

Thanks to Vijay Tikudave, who reported this issue via our bug bounty program.

Bug fixes

We have also fixed a number of bugs, most notably one that caused issues for some users when attempting to update Burp Scanner.

Cloud deployment links

We no longer provide AWS CloudFormation or Azure Resource Manager templates. We're releasing an improved, much simpler deployment method soon and recommend waiting for this instead.
