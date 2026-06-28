# Lab: Exploiting AI agents to exfiltrate sensitive information

Source: https://portswigger.net/web-security/llm-attacks/ai-powered-scanner-vulnerabilities/lab-sensitive-information-exfiltration
Fetched: 2026-06-28T09:17:54.689169+00:00

Web Security Academy

Web LLM attacks

AI-powered scanner vulnerabilities

Lab

Lab: Exploiting AI agents to exfiltrate sensitive information

This lab is vulnerable to indirect prompt injection. The application features an AI-powered scanner that has access to sensitive user data, including API keys, while performing site audits. The scanner has been given the login credentials for carlos so it can explore authenticated areas of the site.

You can log in to your own account using the following credentials: wiener:peter.

To solve the lab, exfiltrate and submit the API key for the user carlos.

To scan a site, select a blog post and click Scan site.

Note

This lab uses a live LLM, which can be unpredictable. If the LLM does not respond as expected, you may need to rephrase your prompts or repeat the scanning process.

Required knowledge

To solve this lab, you need to know how indirect prompt injection can be used to manipulate an LLM's behavior via third-party content.

For more information, see our AI-powered scanner vulnerabilities topic.

Data collection

Labs in this sub-topic collect telemetry data, including AI interaction logs. For details on what data they collect and how we use it, see our Academy Lab Telemetry Privacy Notice.

Solution

The solution for this lab will be published shortly. Check back soon.

Test for vulnerabilities using Burp Suite

Try for free
