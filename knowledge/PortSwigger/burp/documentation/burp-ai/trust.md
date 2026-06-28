# Burp AI trust and compliance FAQ

Source: https://portswigger.net/burp/documentation/burp-ai/trust
Fetched: 2026-06-28T09:15:31.051003+00:00

Support Center

Documentation

Burp AI

Burp AI trust and compliance FAQ

DASTProfessional

Burp AI trust and compliance FAQ

Last updated:

June 18, 2026

Read time:

5 Minutes

This page answers some common questions around how we protect your data when you use Burp AI.

Related pages

Data handling - A deeper dive into how Burp AI handles your data in transit, what each feature sends, and how we handle sensitive data.

Data storage and retention - What PortSwigger stores, how long we keep it, and who can access it.

Data and privacy

Can AI providers use my data to train their models?

No. Our contracts with our providers prohibit them from monitoring your data or using it for model training. Your data passes through provider infrastructure during processing, but the provider does not retain it once the request is complete, and our contracts prohibit any secondary use.

Do AI providers store or retain my data?

No. Burp's AI providers do not store any of the data they process. Requests are handled in real time and immediately returned to Burp.

Does Burp AI send sensitive data?

Burp AI only runs against targets you have explicitly told it to test:

In Burp Suite Professional, it runs when you click a button.

In Burp Suite DAST, it can run automatically after a scan, but only against sites you have configured.

In both products, we do not automatically redact or mask the data sent to AI providers. Depending on the features you use and the traffic you're testing, this may include sensitive data.

As an exception, AI-generated recorded logins replace actual usernames and passwords with placeholders before they are sent to PortSwigger or the AI providers. This is the same behavior as manually-recorded logins.

For a full breakdown of what each feature sends, see Data handling.

What data does PortSwigger store?

PortSwigger stores your prompts, AI responses, and associated metadata to support troubleshooting, auditing, and billing. All stored data is encrypted using AES-256, and only authorized PortSwigger staff can access it. For full details on retention periods and access controls, see Data storage and retention.

Does PortSwigger use my data to improve Burp AI?

PortSwigger reserves the right to use anonymized data to improve Burp AI features and diagnose issues.

How does Burp communicate with AI providers?

When you use Burp AI, data is sent to PortSwigger's AI infrastructure, which manages communication with the AI provider:

In Burp Suite Professional, data is sent from your desktop client.

In Burp Suite DAST, data is sent from a dedicated scanning resource created specifically to investigate the issue. Your scan results and issue data remain in your own database, which PortSwigger cannot access.

The provider does not monitor your data or retain it once processing is complete. All communication between Burp, PortSwigger, and our AI providers is encrypted using TLS 1.2 or later.

For more information on how this process works and what is sent, see Data handling.

Compliance

Is Burp AI covered by PortSwigger's Data Processing Agreement?

Yes. PortSwigger's Data Processing Agreement covers all personal data processed through Burp AI on your behalf.

Is Burp AI ISO 27001 compliant?

Yes. Burp AI is covered by PortSwigger's ISO 27001 certification. For full details, see our Trust Center.

Where is data processed?

PortSwigger's AI infrastructure runs on AWS in the US-East and EU-West regions. Our AI providers process requests in US data centers.

What security controls protect your AI infrastructure?

Our AI infrastructure has protections against common attack types, including prompt injection and data exfiltration. Specific controls include server- and client-side input validation, rate limiting, and token-based authentication.

What happens if there's a security incident involving an AI provider?

In this case, PortSwigger would respond according to its ISO 27001-aligned incident response process and its contractual obligations with the affected provider. AI usage is logged in an encrypted audit trail to support our investigations.

What happens if an AI provider goes down?

We operate failover systems to maintain availability if a provider experiences issues. If the primary provider for a given feature is unavailable, requests are automatically routed to a backup.

User controls

Can I disable Burp AI entirely?

Yes, you can disable Burp AI in both Burp Suite Professional and Burp Suite DAST:

Burp Suite Professional: You can disable Burp AI at any time, at either a global or project level. Go to Settings > Burp AI and select Disable AI features. When Burp AI is disabled, Burp cannot access PortSwigger's AI infrastructure and all AI-related features are grayed out in the UI.

Burp Suite DAST: Access to Burp AI is managed at the organization level by an administrator. To enable or disable Burp AI, go to Settings > Burp AI and toggle Enable Burp AI. You must have the Enable/Disable Burp AI for the installation permission to do this. When Burp AI is disabled, AI features are removed from the UI and any AI results from previous scans are hidden.

Does Burp AI run automatically?

No. All Burp AI features require explicit setup before they can run:

Burp Suite Professional: Burp AI only runs when you actively use an AI feature. It does not send any data to PortSwigger or our AI providers in the background.

Burp Suite DAST: Burp AI features are not available by default. An administrator must enable Burp AI for your installation before any AI features appear in the UI. Once enabled, Burp AI features only run if you have configured them for a specific site. No data is sent to PortSwigger or our AI providers unless Burp AI has been enabled and configured.

Can I stop Burp AI mid-task?

Yes, you can stop Burp AI mid-task in both Burp Suite Professional and Burp Suite DAST:

Burp Suite Professional: For multi-step processes such as Explore Issue or Repeater tasks, you can pause or stop execution at any time from the Tasks panel.

Burp Suite DAST: To stop AI-enhanced scanning, cancel the scan.

Can I control which targets Burp AI analyzes?

Yes. You can use Burp's scope settings to restrict Burp AI to specific hosts and URLs. In DAST, you can also control which issue severity and confidence combinations Burp AI investigates on a per-site basis.

For more information on setting scope in Burp Suite Professional, see Target scope.

For more information on setting scope in Burp Suite DAST, see Configuring AI-enhanced scanning.

How does Burp AI stay focused on security testing tasks?

Burp AI uses structured prompts to keep the AI focused on security testing, reducing the risk of hallucinations or unintended actions. There are also built-in limits on the number of steps the AI can take during a task.

In Burp Suite DAST, AI-enhanced scanning has additional guardrails that block destructive HTTP methods (such as DELETE and PUT) and SQL operations that could cause data loss. These run automatically and cannot be disabled by users.

Can I choose which AI provider or model Burp uses?

Not currently. PortSwigger selects the model used for each task based on performance testing. For more information on how we select and manage models, see Data handling.
