# Burp AI data handling

Source: https://portswigger.net/burp/documentation/burp-ai/trust/data-handling
Fetched: 2026-06-28T09:15:31.009583+00:00

Support Center

Documentation

Burp AI

Burp AI trust and compliance FAQ

Burp AI data handling

DASTProfessional

Burp AI data handling

Last updated:

June 18, 2026

Read time:

3 Minutes

When you use Burp AI, we send data to PortSwigger's AI infrastructure, which manages communication with the AI provider. This page explains how that data is validated and processed, and the controls in place to protect it.

Request: Your data, such as an HTTP request or vulnerability description, is sent to PortSwigger's AI infrastructure. In Burp Suite Professional, this is sent from your desktop client. In Burp Suite DAST, it is sent from a dedicated scanning resource created specifically to handle the investigation.

Authentication: We verify your license. Only licensed users can access the AI service.

Task processing: Once the license check passes, a temporary processing agent is created. Your data is then passed to this agent. This agent is created specifically to handle your request, is decommissioned immediately after the task is complete, and is never reused across requests or users.

Provider transmission: The agent passes your data to the AI provider.

Provider processing: The AI provider processes your data, and returns a response to Burp. It does not retain any of your data once processing is complete.

Storage: PortSwigger stores your prompt, the AI response, and related metadata in its internal systems. This information is retained to support troubleshooting, auditing, and billing.

All data transmitted between Burp, PortSwigger, and our AI providers is encrypted using TLS 1.2 or later.

More information

For more information on what data is stored when you use Burp AI and how PortSwigger keeps that data safe, see Data storage and retention.

Data sent to AI providers

All Burp AI features use the same infrastructure. However, the data sent to AI providers varies depending on the feature you are using. Our agreements with AI providers prohibit them from monitoring, storing, or training on your data.

Explain this

Burp AI sends:

The highlighted text or code snippet

The context type (for example, REQUEST_HEADERS or RESPONSE_BODY)

Explore Issue / AI-enhanced scanning

Burp AI sends:

The full HTTP request and response pair in which the issue was found, including headers

The issue name, target URL, and insertion point

The origin scan ID and site ID (Burp Suite DAST only)

Burp AI in Repeater

Burp AI sends:

The full HTTP request and response pair from the Repeater tab you ran the task from, including headers

Your prompt

Any notes attached to the tab

False Positive Analysis

Burp AI sends:

A screen capture of the vulnerability finding

The associated HTTP request and response

Broken Access Control

Burp AI sends a screenshot of the page content returned during the access check.

Recorded Logins

Burp AI sends:

The page text

HTML attributes of interactive elements

A screen capture of the page

Sensitive data handling

Burp AI does not automatically redact or mask the data sent to AI providers. Depending on the features you use and the traffic you're testing, this may include sensitive data.

As an exception, AI-generated recorded logins replace actual usernames and passwords with placeholders before they are sent to PortSwigger. This is the same behavior as manually-recorded logins.

Models used by Burp AI

Burp AI uses a multi-model approach to ensure the best results for a wide range of security testing tasks. We currently use models from OpenAI and Anthropic.

We select models based on extensive performance testing. We match each feature to the model that delivers the most accurate and reliable results for that task. We only use models that meet our strict data privacy standards and providers that can guarantee your data is not used for training.

Our infrastructure manages Burp AI's connection to these models, enabling us to upgrade model versions after they have been assessed by PortSwigger. These updates happen automatically, giving you access to current AI versions without the need to update Burp.

Geographic locations

Our AI providers (OpenAI and Anthropic) process data in United States data centers.

When you use Burp AI, data is sent between PortSwigger's AWS infrastructure and these data centers. PortSwigger infrastructure is located in the AWS US-East (Virginia) and EU-West (Ireland) regions.

Routing between PortSwigger's US and EU regions is handled automatically, based on latency. You cannot currently elect to have data processed in a specific geographic location.
