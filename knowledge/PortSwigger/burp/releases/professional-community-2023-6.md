# Professional / Community 2023.6

Source: https://portswigger.net/burp/releases/professional-community-2023-6
Fetched: 2026-06-28T09:16:43.687560+00:00

This release introduces BChecks, which are custom scan checks. It also provides improvements to Burp Scanner's live crawl path views, GraphQL scan checks, and a number of additional improvements and bug fixes.

Custom scan checks

This release introduces BChecks, which are scan checks that you can create and import. Burp Scanner runs these checks in addition to its built-in scanning routine. This enables you to fine-tune your scans and make your testing workflow as efficient as possible.

You can use our custom definition language to easily create BChecks. Burp includes a range of templates to get you started.

We have also created a BChecks GitHub repository. This includes example BChecks from PortSwigger, as well as BChecks developed by the Burp Suite community. We look forward to accepting pull requests and celebrating your awesome work.

In the future, we're planning to improve the BCheck language and testing experience. We'd love your feedback. Contact our support team at support@portswigger.net.

Live crawl paths view improvements

We have made a number of improvements to Burp Scanner's live crawl paths view:

You can now view details of all the possible navigation actions that the crawler was able to take from a given location on the crawl path. This enables you to better understand the structure of your site. To view these details, go to the Crawl paths > Outlinks tab of the scan task details window.

You can now view a screenshot of Burp's browser at any crawl location. Go to the Crawl paths tab of the scan task details window and click Show screenshot.

The shortest crawl path tree is now retained when you reopen a project file.

GraphQL scan checks

We have introduced a number of GraphQL scan checks. The new scan checks enable you to:

Identify and maintain a list of any GraphQL endpoints discovered during the crawl.

Identify if introspection queries are enabled.

Find out if GraphQL suggestions are enabled.

Test for CSRF vulnerabilities in all discovered GraphQL endpoints.

Montoya API

We have updated the Montoya API, to enable you to create extensions with additional functionality. You can now:

Convert ByteArray data to different integer bases. This means you no longer need to use additional libraries to complete this task.

Log exceptions to the error output. This means that you don't need to format and convert exceptions manually.

Other improvements

We have made a number of additional improvements, including:

You can now quickly switch to the Organizer tab using the hotkey Ctrl + Shift + O.

In the Issue activity table on the Dashboard, you can now filter issues by your target scope.

We have changed the way we launch Burp's browser. It now works with accounts for sites that fingerprint the presence of the DevTools listener, such as Google accounts.

Bug fixes

We fixed a number of minor bugs:

If you change the highlight in the Organizer table, it no longer deselects the current row.

For Burp Suite Community Edition, filters are now correctly applied to Intruder attack results.

Browser upgrade

We have upgraded Burp's built-in browser to 114.0.5735.110 for Windows and 114.0.5735.106 for Mac and Linux. This update contains multiple security fixes.
