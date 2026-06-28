# Professional / Community 2022.3

Source: https://portswigger.net/burp/releases/professional-community-2022-3
Fetched: 2026-06-28T09:16:37.592365+00:00

This release enables you to add tabs to the message editor that provide the same features as the Inspector panel. It also adds a new domain name for the public Burp Collaborator server, and includes some enhancements to Burp Scanner. Finally, rows of tabs no longer switch places when selected.

Customizable message editor tabs

In addition to the existing Pretty, Raw, Hex, and Render tabs, you can now add the following tabs to the message editor:

Headers

Query params

Body params

Cookies

Attributes

Some of these tabs were available in older versions of Burp Suite, but have now been reintroduced and enhanced with the same powerful features for working with HTTP messages as the Inspector. This is a great alternative if you want to take advantage of the Inspector's functionality, but don't have room on your screen for the side panel.

To control which tabs are displayed, and in which order, click the settings icon in the upper-right corner of the message editor (above the Inspector panel), then select Message editor.

New domain name for the public Burp Collaborator server

We've added a new domain name for the public Burp Collaborator server. Unless you have configured Burp to use a private Collaborator server, Burp Scanner and the Burp Collaborator client will now use *.oastify.com for their Collaborator payloads instead of *.burpcollaborator.net. This will help to reduce false negatives, enabling you to identify out-of-band vulnerabilities that were previously hidden due to widespread blocking of the old domain name.

This new domain name is in addition to the old one, so you'll still be able to see interactions with any of your existing *.burpcollaborator.net payloads.

Please note that if you're running Burp within a closed network and previously had to allow connections to *.burpcollaborator.net on port 443 in order to poll for interactions, you may need to do the same for *.oastify.com.

Detect DOM-based vulnerabilities that rely on API calls

Burp Scanner's dynamic JavaScript analysis can now fetch data from out-of-scope API endpoints if required to load the page correctly. This enables it to detect DOM-based vulnerabilities where malicious input is only passed to a sink if an API call is made.

Note that although Burp Scanner fetches external resources and data when required, it will not perform any additional crawl or audit of out-of-scope URLs.

Rows of tabs no longer switch places when selected

In previous versions of Burp, when you had multiple rows of tabs, the selected row would automatically shift to the bottom. This could make it difficult to keep track of the order of tabs, which was particularly inconvenient in Burp Repeater.

We've now disabled this behavior, so tabs no longer move when selected.

Security fix

We have upgraded Burp's browser to Chromium 99.0.4844.74, which fixes one critical bug and a number of high / medium severity bugs.

Bug fixes

This release also provides a number of bug fixes. Most notably:

Burp Scanner no longer has issues when redirects are triggered by onload event handlers in the HTML <body> tag.

We have fixed a bug that prevented you from reading or editing long lines of JSON in some of the message editor panels.

We have fixed a syntax error on the splash screen that appears when launching Burp.
