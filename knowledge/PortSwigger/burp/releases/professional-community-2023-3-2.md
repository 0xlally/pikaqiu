# Professional / Community 2023.3.2

Source: https://portswigger.net/burp/releases/professional-community-2023-3-2
Fetched: 2026-06-28T09:16:42.299049+00:00

This release introduces support for Collaborator payloads in Intruder attacks, some SPA scanning improvements, and more upgrades for the the Montoya API, and upgrades to the browser and JRE.

Collaborator payloads in Intruder attacks

We have updated Burp Intruder to enable the use of Collaborator payloads in attacks. This update includes:

A new payload type that generates Collaborator payloads, then inserts these at your configured payload positions.

A payload processing rule that replaces a specified placeholder regex with a collaborator payload. The default placeholder regex already matches a placeholder in the predefined payload lists.

Collaborator interactions that result from an Intruder attack are shown in the Intruder results window, instead of the Collaborator tab.

Montoya API

We have continued to update the Montoya API:

Every request and response now has a unique ID, so you can track which request caused each response.

We have fixed a bug that prevented report generation through the Montoya API. In addition, issue references are now present on extension-generated reports.

We have also continued to update our Montoya API support for WebSockets. You can now right-click a WebSocket message and use the context menu to send the message to your extension.

SPA scanning improvements

This release includes changes that enable Burp Scanner to better handle single-page applications (SPAs).

Bug fix

We have upgraded DOM Invader to fix a bug whereby if a user disabled CSP with prototype pollution functionality enabled, then the system would continue to ignore CSP security headers when the user disabled prototype pollution.

Browser upgrade

This release upgrades Burp's browser to Chromium 112.0.5615.49 for Linux and Mac and 112.0.5615.49/50 for Windows.

Java Runtime Environment (JRE) upgrade

This release upgrades Burp installer JRE to 19.0.2. This upgrade gives several security and performance benefits.
