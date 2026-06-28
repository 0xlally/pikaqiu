# Burp AI data storage and retention

Source: https://portswigger.net/burp/documentation/burp-ai/trust/data-storage
Fetched: 2026-06-28T09:15:31.052012+00:00

Support Center

Documentation

Burp AI

Burp AI trust and compliance FAQ

Burp AI data storage and retention

DASTProfessional

Burp AI data storage and retention

Last updated:

June 18, 2026

Read time:

2 Minutes

PortSwigger stores data about your Burp AI usage to support reliability, account management, and the ongoing improvement of our AI features. This data is protected using industry-standard encryption and strict access controls.

This page explains what we store and how we keep it safe.

Data we collect

When you use Burp AI, we collect the following data:

Your prompts and AI responses.

Any data you include as context, such as highlighted HTTP headers or code snippets.

Task metadata, such as which Burp AI feature was used, issue details, and target URLs.

The timestamp at which the request was started.

Details of your license.

Token counts, credit consumption, and request counts to facilitate billing.

Note

The specific data collected for each request depends on the feature used. For a full breakdown of what each feature sends, see Data handling.

Retention periods

The length of time we retain data depends on its type and purpose:

Conversation and audit data (the record of your prompts, AI responses, and associated task details) is retained indefinitely to support troubleshooting and long-term feature development.

Operational logs (such as error and infrastructure logs) are deleted after 31 days.

Account identifiers are deleted after 7 days of inactivity.

Access control and security

All stored data is encrypted using AES-256.

Only authorized PortSwigger staff can access your data, and can only do so when necessary to support troubleshooting or resolve an issue. Access is managed through role-based permissions, and every internal interaction with your data is individually logged for accountability and audit purposes.

How your data may be used

Our contracts with OpenAI and Anthropic explicitly prohibit them from using your data to train their models.

PortSwigger reserves the right to use anonymized data to improve Burp AI features.

Geographic location

PortSwigger's storage infrastructure is located in the AWS US-East (Virginia) and EU-West (Ireland) regions.

Requests are automatically routed between regions based on latency. You cannot currently request that data is stored in a specific geographic location.

More information

For more information on the legal frameworks governing your data, see our Data Processing Agreement.
