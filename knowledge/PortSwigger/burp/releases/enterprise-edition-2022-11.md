# Enterprise Edition 2022.11

Source: https://portswigger.net/burp/releases/enterprise-edition-2022-11
Fetched: 2026-06-28T09:16:18.204153+00:00

This release enables you to export issue data from your scans in XML format.

Export issue data in XML

If you use your own tools or frameworks to produce reports, you can now import issue data from Burp Suite Enterprise Edition in XML format. Simply select Export Issue Data from the Reporting tab for your scan.

Other improvements

We've added links to our documentation from several places, so you can find out more about Burp Suite Enterprise Edition's features. For example, the Integrations page now has links to help you to integrate with CI/CD platforms.

If you enter a site URL for the scope that contains a query string, Burp Suite Enterprise Edition now warns you that the query string will be stripped from the URL. This should help to prevent the unintended exclusion of seed URLs, for example.

We've renamed Health check to Pre-scan check to make its purpose more clear.

Bug fixes

We've fixed some minor bugs.
