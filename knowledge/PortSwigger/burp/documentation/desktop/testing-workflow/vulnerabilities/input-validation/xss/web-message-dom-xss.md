# Testing for web message DOM XSS with DOM Invader

Source: https://portswigger.net/burp/documentation/desktop/testing-workflow/vulnerabilities/input-validation/xss/web-message-dom-xss
Fetched: 2026-06-28T09:16:00.202234+00:00

Support Center

Documentation

Desktop editions

Testing workflow

Testing for vulnerabilities

Testing input validation

Cross-site scripting

Testing for web message DOM XSS with DOM Invader

ProfessionalCommunity Edition

Testing for web message DOM XSS with DOM Invader

Last updated:

June 18, 2026

Read time:

2 Minutes

Web message DOM XSS occurs if the destination origin for a web message trusts the sender not to transmit malicious data in the message, and handles the data in an unsafe way by passing it into a sink.

You can use DOM Invader to test applications for web message DOM XSS. DOM Invader enables you to log any messages that are sent via the postMessage() method, and modify and resend web messages.

To learn more about sources and sinks, see DOM-based vulnerabilities.

Note

DOM Invader is pre-installed in Burp's browser. It's disabled by default as some of its features may interfere with your other testing activities.

Before you start

Enable DOM Invader. For more information, see Enabling DOM Invader.

Enable Postmessage interception from the DOM Invader settings menu. For more information, see Main DOM Invader settings.

Steps

You can follow the processes below using the lab DOM XSS using web messages.

Use Burp's browser to visit your target website.

Right-click the browser window and select Inspect.

Select the DOM Invader tab and then select Messages from the right-hand panel. You can see the messages that DOM invader has flagged as exploitable.

Click each message to review it, and see if the origin, data, or source properties of the message are accessed by the client-side JavaScript:

If the origin property isn't accessed, it's likely that the origin isn't being validated.

If the data property isn't accessed, the message can't be exploited.

If the source property isn't accessed, it's likely the source (usually an iframe) isn't being validated.

You can use the message information to craft an exploit. Use DOM Invader to send a modified web message:

From the Messages view, click on any message to open the message details dialog.

Review the message information to identify the type of sink the data ends up in.

Edit the Data field with an exploit that matches the sink type.

Click Send.

If you find an exploitable vulnerability, use DOM Invader to generate a proof of concept:

Select the vulnerable message to open the message details dialog.

Modify the values as required for your exploit.

Click Build PoC to save the HTML to your clipboard.

Related pages

Testing for DOM XSS using web messages

DOM Invader
