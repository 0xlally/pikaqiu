# Professional / Community 2022.11.2

Source: https://portswigger.net/burp/releases/professional-community-2022-11-2
Fetched: 2026-06-28T09:16:36.569282+00:00

In this release, we have significantly improved the usability of Burp's user and project options. We have also added new functionality to DOM Invader and the Montoya API.

User and project options refactor

We have moved all of the options in the User options and Project options tabs to a new Settings dialog, accessible from a button on the main toolbar or by a configurable hotkey.

This new dialog improves the layout and navigation of Burp's options in several ways:

You can now access all user and project settings in one window.

You can now use search and filter commands to find the settings you need.

Following extensive UX research, we have rearranged the available settings into a more logical structure.

Each setting in the dialog has a marker indicating whether it is a user-level or project-level setting. For settings that can apply at either level, there is an Override options for this project only toggle that enables you to select the level at which the setting should apply.

DOM Invader: Detect cross-origin data leaks via web messages

DOM Invader can now detect when the current page sends a web message containing data from the URL to a different target origin. In this case, an attacker can potentially steal sensitive data, such as OAuth tokens, by embedding the affected page in an iframe, along with an event listener that extracts the data.

Testing for these vulnerabilities manually is a laborious task, but DOM Invader can automate most of this process for you. Just enable the Detect cross-domain leaks option from DOM Invader's web message settings:

DOM Invader: Remove Permissions-Policy header

You can now configure DOM Invader to strip the Permissions-Policy header from responses.

Some websites set directives via the Permissions-Policy header that block features that are essential to DOM Invader's functionality, such as synchronous XHR. In this case, DOM Invader informs you via the console and prompts you to enable the Remove permissions policy header option from the settings menu.

Proxy WebSocket listener support for Montoya API

You can now use the Montoya API to intercept and modify proxied WebSocket messages.

Minor improvements

This release includes several minor improvements to Burp Suite's tools, including:

You can now scan a selected insertion point only, without the need to run a full scan.

You can now load or unload multiple extensions at once via a new context menu option on the Extensions table.

We have added a search text field to the Edit hotkeys dialog, enabling you to filter the table of hotkeys.

Browser upgrade

We have upgraded Burp's browser to Chromium 107.0.5304.110, which fixes a number of high-severity security issues.

Bug fix

We have fixed a bug whereby requests were sometimes not rendering correctly in the message editor.
