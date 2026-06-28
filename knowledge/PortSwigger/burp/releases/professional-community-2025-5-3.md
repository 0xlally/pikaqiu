# Professional / Community 2025.5.3

Source: https://portswigger.net/burp/releases/professional-community-2025-5-3
Fetched: 2026-06-28T09:16:53.561294+00:00

This release introduces AI-powered custom actions in Burp Repeater, Montoya API updates for improved extension settings integration, and quality of life updates across Burp Suite.

AI-powered custom actions in Repeater

Burp Repeater now supports custom actions enhanced with AI, enabling real-time, context-aware analysis of HTTP

messages.

To help you get started, we've added a sample AI custom action that explains selected text. You can load it from the empty Custom actions panel by clicking Add samples. You can also use it as a template for new custom actions, by clicking New > From template. For guidance on creating your own AI features, see Developing AI features in custom actions.

Running an AI-powered custom action uses AI credits. The cost depends on the number and complexity of the AI requests. To check your credit balance, click the AI icon in the button-right corner of Burp.

All AI interactions are handled within Burp Suite's secure AI infrastructure, and your data is never used to train AI models. For more information, see our AI security, privacy and data handling documentation page.

Custom actions are only available in Burp Suite Professional.

Extensions can add custom settings panels

Extensions can now add panels directly into the Settings dialog using the SettingsPanel interface of the Montoya API. These panels appear in Settings > Tools > Extensions, listed under the extension's name. This means that extension developers no longer need to create separate tabs or menu items for settings, reducing clutter and making extension settings easier to find.

Quality of life improvements

We've added the following quality of life improvements:

Custom actions can now access timing data, so you can log or act on response timing.

The Change body encoding context menu option now enables you to quickly switch between form URL-encoding, multipart encoding, and JSON.

When Burp is set to drop all out-of-scope requests, it now also blocks TLS pass through connections to out-of-scope hosts by default.

We've added a new custom action template that tests how a server responds to repeated requests, making it easier to test for race condition vulnerabilities. To view the template, go to the Custom actions side panel in Repeater, click New > From template, then select Trigger race condition.

Bug fixes

We've made the following bug fixes:

Repeater tabs can now send requests correctly after being removed from a group that used the Send group option.

The Save OpenAPI requests to site map context menu option now correctly populates the site map with the actual API definition endpoint instead of the hostname.

In Burp Intruder, the Max integer digits value now updates when using the Numbers payload type with a From value that is bigger than the To value.

Burp Intruder now respects two-digit hex formatting when using a Numbers payload with a range ending in f.

Browser upgrade

We've upgraded Burp's browser to Chromium 137.0.7151.69 for Windows & Mac and 137.0.7151.68 for Linux. For more information, see the Chromium release notes.
