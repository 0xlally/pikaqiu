# Professional / Community 2025.2

Source: https://portswigger.net/burp/releases/professional-community-2025-2
Fetched: 2026-06-28T09:16:51.461599+00:00

This release introduces AI support to the Montoya API, enabling you to build smarter, AI-powered extensions. We've also added a Bambda library for storing and reusing Bambdas, plus a ready-to-use extension starter project to streamline extension development.

Support for AI-powered features in Montoya API extensions

We've added built-in AI support to the Montoya API. Your extensions can now securely interact with a large language model (LLM) through PortSwigger’s purpose-built AI platform, enabling you to build advanced automation and data analysis features with no need for complex setup or external API keys.

We've also introduced AI credits, an easy way to pay for AI features in Burp. When an extension interacts with an LLM, credits are debited from the user's balance, with the cost varying based on the complexity of requests. To help you start using and creating AI-powered extensions, we've given you 10,000 free AI credits. This is equivalent to 5 US dollars worth of AI requests.

To see what's possible with AI-powered extensions, check out the AI-enhanced Hackvertor extension by PortSwigger researcher Gareth Heyes. The AI-enhanced version of Hackvertor can:

Generate custom transformation tags based on natural language descriptions.

Create custom tags in JavaScript, Python, Java, or Groovy based on AI-generated code.

Automatically generate encoding/decoding tags by analyzing Repeater traffic.

For more information on the Montoya API's new AI features, including information on how we protect your data and ensure AI-powered interactions remain secure, see the Creating AI extensions documentation.

As part of these changes, we've updated our data processing agreement to cover new AI service provider processes. You'll need to accept the new End User Licence Agreement (EULA) when you update to the new version of Burp.

Bambda library

We've added a Bambda library to Burp, making it easy to store, manage, and reuse Bambdas in any Burp tool that supports them.

To build your collection, you can import Bambdas that have been shared with you or downloaded from the 2025.2-early-adopter branch of our Bambdas GitHub repository. To access a wide selection of ready-to-use Bambdas, you can even import the entire repository. The library also includes built-in templates to help you start writing your own Bambdas.

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

We've upgraded Burp's browser to Chromium 133.0.6943.54 for Windows & Mac and 133.0.6943.53 for Linux. For more information, see the Chrome for Developers release notes.
