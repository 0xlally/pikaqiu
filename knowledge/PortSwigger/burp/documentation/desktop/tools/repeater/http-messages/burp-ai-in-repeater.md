# Burp AI in Repeater

Source: https://portswigger.net/burp/documentation/desktop/tools/repeater/http-messages/burp-ai-in-repeater
Fetched: 2026-06-28T09:16:07.627509+00:00

Support Center

Documentation

Desktop editions

Tools

Repeater

Working with HTTP messages

Burp AI in Repeater

Professional

Burp AI in Repeater

Last updated:

June 18, 2026

Read time:

4 Minutes

Burp AI is an on-demand assistant inside Repeater that helps you analyze, understand, and test HTTP messages efficiently. It acts as a skilled penetration tester, automating mundane tasks while you stay in control of your workflow.

You can use it to:

Quickly validate findings: Ask Burp AI to confirm a suspected vulnerability or replay test cases before deeper investigation.

Automate routine steps: Generate and send payloads, or summarize responses, directly within Repeater.

Explore variations instantly: Use short prompts to try different payloads or bypass techniques without writing them manually.

Capture insight as you go: Turn Burp AI's summaries into reusable notes or report snippets.

Burp AI is designed to augment, not replace, your expertise. It frees up time and resources so you can focus on complex reasoning, creative attack techniques, and impactful results.

Example

While testing an e-commerce application, you notice a response that exposes several user IDs. You suspect these identifiers could be used to access other users' data.

Instead of manually testing each possibility, you ask Burp AI to investigate. It identifies the parameter controlling object access, constructs a series of requests substituting the leaked IDs, and confirms that some return data belonging to other users.

Burp AI then checks related endpoints for similar behavior and summarizes the confirmed insecure direct object reference (IDOR) for reporting.

Running a Burp AI task in Repeater

To run a Burp AI task in Repeater:

Open the Repeater tab you want to use.

[Optional] Highlight part of the request or response to focus Burp AI's attention.

Click Burp AI. Burp displays a prompt dialog.

Enter your question or instruction. For more information on writing effective prompts for Burp AI, see Writing effective prompts for Burp AI.

[Optional] Use the lozenges to select any additional context you want to include with your prompt (for example a highlighted area, full request, full response, or notes).

Click the arrow to start the exploration. Burp adds the task to the Dashboard > Tasks panel.

Burp displays a notification when the task starts. Click View task to open the task in the Tasks panel. Completed tasks are saved to your project file.

You can run a Burp AI task on any Repeater tab that has a specified target. For more information on configuring targets, see Working with HTTP messages in Burp Repeater.

Note

Burp AI doesn't retain conversation history. Include all necessary context in each prompt.

Managing context

You can choose which information Burp AI uses as context when you run a task. Including the relevant context improves both response quality and credit efficiency.

By default, Burp AI includes the full request and response as context.

Adding highlighted areas

If you highlight part of a request or response, such as a parameter or header, you can use the lozenges in the prompt dialog to add it as specific context. This focuses Burp AI's analysis on that section.

Adding notes

You can include any notes you added to the current Repeater tab by clicking + and selecting Notes. Burp adds the entire contents of the Notes panel as context.

For more information on adding notes in Repeater, see Adding notes for HTTP Repeater tabs.

Removing items

To remove a context item, click the x button on its lozenge in the prompt dialog.

To add the item again, click + and select the item from the menu.

Reviewing task results

To view an AI task:

Go to Dashboard > Tasks.

Select the task to view its details.

Each AI task contains two tabs:

Task progress - shows a step-by-step log of Burp AI's actions.

Logger - records all HTTP traffic generated during the task.

Task progress

The Task progress tab shows the actions Burp AI performs during a task as a series of steps. You can review every step and reproduce any action manually if needed.

Some steps have additional options available, depending on the tool Burp AI used at that point.

Steps using Repeater

For Repeater steps, you can:

View the request and response for that action.

Click Expand to inspect the request and response in the message editor.

From the expanded view, click Send to Repeater to open the request in a new Repeater tab. This enables you to verify Burp AI's analysis and perform further manual testing.

Steps using Intruder

For Intruder steps, you can:

View the results table showing payloads, status codes, content types, and response lengths.

Inspect the request for each result.

Click Send to Intruder to open the step in a new Intruder tab. This enables you to continue an AI-generated attack sequence using Intruder.

Logger

The Logger tab shows a complete record of all HTTP requests and responses generated during the task.

Ending a task

To end a Burp AI task manually, select it and click Finish task. Tasks also end automatically if Burp AI determines it can't progress further.

Trust and transparency in Burp AI

Burp AI in Repeater is designed to be transparent, reproducible, and always under your control.

Step-by-step visibility: Every action Burp AI takes is logged in the Task progress tab.

Manual verification: You can send any AI-generated request to Repeater or Intruder for independent testing.

User control: Tasks only run when you start them. You can pause or stop them at any time.

Data security: All data is processed within PortSwigger's secure AI infrastructure. Requests are handled in real time, and providers don't retain them.

Note

For more details on AI security and data handling across all of Burp AI's features, see Burp AI trust and compliance FAQ.

Related topics

Writing effective prompts for Burp AI

AI credits

Troubleshooting Burp AI connectivity
