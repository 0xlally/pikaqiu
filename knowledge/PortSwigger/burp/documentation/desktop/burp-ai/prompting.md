# Prompting best practices with Burp AI

Source: https://portswigger.net/burp/documentation/desktop/burp-ai/prompting
Fetched: 2026-06-28T09:15:44.960226+00:00

Support Center

Documentation

Desktop editions

Burp AI

Prompting best practices with Burp AI

Professional

Prompting best practices with Burp AI

Last updated:

June 18, 2026

Read time:

4 Minutes

In Repeater, Burp AI enables you to analyze, explain, and test HTTP messages using natural language prompts. Burp doesn't require any specific prompt format, but you can get better results by following a few simple guidelines. Clear, specific prompts produce more accurate answers and are more efficient.

This page explains how to write effective prompts for Burp AI, refine them through iteration, and use them efficiently within your testing workflow.

Writing effective prompts

A good prompt is specific, concise, and focused on a single task. Overly broad questions can produce vague answers.

Be specific and goal-oriented

Clearly describe what you want Burp AI to do.

Inefficient: Check security.

Efficient: Check this login response for signs of SQL injection in the username parameter.

Making your prompts specific helps Burp AI stay focused and reduces the complexity of the requests sent to PortSwigger's AI infrastructure.

Use context strategically

Burp AI automatically includes the active request and response as context, but you can refine what it pays attention to by highlighting key sections or adding observations in the Notes panel.

These contextual hints help the AI to target areas with the most potential impact.

Stay focused

Long or unfocused prompts can make it harder for Burp AI to give accurate, relevant answers. Keeping your prompt short, clear, and targeted helps the AI to stay focused and produce more useful results.

If you only need a summary or a specific format, say so explicitly.

Example

Summarize the key exploitation steps and suggest one remediation approach.

Guide the format

You can specify the format of Burp AI's response directly in your prompt.

Example

Summarize the issue using this format:

- Root cause

- Exploitation steps

- Recommended remediation

Include scenario details

When testing business logic or access control, explain expected behavior so Burp AI can reason correctly.

Providing this kind of context helps Burp AI to distinguish normal behavior from vulnerabilities.

Example

This is a user management API. Users should only be able to access their own records.

Reference known security categories

Referencing recognized vulnerability classes keeps your prompt focused and gives Burp AI a "starting point" in its analysis.

Example

Analyze this request for IDOR vulnerabilities. Check whether user IDs are properly enforced.

Write complete prompts

Because each task runs independently, make sure your prompt includes any key information Burp AI needs, such as the scenario, expected behavior, or specific values to examine. However, avoid copying entire traffic logs or issue histories unless they are relevant. Focused prompts with the right context tend to give clearer, more accurate answers.

Avoid follow-up style prompts such as Now check for XSS. Instead, create a separate task with its own focused prompt.

Example

Summarize why this request triggers a 500 Internal Server Error. Focus on possible input handling or database errors.

Example prompts for common testing scenarios

The following examples show how clear, targeted prompts help Burp AI deliver high-quality results.

Explaining a vulnerability

Poor prompt: Explain everything about this issue and how to fix it.

Better prompt: Summarize the cause of this XSS issue and recommend a remediation step.

Why it works: Focused intent produces more relevant output that you can use directly in your report.

Reviewing HTTP traffic

Poor prompt: Analyze this entire log.

Better prompt: Identify any suspicious parameters in this request.

Why it works: Narrowing the scope helps Burp AI to concentrate on meaningful indicators rather than returning generic information.

Investigating access control

Poor prompt: Check all responses for issues.

Better prompt: Evaluate whether this endpoint allows unauthorized access.

Why it works: A clear, single objective makes it easier for Burp AI to identify and investigate potential access control flaws.

Interpreting unusual responses

Poor prompt: Why is this broken?

Better prompt: Explain why this request returns 500 Internal Server Error while the same request with ID=4 returns 200 OK.

Why it works: The improved prompt gives Burp AI context and a clear comparison, helping it to focus on possible causes.

Generating test payloads

Poor prompt: Give me payloads.

Better prompt: Suggest two example payloads to test for reflected XSS in the search parameter.

Why it works: Defining the vulnerability type and parameter guides Burp AI toward useful, accurate examples.

Summarizing findings

Poor prompt (in a reporting context): What's going on here?

Better prompt for summarizing and reporting: Summarize the main security issues in this response, grouped by issue type, and include one short remediation suggestion for each.

Why it works: The revised version sets a clear structure for the output and prompts Burp AI to produce concise, actionable results.

Note

If your goal is to learn or explore an unfamiliar issue, a broader prompt like "What's going on here?" can be useful, especially when you're not sure what to look for yet. The same wording can be effective in an exploratory or educational context, where open-ended responses are welcome.

More information

Using Burp AI in Repeater
