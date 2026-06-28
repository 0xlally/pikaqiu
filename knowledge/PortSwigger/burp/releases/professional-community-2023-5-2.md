# Professional / Community 2023.5.2

Source: https://portswigger.net/burp/releases/professional-community-2023-5-2
Fetched: 2026-06-28T09:16:43.426624+00:00

This release introduces the new Burp Organizer tool, a live crawl paths view, upgrades for the Montoya API, and a number of minor improvements.

Live crawl paths view

We have added a new Crawl paths tab to the Task details dialog. This tab gives you real-time updates on crawls, displaying all the locations found in the target site and the actions taken by Burp Scanner to reach each of those locations.

For audit scans, the Crawl paths tab also shows details of any issues discovered in each location.

Please note that the Crawl paths tab is still under active development, and the contents of the tab are not currently saved to Burp Suite project files. As such, if you close and re-open the project the tab does not display any information for previously-run scans.

To learn more about the crawl paths view, see our documentation.

Burp Organizer

This release introduces Burp Organizer, which enables you to store copies of HTTP messages that you want to come back to later. Use Organizer to better manage your penetration testing workflow. For example, you can:

Store messages that you want to investigate later.

Save messages that you've already identified as interesting.

Save messages that you want to add to a report later.

Organizer is designed to provide an alternative to storing messages in Burp Repeater. Organizer's table structure makes it easier to work with large numbers of stored messages. It also enables you to add notes to your messages, so you can capture your thoughts to review later. These are displayed in the collapsible Notes panel.

To learn more about Burp Organizer, see our documentation.

In the future, we may add the notes function to other Burp tools. If you think this would be useful, please let us know how you would use notes in your penetration testing workflow. Contact our support team at support@portswigger.net.

Recorded login improvements

We have made the following minor changes to the Burp Suite Navigation Recorder browser extension:

When the login sequence that you're recording uses a type of platform authentication that is not supported by the extension, such as an NTLM-based mechanism, we now warn you of this during the recording.

When recording a login sequence, you no longer need to use the browser's incognito mode. However, we strongly recommend using incognito mode whenever possible to avoid issues with stateful behavior. We implemented this change to support users who would otherwise be unable to use the extension at all due to restrictions imposed by their organization.

Montoya API

We have updated the Montoya API, to enable you to create extensions with additional functionality. You can now:

Access font information for the message editor and display.

Access the insertion points that are automatically detected by Burp Intruder.

Update and add headers or parameters. Burp adds the header or parameter if it isn't already present in a request.

Create Collaborator payloads so that any resulting interactions appear in the Collaborator tab.

Retrieve the details of any Collaborator interactions from issues identified by Burp Scanner in an audit.

We have fixed a bug so that extension settings from earlier versions of Burp now carry over to the Montoya API versions of Burp.

Minor improvements

We have added a number of minor improvements, including:

You can now choose to apply enabled match and replace rules to in-scope items only.

You can now generate a project file that includes high, medium, low, and informational issues, but doesn't include false positives.

Burp Scanner now audits requests issued by iframes.

You can now use wildcard domains when you set a simple scope for Burp Scanner under Detailed scope configuration in the New scan dialog. This enables you to quickly and easily add all subdomains of a target domain to scope. For more information, see Setting the scan scope - Wildcards.

The Click all clickable elements setting has been moved into the Miscellaneous section in the crawler scan configuration options. It has also been enabled by default. You should see an increase in scanning coverage for single-page applications that use non-traditional navigational elements.

Bug fixes

We have fixed an issue with DOM Invader that prevented it from working properly with newer versions of Chromium.

Previously, the crawler could erroneously consolidate separate locations into one under certain circumstances. The fix for this issue may result in you seeing an increase in locations discovered by the crawler.

We have fixed a bug that sometimes prevented applications from reaching a logged-in state when crawling sites with input elements that are not enclosed within a <form> tag.

When checking for SQL and XPath vulnerabilities, issues are now correctly linked to the first response in a redirection chain that includes the error string. Previously, issues continued to be reported for each response with the error string.

Browser upgrade

We have upgraded Burp's built-in browser to 114.0.5735.91 for Windows and 114.0.5735.90 for Mac and Linux.
