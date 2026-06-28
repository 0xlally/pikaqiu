# Professional / Community 2025.2.3

Source: https://portswigger.net/burp/releases/professional-community-2025-2-3
Fetched: 2026-06-28T09:16:51.692341+00:00

This release introduces Burp AI, a powerful set of AI features designed to enhance your security testing workflow. We've also added a Bambda library for storing and reusing Bambdas, plus a ready-to-use extension starter project to streamline extension development.

AI features now available in Burp

Burp's new AI features enhance your testing workflow by helping you to save time on manual tasks, understand complex issues faster, and focus your effort where it matters most.

Burp AI includes:

Explore Issue - Autonomously investigates vulnerabilities identified by Burp Scanner, saving you time and effort. Explore Issue follows up like a human pentester - attempting exploits, identifying additional attack vectors, and summarizing findings so you can validate and demonstrate impact more efficiently.

Explainer - Helps you to quickly understand unfamiliar technologies without leaving Burp Suite. Highlight any part of a Repeater message and click a button to get an AI-generated explanation.

Broken access control false positive reduction - Burp enhances Broken Access Control scan checks by intelligently filtering out false positives before they appear in results, letting you concentrate on real threats.

AI-powered recorded logins - Configuring authentication for web apps can be time-consuming and error-prone. Burp can use AI to generate recorded login sequences automatically, saving time and reducing the risk of human error.

AI-powered extensions - The Montoya API now enables you to add advanced AI features into your Burp Suite extensions. There's no need for complex setup, such as managing API keys, as all AI interactions are handled within Burp Suite's secure AI infrastructure.

For more information on AI features in Burp, see the Burp AI documentation.

As part of these changes, we've updated our data processing agreement to cover new AI service provider processes.

AI features are currently available only in Burp Suite Professional.

AI credits

We've also introduced AI credits, an easy way to pay for AI features in Burp. Whenever you use an AI-powered tool or an extension that interacts with an AI model, credits are deducted from your balance. To help you get started, we've given you 10,000 free AI credits. This is equivalent to 5 US dollars worth of AI requests.

AI security and privacy

Burp's AI features only run when you choose to use them. All AI requests are processed securely through PortSwigger’s trusted AI infrastructure, and your data is never used to train AI models​. For more information on security and privacy in Burp's AI features, see our AI security, privacy and data handling documentation page.

Bambda library

We've added a Bambda library to Burp. Bambdas are small sections of code that you can run directly from Burp Suite's interface to quickly personalize various tasks, such as creating custom match-and-replace rules, table columns, and filters.

The new library makes it easy to store, manage, and reuse Bambdas in any Burp tool that supports them. To build your collection, you can import Bambdas that have been shared with you or downloaded from the Bambdas GitHub repository. To access a wide selection of ready-to-use Bambdas, you can even import the entire repository. The library also includes built-in templates to help you start writing your own Bambdas.

To access the library, go to Extensions > Bambda library. For more information, see Managing Bambdas in your Bambda library.

Extension development starter project

You can now download a ready-to-use extension starter project from Burp, enabling you to start developing Montoya API extensions more easily.

To get started, go to Extensions > APIs, click Download starter project, then open the project in your IDE. The project includes essential configuration files and a template extension file so you can begin coding immediately.

For detailed setup instructions, see Setting up your extension development environment using the starter project.

Montoya API updates for writing Bambdas and extensions

We've made the following updates to the Montoya API, improving support for writing Bambdas and extensions:

You can now obtain the unique project file ID that the project uses internally, alongside the project file name.

You can now retrieve parameters without specifying their type.

Quality of life improvements

We've made the following quality of life improvements:

Intruder now retains capture and view filter settings when repeating an attack. This prevents settings from resetting to default, saving you time when refining your attacks.

We've added a session handling action that lets you modify any part of a request sent by Burp. It is useful for broad modifications, such as updating JSON content. For more information, see Replace matching part of the request.

We've added a Load behavior setting that prevents the extension load dialog from appearing by default when you reload an extension. This streamlines extension development. If you prefer to see the dialog, enable the setting.

Bug fixes

We've fixed a bug where the Burp Collaborator Source IP address column was empty for DNS requests over IPv6. It now correctly displays the source IP address.

Browser update

We've upgraded Burp's browser to Chromium 134.0.6998.178 for Windows, 134.0.6998.166 for Mac, and 134.0.6998.165 for Linux. For more information, see the Chrome for Developers release notes.
