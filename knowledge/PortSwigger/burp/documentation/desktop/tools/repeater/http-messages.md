# Working with HTTP messages in Burp Repeater

Source: https://portswigger.net/burp/documentation/desktop/tools/repeater/http-messages
Fetched: 2026-06-28T09:16:07.411921+00:00

Support Center

Documentation

Desktop editions

Tools

Repeater

Working with HTTP messages

ProfessionalCommunity Edition

Working with HTTP messages in Burp Repeater

Last updated:

June 18, 2026

Read time:

3 Minutes

You can use Burp Repeater to manipulate and resend individual HTTP requests, and analyze the application's responses. You can also add notes to each tab, to help you to manage your work.

To send HTTP requests with Burp Repeater:

Right-click on an HTTP request anywhere in Burp, and click Send to Repeater. A new tab is added to Repeater containing the request.

Go to Repeater and view the HTTP request details in the new tab.

Modify the message.

Click Send to send the request to the target server, and view the response details.

Repeat this process as many times as you like to see how modifying the request in different ways changes the server's response.

Professional During testing, you can run custom action scripts to extract, transform, and analyze HTTP request and response data. You can run custom actions on demand, or configure them to run automatically when sending a request. For more information, see

Custom actions.

Professional When you identify a vulnerability during testing you can manually create an issue to include in your report.

For more information, see Manually creating issues for reports.

Related pages

You can choose which protocol Burp will use to send the message. For more information, see Working with HTTP/2 in Burp Suite.

You can send a series of requests in sequence with a single click. For more information, see Sending HTTP requests in sequence.

HTTP Repeater tab

For HTTP messages, each Repeater tab contains the following items:

An HTTP message editor which contains the request to be sent. You can use the message editor functions to analyze and edit the message.

The target server to which the request will be sent. This is set automatically when you send a request to Repeater. To configure the target details, click :

If you've modified the host header, the Host and Port fields can be useful to see where your request is being sent.

If you want to manually set an SNI value, select Override SNI. This can be used to reproduce external service interaction issues detected by Burp Scanner using Burp Collaborator payloads within the SNI.

An HTTP message editor which shows the response that was received from the sent request.

The size of the response in bytes, and the response time in milliseconds.

Controls to navigate the request history:

Click the < and > buttons to navigate backwards and forwards through the history.

Use the drop-down buttons to show a numbered list of history items, and move quickly to them.

At any point in the history, you can edit and resend the currently displayed request.

Adding notes for HTTP Repeater tabs

If you find something interesting in a request or response, you can add notes to the Repeater tab. This can help you to improve your workflow when you have multiple tabs open.

To add a note to an HTTP Repeater tab:

In Repeater, select the tab that you want to add notes to.

Click Notes.

Type your notes into the Notes panel.

Note

If you added notes or highlights in another Burp tool, these are copied into Repeater. In addition, if you send a message from Repeater to another tool, your notes and highlights are copied across.

AI features in Repeater

Burp AI is built into Repeater, enabling you to run custom prompts against any tab. This flexible workflow gives you full control over what Burp AI examines, making it easy to tailor each task to your needs. For example, you can analyze a suspicious request, test for a specific vulnerability, or ask for suggestions on what to try next when you're unsure how to proceed.

Repeater also includes Explainer, a tool that provides instant AI-generated explanations for selected parts of a message. This is useful for quickly understanding headers, cookies, JavaScript, or other unfamiliar components without leaving your workflow.

More information

Using Burp AI in Repeater

Generating AI-powered explanations
