# Using AI extensions

Source: https://portswigger.net/burp/documentation/desktop/extend-burp/extensions/using-ai-extensions
Fetched: 2026-06-28T09:15:48.288454+00:00

Support Center

Documentation

Desktop editions

Extending Burp

Extensions

Using AI extensions

Professional

Using AI extensions

Last updated:

June 18, 2026

Read time:

2 Minutes

Burp's AI-powered extensions enhance and automate your testing workflow. This page explains how to enable AI-powered extensions and how the AI credit system works.

Using AI credits

AI credits are required to use AI features in Burp Suite. When an extension interacts with an AI large language model (LLM), it deducts credits from your AI credit balance. Different interactions require different amounts of credits depending on the number and complexity of AI requests needed.

You can buy AI credits from My Account on the PortSwigger site. You must have a Burp Suite Professional license associated with your account to buy AI credits.

More information

For more information on how AI credits work, see AI credits.

Checking AI credit use

To see your AI credit balance, click the AI icon in the bottom-right corner of Burp.

To see how many credits an extension has used, go to Extensions > Installed. The AI credits used column shows the credits used by each extension during the current Burp session.

If you start to run low on credits, Burp displays a reminder dialog with a link to buy more.

Enabling AI for extensions

By default, AI features are disabled for all extensions to keep you in control of how and when Burp uses AI. You need to manually enable AI functionality for any extensions you want to be able to make AI calls.

When you install an AI-powered extension from the BApp store, Burp asks whether you want to enable AI features for that extension.

You can enable or disable AI for extensions you have already installed. To enable AI for an extension:

Select Extensions > Installed, and find the extensions you want to manage.

Select the Use AI checkbox for those extensions.

More information

Installing extensions

Managing extensions

Data and privacy

PortSwigger does not collect data from AI-powered extensions by default. What data is processed depends entirely on the extension's implementation. PortSwigger reviews BApp Store extensions for quality and compatibility, but cannot guarantee their behavior. If you are working in regulated or legally sensitive environments, review the extension's code and documentation to understand what data is sent externally and consider additional safeguards before acting on AI output.

More information

For more information on how Burp AI handles your data, see the Burp AI trust and compliance FAQ.
