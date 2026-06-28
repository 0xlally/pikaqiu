# Generating AI-powered explanations

Source: https://portswigger.net/burp/documentation/desktop/tools/repeater/http-messages/ai-explainer
Fetched: 2026-06-28T09:16:07.649255+00:00

Support Center

Documentation

Desktop editions

Tools

Repeater

Working with HTTP messages

Generating AI-powered explanations

Professional

Generating AI-powered explanations

Last updated:

June 18, 2026

Read time:

1 Minute

Explainer provides AI-generated explanations for selected sections of HTTP messages in Repeater. This helps you to interpret key details quickly, enabling you to research unfamiliar message components without leaving Burp Suite or disrupting your workflow.

For example, AI-powered explanations can:

Identify the application framework behind a header.

Clarify JavaScript functionality that may affect security.

Explain obscure headers, cookies, or HTML tags from a security perspective.

Note

AI-powered features require AI credits. To learn more about AI credits, see AI credits.

Generating an AI-powered explanation

To generate an AI-powered explanation:

In Repeater, highlight part of an HTTP request or response. The highlighted section must be between 3 and 1000 characters in length.

Right-click and select Explain this, or use the Ctrl+E / Cmd+E hotkey.

The explanation appears in the Explanations panel on the sidebar.

As with all of Burp's AI-powered features, Explainer requests are processed in real time and not retained by the AI service provider. Burp only sends the part of the message you highlight to the AI.

Tip

For best results, focus on a single feature, such as a header, parameter, or JavaScript function.

Managing explanations

The Explanations panel only appears when you request an explanation. From here, you can:

Expand or collapse explanations - Click or .

Regenerate an explanation - Click to request a new AI response.

Delete an explanation - Right-click the explanation header and select Delete.
