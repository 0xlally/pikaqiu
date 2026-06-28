# Enterprise Edition 2022.8

Source: https://portswigger.net/burp/releases/enterprise-edition-2022-8
Fetched: 2026-06-28T09:16:18.097804+00:00

This release makes it much easier to troubleshoot connectivity issues for your target URLs. We've also made it easier to create sites and scans, and improved how we handle tabs on small screens.

Introduction of connection check tool

The new connection check tool enables you to check the connection to your target URLs before you start a scan. You can quickly troubleshoot any connectivity issues without having to wait for a scan to finish.

Improved handling of tabs on small screens

We've improved how tabs are displayed if you're using Burp Suite Enterprise Edition on a small screen. Instead of wrapping onto a new row, the tabs are now collated in a dropdown menu so that they take up less space.

Simplified steps for starting and scheduling scans

We've made a number of changes to make it easier for you to get scanning:

When you create a new scheduled scan, the scan will repeat once a week by default.

We've added the option to create a new site from the Create a scan page.

We've added the option to Scan a new site from the Scans top menu.

Other improvements

We've also made the following improvements:

If Burp Scanner detects that a site is vulnerable to client-side prototype pollution, Burp Suite Enterprise Edition now shows evidence of the vulnerability. You can use this information to resolve the issue.

If you try to navigate away from the Database backup screen, we'll prompt you to save any unsaved changes.

This release upgrades the JRE to version 17.0.4. This provides bug fixes and updates.

Bug fixes

We've fixed some bugs. For example:

We've made sure that the Enterprise server can be updated cleanly, without breaking the connection to the database.

For Kubernetes deployments, we've fixed an issue where scans didn't start if a custom PVC name was used.
