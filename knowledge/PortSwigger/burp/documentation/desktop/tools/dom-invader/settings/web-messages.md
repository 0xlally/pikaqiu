# Web message settings

Source: https://portswigger.net/burp/documentation/desktop/tools/dom-invader/settings/web-messages
Fetched: 2026-06-28T09:16:03.211142+00:00

Support Center

Documentation

Desktop editions

Tools

DOM Invader

Settings

Web message settings

ProfessionalCommunity Edition

Web message settings

Last updated:

June 18, 2026

Read time:

2 Minutes

You can click the cog icon next to the Postmessage interception option to access further settings for fine-tuning DOM Invader's behavior when handling web messages.

Postmessage origin spoofing

When this setting is enabled, DOM Invader automatically replaces the origin of any messages with a fake origin that both starts and ends with the domain name of the true origin. By doing so, DOM Invader can automatically identify event handlers that rely on flawed logic or regular expressions to validate the origin of messages.

For example, some websites use the startsWith() or endsWith() methods to verify the domain name in the origin. This kind of validation can be easily bypassed using these techniques.

Note

If this setting is disabled, you can still spoof the origin of individual requests by selecting the Spoof origin checkbox when replaying the message. Alternatively, you can manually modify the origin using the provided field.

Canary injection into intercepted messages

When this setting is enabled, DOM Invader automatically injects the canary into the data property of any messages that are sent on the page. DOM Invader determines whether the expected data is a JSON string, JSON object, or plain string, then injects the canary using the correct format.

When viewing the message details, you can use the Show drop-down to toggle between the original data that was sent by the page, and the one containing the automated injection.

Filter messages with duplicate values

When this setting is enabled, DOM Invader groups identical messages together to reduce noise. In some cases, you might want to disable this setting so that you can see every single message. For example, you might want to see individual messages to make sure that they are being sent.

Generate automated messages

When this setting is enabled, DOM Invader generates and sends its own messages to any message event listeners that it identifies on the page. This is useful in cases where you want to test a potentially vulnerable event handler but are unable to trigger a message event by interacting with the page as normal.

DOM Invader attempts to infer information about the structure of the data that each event handler is expecting. It then uses this information to generate and send a suitable message.

Based on how the listener handles each message, DOM Invader is able to generate follow-up messages that are tailored to hit additional code paths, which can potentially lead to more dangerous sinks.

Note

You can tell which messages DOM Invader generated because they do not have a numeric ID on the Messages view.

Detect cross-domain leaks

When this setting is enabled, DOM Invader reports when the current page sends a web message containing data from the URL to a different origin. In this case, an attacker can potentially steal sensitive data such as OAuth tokens by embedding the affected page in an iframe, along with an event listener that extracts the data.
