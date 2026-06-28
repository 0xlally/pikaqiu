# Creating match and replace rules

Source: https://portswigger.net/burp/documentation/desktop/tools/proxy/match-and-replace/creating
Fetched: 2026-06-28T09:16:06.893532+00:00

Support Center

Documentation

Desktop editions

Tools

Burp Proxy

Match and replace

Creating rules

ProfessionalCommunity Edition

Creating match and replace rules

Last updated:

June 18, 2026

Read time:

3 Minutes

You can configure match and replace rules to automatically replace parts of messages as they pass through the proxy. To create a rule, go to the Proxy > Match and replace tab and click Add. The

Add match/replace rule window opens, which has two modes:

Settings mode - Configure match and replace rules using checkboxes and drop-downs. You can use this to create rules for both HTTP and WebSocket messages.

Script mode - Create powerful match and replace rules using Java-based scripts. You can use this to create rules for HTTP messages.

Settings mode

On the Settings mode tab, you can add match and replace rules using the configuration options. Each match and replace rule specifies a literal string or regex pattern to match, and a string to replace it with.

You can use this to create rules for both HTTP and WebSocket messages.

To add a new rule using Settings mode:

In Proxy > Match and replace, click Add to open the Add match/replace rule dialog.

In the Add match/replace rule dialog, click the Settings mode tab.

Specify the details of the match/replace rule:

Type - For HTTP requests, specify the type of rule you want to define. For example, Request header or Response body.

Direction - For WebSocket messages, specify the direction of the message you want the rule to apply to. Choose from Client to server, Server to client, or Both directions.

Match - The string or regex pattern you want the rule to match. If you leave this blank for an HTTP rule with the Request header or Response header type, the replacement string is added as a new header.

Replace - The string you want the rule to replace. If you leave this blank for an HTTP rule with the Request header or Response header type, then any header that matches is removed.

Comment - An optional description of the rule.

If you want Burp to treat the match parameter as a regex, select Regex match. For more information, see Using regex syntax.

For HTTP messages, you can test the rule using the built-in test function. For more information, see Testing

HTTP match and replace rules.

Click OK.

The new rule is added to the table and automatically enabled for the current project.

Using regex syntax

You can use a regex pattern to match the text you want to replace. This enables you to match a variety of text inputs that follow a specific format, such as email addresses or IP addresses. It also enables you to match the underlying structure for content that changes dynamically.

Matching multi-line regions

You can use regex syntax to match multi-line regions of a message body. For example, if a response body contains only:

Now is the time for all good men

to come to the aid of the party

then using the regex:

Now.*the

will match:

Now is the time for all good men

to come to the aid of the

If you want to match only within a single line, you can modify the regex to:

Now[^\n]*the

which will match:

Now is the

Using regex groups in back-references and replacement strings

In a Match expression you can:

Define groups using parentheses. Burp assigns groups a 1-indexed reference number in order from left to right (with group 0 representing the entire match).

Back-reference groups. Use a backslash followed by the group's index.

For example, to match a pair of opening and closing tags with no other tags between, you could use the regex:

<([^/]\w*)[^>]*>[^>]*?</\1[^>]*>

You can reference groups in the replacement string by using a $ followed by the group index. For example, the following replacement string would include the name of the tag that matched the above regex:

Replaced: $1

Script mode

Script mode enables you to apply Java-based scripts to define powerful HTTP match and replace rules. For more information, see Creating HTTP match and replace rules using scripts.
