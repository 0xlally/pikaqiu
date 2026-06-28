# Enterprise Edition 2023.6

Source: https://portswigger.net/burp/releases/enterprise-edition-2023-6
Fetched: 2026-06-28T09:16:19.193278+00:00

This release introduces CI-driven scans, which enable you to easily run Burp Scanner from a Docker container in your CI/CD environment. In addition, you can now add headers and cookies to your requests at the site level, to make it easier to configure header authentication. We've also made some other improvements and bug fixes.

CI-driven scans

We've made it easy to run CI-driven scans from a container in an external environment, such as your CI/CD platform. CI-driven scans are easy to configure, and you can use advanced features such as custom scan configurations and recorded login sequences.

You can view the results of your scans in the following ways:

In your CI/CD environment

As a JUnit XML file

On your Burp Suite Enterprise Edition dashboard

CI-driven scans are compatible with most platforms, including Jenkins, TeamCity, and GitHub Actions. To learn more, see Integrating CI-driven scans.

Add custom HTTP headers and cookies to requests

We've made it easier to add custom headers and cookies to requests, by enabling you to add them at the site level. This enables you to scan sites with authentication mechanisms that rely on HTTP headers or control request throttling, for example.

You can add a header or cookie when you edit an existing site, or when you add a new site.

Improved functionality for marking false positives

We now record your username and the date when you mark an issue as a false positive. You can also add notes to explain why you've marked an issue in this way. Other users in your organization can see this information, so they can learn more about the decision.

Recorded login improvements

We have made the following minor changes to the Burp Suite Navigation Recorder browser extension:

When the login sequence that you're recording uses a type of platform authentication that is not supported by the extension, such as an NTLM-based mechanism, we now warn you of this during the recording.

When recording a login sequence, you no longer need to use the browser's incognito mode. However, we strongly recommend using incognito mode whenever possible to avoid issues with stateful behavior. We implemented this change to support users who would otherwise be unable to use the extension at all due to restrictions imposed by their organization.

Improvements to Burp Scanner

We have made a number of improvements to Burp Scanner:

Burp Scanner now audits requests issued by iframes.

You can now scan YAML API definitions.

You can now scan floating input fields, which enables Burp Scanner to better handle single-page applications (SPAs).

We have reduced the amount of noise in the event log that recorded logins produce when pop-ups close.

Bug fixes for Burp Scanner:

We have fixed a bug in Burp Scanner that caused issues when crawling some API definitions.

We have fixed a bug that sometimes prevented applications from reaching a logged-in state when crawling sites with input elements that are not enclosed within a form tag.

Previously, the crawler could erroneously consolidate separate locations into one under certain circumstances. The fix for this issue may result in you seeing an increase in locations discovered by the crawler.

Other improvements

If you want to learn more about the connection check for a particular URL, you can now see the request and response messages. This can help you to remediate any issues.

We added support for PostgreSQL 15 databases.

Burp Scanner now audits requests issued by iframes.

The Click all clickable elements setting has been moved into the Miscellaneous section in the crawler scan configuration options. It has also been enabled by default. You should see an increase in scanning coverage for single-page applications that use non-traditional navigational elements.

Bug fixes

This release fixes a number of bugs:

Users who don't have permission to view scan configurations can now use custom configurations to scan their sites.

In your network settings, age limits for HSTS are now displayed correctly.
