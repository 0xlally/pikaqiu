# Match and replace rules

Source: https://portswigger.net/burp/documentation/desktop/tools/proxy/match-and-replace
Fetched: 2026-06-28T09:16:07.022181+00:00

Support Center

Documentation

Desktop editions

Tools

Burp Proxy

Match and replace

ProfessionalCommunity Edition

Match and replace rules

Last updated:

June 18, 2026

Read time:

2 Minutes

Match and replace rules enable you to automatically replace parts of HTTP and WebSocket messages as they pass through the proxy. You can configure and enable these in the Proxy > Match and replace tab. They can used for a variety of tasks, such as adjusting headers, rewriting content, or modifying authentication tokens automatically in real-time.

Match and replace rules are listed in the HTTP match and replace rules and WebSocket match and replace rules tables. Burp executes enabled match and replace rules in turn for each message, making any applicable replacements. To change the order in which rules are applied, reorder them using the Up and Down buttons.

To only apply match and replace rules to items that are in the project scope, select Only apply to in-scope items. For more information on how to set a scope for your work, see

Scope settings - Target scope.

Adding match and replace rules

You can configure match and replace rules in two different ways:

Settings mode - Configure match and replace rules using checkboxes and drop-downs. You can use this to create rules for both HTTP and WebSocket messages. For more information, see Creating match and replace rules.

Professional Script mode - Create powerful match and replace rules using Burp's Java-based scripts. You can use this to create rules for HTTP messages. For more information, see Creating HTTP match and replace rules with scripts.

When adding or editing a HTTP match and replace rule, you can test your rule using the built-in test function. For more information, see

Testing HTTP match and replace rules.
