# Burp AI

Source: https://portswigger.net/burp/documentation/desktop/burp-ai
Fetched: 2026-06-28T09:15:44.655754+00:00

Support Center

Documentation

Desktop editions

Burp AI

Professional

Burp AI

Last updated:

June 18, 2026

Read time:

3 Minutes

Burp Suite includes AI-powered features designed to enhance your security testing workflow. They enable you to uncover vulnerabilities more efficiently, understand complex web technologies, and streamline authentication setup.

Burp's AI features prioritize privacy and security, to keep your data safe and make sure you remain in full control of the testing process. None of the features run unless you explicitly activate them.

Getting started with AI in Burp

To start using Burp's AI features, you need AI credits. AI credits give you access to Burp Suite's AI-powered features. Whenever you use an AI-powered tool or extension, credits are deducted from your balance.

You can buy AI credits from My Account on the PortSwigger site.

To check your AI credit balance, click the AI icon in the bottom-right corner of Burp.

More information

For more information on how AI credits work, see AI credits.

AI features in Burp

Once you have AI credits, you're ready to start using Burp's AI-powered tools. These include:

Burp AI in Repeater

Burp AI is built into Repeater, enabling you to run custom prompts against any tab. This flexible workflow gives you full control over what Burp AI examines, making it easy to tailor each task to your needs. For example, you can analyze a suspicious request, test for a specific vulnerability, or ask for suggestions on what to try next when you're unsure how to proceed.

More information

Using Burp AI in Repeater

Prompting best practices with Burp AI

Explore Issue

Explore Issue autonomously investigates vulnerabilities identified by Burp Scanner, saving you time and effort. It follows up on issues like a human pentester would - attempting exploits, identifying additional attack vectors, and summarizing findings so you can validate and demonstrate impact more efficiently.

More information

For more information on Explore Issue, see Exploring Issues with AI.

Explainer

Explainer enables you to quickly understand unfamiliar technologies without leaving Burp Suite. Highlight any part of a Repeater message and click a button to get an AI-generated explanation. Explainer provides instant insights into headers, cookies, JavaScript functions, and more, to help you quickly identify potential security implications without disrupting your workflow.

More information

For more information on Explainer, see Generating AI-powered explanations.

Broken access control false positive reduction

False positives in automated security testing can waste valuable time. Burp enhances Broken Access Control scan checks by intelligently filtering out false positives before they're reported, helping to free up your time to focus on real threats.

More information

For more information on BAC false positive reduction, see Configure AI scan enhancements.

AI-powered recorded logins

Configuring authentication for web apps can be time-consuming and error-prone. Burp can use AI to generate recorded login sequences automatically, saving time and eliminating the possibility of human error.

More information

For more information on AI-generated recorded login sequences, see Adding recorded login sequences.

AI-powered extensions

The Montoya API enables you to add advanced AI features into your Burp Suite extensions. Your extensions can send prompts to an AI model, allowing for real-time input analysis and intelligent responses. There's no need for complex setup, such as managing API keys, as all AI interactions are handled within Burp Suite's secure AI infrastructure.

More information

For more information on creating AI extensions, see Creating AI extensions.

AI-powered custom actions in Burp Repeater

Burp Repeater supports custom actions enhanced with AI, enabling real-time, context-aware analysis of HTTP messages.

All AI interactions are handled within Burp Suite's secure AI infrastructure, so there's no need for complex setup, such as managing API keys.

More information

For more information on creating AI custom actions, see Developing AI features in custom actions.

Security and privacy

We've designed Burp's AI features with security, privacy, and transparency in mind:

Full user control - AI features only run when you choose, giving you full control over when and where they execute. You can also disable AI entirely if needed.

Data privacy - AI request data is processed securely through our trusted AI infrastructure. It is never stored by our AI providers.

Industry-standard security - Burp AI complies with ISO 27001 standards and implements robust encryption, ensuring data is protected in transit and at rest.

More information

For answers to common questions about data privacy, compliance, and user controls, see the Burp AI trust and compliance FAQ.

For more information on PortSwigger's security standards, and related documentation, see the PortSwigger Trust Center.

If you have bought AI credits but can't see them in Burp, see Troubleshooting AI connectivity.
