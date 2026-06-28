# Burp AI

Source: https://portswigger.net/burp/documentation/dast/user-guide/burp-ai
Fetched: 2026-06-28T09:15:34.603019+00:00

DAST

Burp AI

Last updated:

June 18, 2026

Read time:

2 Minutes

Cloud

Burp Suite DAST includes AI-powered features that help you to triage issues faster and to simplify scan setup.

Note

Burp AI in Burp Suite DAST is currently in a limited access beta and is not available to all customers.

Burp AI features in DAST

Burp Suite DAST includes:

AI-enhanced scanning

AI-enhanced scanning automatically investigates issues found during a scan to see if they can be reproduced and exploited. Burp AI uses evidence from Burp Scanner to plan and execute targeted validation steps. It then displays its results on the issue detail page, including an impact analysis and manual reproduction steps, to help you prioritize and resolve issues faster.

Related pages

For more information on AI-enhanced scanning, see Configuring AI-enhanced scanning.

AI-powered recorded logins

Configuring authentication for web apps can be time-consuming and error-prone. Burp Suite DAST can use AI to generate recorded login sequences automatically, saving time and eliminating the possibility of human error.

Related pages

For more information on AI-generated recorded login sequences, see Using recorded logins.

Enabling Burp AI features in your DAST instance

Burp AI features only appear in Burp Suite DAST if they have been enabled for your instance. You must have the Enable/Disable Burp AI for the installation permission to enable Burp AI.

To enable Burp AI in DAST:

From the settings menu, select Burp AI.

Activate the Enable Burp AI toggle.

Click Save.

Security and privacy

We've designed Burp Suite DAST's AI features with security, privacy, and transparency in mind:

AI features only run when you choose, giving you full control over when and where they execute.

AI request data is processed securely through our trusted AI infrastructure. It is never stored by our AI providers.

Burp AI complies with ISO 27001 standards and implements robust encryption, ensuring data is protected in transit and at rest.

Related pages

For more information on trust and safety in Burp AI, see the Burp AI trust and compliance FAQ.
