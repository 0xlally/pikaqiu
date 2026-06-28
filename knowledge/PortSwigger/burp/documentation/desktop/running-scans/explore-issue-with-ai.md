# Exploring issues with AI

Source: https://portswigger.net/burp/documentation/desktop/running-scans/explore-issue-with-ai
Fetched: 2026-06-28T09:15:52.431439+00:00

Support Center

Documentation

Desktop editions

Running scans

Exploring issues with AI

Professional

Exploring issues with AI

Last updated:

June 18, 2026

Read time:

3 Minutes

Explore Issue is an AI-powered pentesting assistant that performs automated follow-up investigations on vulnerabilities identified by Burp Scanner. It helps you to efficiently validate issues, generate proof-of-concept (PoC) exploits, and uncover additional attack vectors, freeing you up to focus on more complex analysis work.

How Explore Issue works

When attempting to explore an issue, Burp analyzes the context of the vulnerability and determines the best strategy to explore it.

The AI can:

Select appropriate Burp tools to use.

Structure and send requests to test different exploitation techniques.

Handle responses dynamically, adjusting its approach based on the target system's behavior.

Generate and validate PoC exploits to demonstrate real-world impact.

Identify additional attack vectors beyond Burp Scanner's initial findings, including privilege escalation paths or data exposure risks.

Note

Burp's AI-powered features require AI credits. If your credits run out while exploring an issue, the task pauses until you top up. For details, see AI Credits.

Running an explore task

You can only explore issues that Burp Scanner has previously identified. For more information on running scans in Burp Suite, see Running scans.

To run an AI-powered explore task:

Select a scan or live audit task.

Go to the Issues tab and select the issue you want to explore.

From the Advisory tab, click Explore issue. Burp starts to explore the issue and adds a card to the Tasks list on the Dashboard.

Click the task card and select the Task progress tab. Burp displays the results of the task as a series of steps.

Once the AI determines that the task is complete, Burp displays a task summary outlining key findings, impact, and potential next steps.

Tip

To pause the task, click the pause icon on the task card.

Completed explore tasks are saved to your project file.

Reviewing results

To view the results of an explore task:

Go to the Dashboard.

Select the task from the Tasks list.

Each explore task contains two tabs:

Task progress

Logger

Task progress

This tab provides a step-by-step log of how Burp attempted to exploit the vulnerability. It logs every action taken, enabling you to review and reproduce the AI's methodology.

Depending on the tools the AI used in a particular step, different options are available:

Repeater: If the AI used Repeater in the step, click Expand to view the relevant HTTP messages in the message editor and Inspector. From here, you can also click Send to Repeater to open these messages in a new Repeater tab.

Intruder: If the AI used Intruder in the step, click Send to Intruder to open a new Intruder tab containing the step's HTTP messages.

To navigate between steps, select them in the left-hand panel. You can also use the search bar.

Once the AI determines that the task is complete, it generates an executive summary that consolidates key findings, making it easy to review task results. Burp displays this information in the Task summary panel at the top of the tab.

Logger

The Logger tab contains a comprehensive record of all HTTP requests and responses generated during the task.

Ending an explore task

To manually end an explore task, select the task and click Finish task. Explore tasks end automatically if the AI determines that it cannot progress any further.

Trust and transparency in Explore Issue

Explore Issue is designed to be fully transparent and reproducible, ensuring you can trust the AI's findings and validate them manually.

Every AI-driven action in Explore Issue is governed by these core principles:

Step-by-step visibility - Every action the AI takes is logged in the Task Progress tab, so you can review its methodology in detail.

Manual verification - If you want to further investigate a step, you can send AI-generated requests to Repeater or Intruder for manual testing.

Data security - All of Burp's AI features process data within PortSwigger's secure trust boundary. Requests are handled in real time, and our AI providers do not store them.

User control - Explore Issue does not run unless you activate it. You can pause or end an Explore Issue task at any time.

Note

For more details on AI security and data handling, see Burp AI trust and compliance FAQ.
