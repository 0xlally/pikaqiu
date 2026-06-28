# Enterprise Edition 2025.3

Source: https://portswigger.net/burp/releases/enterprise-edition-2025-3
Fetched: 2026-06-28T09:16:21.140652+00:00

This release brings significant improvements to our integration with Jira. For example, you can now create automatic rules and apply them to multiple sites, and you can specify Jira parents. We also fixed some bugs, and updated Java Runtime and Azul Zulu.

Improvements to Jira integration

We've made it much easier to create Jira tickets both automatically and manually:

You can create multiple automatic rules for your sites.

You can apply automatic rules to multiple folders and sites.

You can raise Jira tickets automatically for Jira parents.

You can enable your users to raise tickets manually for Jira parents.

We've also improved performance and stability.

Note

If you already have an automatic Jira rule, Burp Suite Enterprise edition will raise Jira tickets for any issues that were found before you created the rule, when you next run a scan.

Java updates

We updated Java Runtime to 21.0.6, and Azul Zulu to 21.40.17.

Bug fixes

We fixed the following bugs:

If you save a scan with the default name New scan configuration and you already have a scan with this name, it no longer causes an error. We now use the name New scan configuration [n+1].

We fixed a 'time out' error when using Jira with a large number of projects.
