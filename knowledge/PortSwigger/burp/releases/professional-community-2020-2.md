# Professional / Community 2020.2

Source: https://portswigger.net/burp/releases/professional-community-2020-2
Fetched: 2026-06-28T09:16:33.770304+00:00

This release builds on the general improvements we have been making to the HTTP message editor and incorporates some feedback from the community:

Triple-clicking a word now selects the entire token, for example, the header value or a string literal of a JSON value.

In editable messages, such as requests and responses in Burp Repeater, hovering over URL-encoded text now shows the decoded version in a tooltip.

The "Convert selection" popup now works in responses as well as requests.

In the user options for displaying HTTP messages, you can now choose to use any monospaced font that is installed on your system.

Performance when analyzing responses with multiple code blocks has been improved.

The "Render" tab now enables you to view rendered HTML pages and images directly within the various tools instead of in a separate popup.

You can now add custom content to the Burp Collaborator service. For example, you could add a readme on the index page identifying the organization and the purpose of the service, or prove ownership of your domain to validate TLS certificate requests. To do this, you simply add new entries in the configuration file containing a path, contentType, and base64Content as follows:

"customHttpContent":

[

{ "path": "/", "contentType": "text/plain", "base64Content": "VGhpcyBpcyBhIHJhbmRvbSBsaW5lIG9mIHRleHQ="},

{ "path": "/foo", "contentType": "text/html", "base64Content": "dGhpcyBpcyBhbm90aGVyIG9uZSBmb3IgZ29vZCBtZWFzdXJlLiBOaWNlLg==" }

]

You can now initiate instant active or passive scans in Burp. This means you can quickly check for vulnerabilities without having to open the scan launcher. You can access these options by right-clicking on a request. Alternatively, you can configure hotkeys for triggering instant scans.

The following bugs fixes have also been implemented:

A bug causing load/save filter dialogs to be hidden has been fixed.

The "Scan defined insertion points" feature now works for all environments.

Redirections are now shown in the site map when crawling.
