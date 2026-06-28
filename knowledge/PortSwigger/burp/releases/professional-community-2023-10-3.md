# Professional / Community 2023.10.3

Source: https://portswigger.net/burp/releases/professional-community-2023-10-3
Fetched: 2026-06-28T09:16:40.385543+00:00

This release introduces Bambdas into the HTTP history filter, the ability to export BChecks, the rollout of notes in other areas of Burp, TLS passthrough for out-of-scope items, and the ability to include subdomains in your target scope.

In Burp Scanner, we have made improvements to the Task details dialog to make it easier to find information about scan results and live tasks.

Advanced HTTP history filtering using Bambdas

Bambdas are a new way to customize Burp Suite directly from the UI, using small snippets of Java code. This release introduces Bambdas into the Proxy > HTTP history tab, enabling you to write custom filters for your HTTP history. These highly customizable filters can help you cut out white noise in your HTTP history, helping you to focus on only the exact items you're interested in seeing.

To try Bambdas for yourself, go to the Proxy > HTTP history tab filter, switch to Bambda mode, and write a custom filter using your own code.

Keep an eye out for Bambdas appearing in more Burp tools over the next few months.

Exporting BChecks

You can now export BChecks, making it easier to share them between different instances of Burp. Just select the BChecks you want, then click Export.

Check out our BChecks GitHub repository for BChecks from PortSwigger and from the Burp Suite community.

Increased support for notes throughout Burp

We're rolling out the notes feature into more areas of Burp. This feature enables you to record key information on tabs, making it easier to return to at a later time. Notes are copied when items are sent between different tabs. Use the Notes panel in the tab sidebar to add a note.

This update also introduces functionality that copies your notes when you send items between different tools in Burp.

This release introduces notes into:

Target > Site map

Proxy > Intercept

Proxy > HTTP history

Proxy > WebSockets history

TLS passthrough for out-of-scope items

You can now apply TLS passthrough for out-of-scope items automatically when you set the target scope, which can greatly improve performance. This behavior is automatically enabled when you accept the option to Stop logging out-of-scope items.

Include subdomains in target scope

You can now include subdomains of hosts you've included or excluded from your target scope. Enable this feature by selecting the Include subdomains checkbox in Target > Scope settings.

Improved Task details dialog

We've made some improvements to the Task details dialog to make it easier to find information about scan results and live tasks:

We've replaced the Details tab with a new Summary tab. The Summary tab contains all the information that the Details tab did, but also features a list of the most serious vulnerabilities found, more detailed information on task progress, and a task log to give you real-time information on the task's actions.

We've added a new Issues tab listing all of the issues found during a scan. As part of this change, we've renamed the Issue activity tab (which also details changes from previous scans, such as an issue being deleted or more evidence being found) to the Audit log tab.

You can now view further details on an item in the Event log by selecting it. Previously, you had to double-click an item to display the Event detail dialog.

BChecks grammar enhancements

We have added some new features to the BChecks grammar, including:

A removing query_string action that removes an entire query string from a request.

A new variable that returns Burp's User-Agent header.

A new pre-defined variable called insertion_point_base_value that contains the base value of the current insertion point.

A new per-path BCheck template that you can base your checks on.

BChecks can now return more than one issue. As a result of this, the issues reported by BChecks can now have individual names.

As a result of these changes, we have updated the grammar version to v2-beta. Please use this value in the metadata.language property when writing a check that uses these new features.

Browser upgrade

We have upgraded Burp's built-in browser to 118.0.5993.70 for Mac and Linux and 118.0.5993.70/.71 for Windows. This update contains security fixes.
