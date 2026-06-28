# Enterprise Edition 2020.7

Source: https://portswigger.net/burp/releases/enterprise-edition-2020-7
Fetched: 2026-06-28T09:16:16.858346+00:00

This release provides several improvements to our APIs and continues the ongoing improvements to the Burp Suite Enterprise Edition UI.

GraphQL API

We recently released a new GraphQL API to improve the integration of Burp Suite Enterprise Edition with other tools. This release implements the following changes:

You can now apply a site_id filter to the scans query. This enables you to fetch all scans for a given site.

When fetching issues for a scan, specifying a type_index is now optional. This enables you to fetch all issues for a scan directly. Previously, you first had to fetch the issues grouped by type.

We've added a new type IssueType, which contains information relevant to a specific issue type, such as a description and remediation advice. Instances of the type Issue now also contain an issue_type field that allows you to fetch this information.

We have also made the following adjustments to the names of some entities:

To allow for the new type IssueType, the query issue_types has been renamed to issue_type_groups. Similarly, the existing type IssueType has now been renamed to IssueTypeGroup.

For the input object DeauthorizeAgentInput, we have renamed the machine_id field to just id.

REST API

When you apply a custom scan configuration to a scan using the REST API, you can now save it as a named configuration for reuse in future scans. Previously, a custom scan configuration assigned using the REST API would be deleted after the scan was completed.

UI improvements

This release provides more improvements to the Burp Suite Enterprise Edition UI. The placeholder pages that are displayed before you have added a site or run a scan are now much more intuitive.

Bug fixes

We've also provided several minor bug fixes, most notably:

Active Directory users can now view the scan results by clicking on a scan.

Scans that fail to start now appear as failed in the list of scans. This frees up the assigned agent so that you can use it to perform another scan.

Cloud deployment links

We no longer provide AWS CloudFormation or Azure Resource Manager templates. We're releasing an improved, much simpler deployment method soon and recommend waiting for this instead.
