# Enterprise Edition 2021.6

Source: https://portswigger.net/burp/releases/enterprise-edition-2021-6
Fetched: 2026-06-28T09:16:17.513378+00:00

This release contains a Java update and several minor improvements and bug fixes.

Update to Java 11

Burp Suite Enterprise Edition now uses Java version 11.

Minor improvements

This release includes the following minor improvements:

Installing Burp Suite Enterprise Edition on a MacOS machine no longer requires a change in security settings.

We have made several small improvements to the user interface.

Bug fixes

Scans are now reported correctly in the UI and GraphQL if the browser crashes during the scan.

The user count now only includes users created directly in Burp Suite Enterprise Edition. External users, such as those logged in via SSO, will no longer be included.

Cloud deployment links

We no longer provide AWS CloudFormation or Azure Resource Manager templates. We're releasing an improved, much simpler deployment method soon and recommend waiting for this instead.
