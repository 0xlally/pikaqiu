# Professional / Community 2025.8

Source: https://portswigger.net/burp/releases/professional-community-2025-8
Fetched: 2026-06-28T09:16:54.734686+00:00

This release introduces Burp AI in Repeater, improved streaming support for testing AI-powered applications, and resources for vibe coding Burp extensions with AI.

Burp AI in Repeater

We've added Burp AI to Repeater, enabling you to run AI-powered tasks directly from Repeater tabs. Each task is driven by a custom prompt, giving you full control over what Burp AI does. For example, you can use Burp AI to analyze a suspicious request, test for a specific vulnerability, or ask for suggestions on what to try next.

You can run a Burp AI task from any Repeater tab with a specified target. Simply click the Burp AI button, enter a prompt, and click Send to create your task. You can also choose parts of the message to include as specific context, such as highlighted sections or any notes you've added.

Burp AI displays its results in the Tasks list on the Dashboard, with a step-by-step log of the actions taken by the AI and any findings generated. From here, you can also send AI-generated traffic to Repeater or Intruder for further manual testing.

For more information, see Using Burp AI in Repeater.

Improved streaming support for testing AI-powered applications

We've improved Burp's handling of streaming responses, making it easier to test modern applications that rely on live updates, such as AI-powered applications.

In our previous release, we added support for streaming over HTTP/2. Building on that, Burp now automatically recognizes responses with the text/event-stream MIME type as streaming. This means you no longer need to manually define the URLs for server-sent events (SSE), which are often used in AI and other real-time applications. We've also added syntax highlighting for SSE responses, making it easier to inspect the data structure as it streams in.

To help manage performance when testing streaming applications, we've also added a timeout for streaming responses in Repeater. By default, this is set to 600

seconds (10 minutes). You can change this in the Settings dialog under Tools > Repeater > Streaming response timeout.

Support for vibe coding extensions with AI

We've added a CLAUDE.md file and supporting documentation to help you use large language models (LLMs) to build Burp extensions more efficiently. For example, you could use these resources with LLMs to:

Build extensions faster - Write code, fix errors, and quickly prototype new ideas.

Maintain your extensions - Generate code improvements and respond more quickly to BApp Store

feedback.

Troubleshoot issues with extensions - Analyze extension code more easily to understand how extensions work and identify issues.

To help you get started quickly, we've added the resources to our extension starter project. You can also add them to your own project manually. For instructions, see the documentation on setting up our starter project, or manual setup.

Montoya API updates for writing extensions and Bambda scripts

We've made the following updates to the Montoya API:

Extensions can now programmatically open Burp's Settings dialog. If your extension includes a custom settings panel, it's selected automatically. This helps users quickly find and configure settings. For more information, see Help users find your settings panel.

You can now use the Montoya API to set the caret position in message editors. This gives you more control over cursor placement when building extensions.

You can now use the Montoya API to send raw byte values in HTTP/2 headers. This gives you more control over multi-byte characters, such as in cookie headers, and helps prevent charset encoding issues.

Quality of life improvements

We've made the following quality of life improvements:

You can now send multiple messages at once from Burp Proxy or the Intruder attack results to Repeater and Organizer. Simply select the items you want to send, right-click, and choose the appropriate option.

We've expanded the default file types hidden by the Filter by file extension option to include ico, woff, woff2, ttf, and svg.

Bug fixes

We've fixed the following bugs:

A bug where the Home and End keys didn't work correctly in Repeater when the scrollbar was visible.

A bug that prevented the Add note hotkey from working from Burp Proxy's message editor.

A bug where the Proxy > Logging settings in the Settings dialog weren't saved when reopening a project file.

A bug where HTTP/2

requests sent from Search to some tools were missing headers.

A bug that allowed invalid characters in scan configuration and login names, which could cause save errors or unexpected file behavior.

Browser upgrade

We've upgraded Burp's browser to Chromium 138.0.7204.184 for Windows & Mac, and 138.0.7204.183 for Linux. For more information, see the Chromium release notes.
