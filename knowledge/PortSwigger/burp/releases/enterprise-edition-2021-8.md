# Enterprise Edition 2021.8

Source: https://portswigger.net/burp/releases/enterprise-edition-2021-8
Fetched: 2026-06-28T09:16:18.531038+00:00

This release enables you to install extensions and adds some Scanner compatibility improvements, telemetry collection, and some bug fixes.

Extensions support

Burp Suite Enterprise Edition now lets you use extensions to expand and customize its scanning functionality. For example, you could use an extension to scan for a specific vulnerability or to expand your logging.

With this release, Enterprise Edition supports custom extensions written in java and BApps identified as Enterprise Edition compatible. The BApp store has been updated to identify which products each BApp is compatible with. Those with the Enterprise tag can be downloaded from the BApp store and uploaded to the Enterprise extensions library.

Scanner compatibility

Burp Suite Enterprise Edition and Burp Scanner are updated and installed independently. Each component has dependencies (such as the JRE version) that mean not all versions are compatible with each other.

If you are updating components manually and you attempt to upgrade to a version of Burp Scanner that is not compatible with your version of Enterprise Edition, the Managing updates page will now tell you that you need to update your version of Enterprise Edition before you install the new Scanner. We will also email you if we release a new version of Burp Scanner that is incompatible with your version of Enterprise Edition.

Telemetry collection

Starting with this release, we are collecting telemetry that will allow us to understand your usage of Burp Suite Enterprise Edition better, and offer you more cost-effective options. We will not be capturing any information about the sites that you are scanning or any details of your scan results.

Bug fixes

This release includes the following bug fixes:

You can now use Cyrillic characters in group names.

GraphQL queries no longer return incorrect null values in Issue fields.

We fixed several minor bugs.

Cloud deployment links

We no longer provide AWS CloudFormation or Azure Resource Manager templates. We're releasing an improved, much simpler deployment method soon and recommend waiting for this instead.
