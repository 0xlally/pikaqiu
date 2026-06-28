# Burp Intruder payload processing

Source: https://portswigger.net/burp/documentation/desktop/tools/intruder/configure-attack/processing
Fetched: 2026-06-28T09:16:04.572638+00:00

Support Center

Documentation

Desktop editions

Tools

Intruder

Configure attack

Processing

ProfessionalCommunity Edition

Burp Intruder payload processing

Last updated:

June 18, 2026

Read time:

3 Minutes

You can configure payload processing rules so that Burp Intruder modifies payloads before it inserts them into the request. This is useful for a variety of purposes, such as when you need to:

Generate unusual payloads.

Wrap payloads up within a wider structure or encoding scheme prior to use.

Apply a sequence of encodings to each payload in a predefined wordlist.

Configuring processing rules

You can define rules to perform various processing tasks on each payload before it is used:

Go to Intruder. In the Payloads side panel, scroll down to the Payload Processing field.

Click Add. A window opens with a drop-down list of processing rules.

Select a rule type from the list. Fill in any further requirements to configure the rule.

Processing rules are executed in sequence. Modify the sequence using the Up and Down buttons. You can also toggle each rule on and off, this can help you debug any problems with the configuration.

Types of processing rules

The following types of processing rules are available:

Add prefix - Add a literal prefix before the payload.

Add suffix - Add a literal suffix after the payload.

Match / replace - Replace any parts of the payload that match a specific regular expression with a literal string.

Substring - Extract a sub-portion of the payloads, starting from a specified offset (0-indexed) and up to a specified length.

Reverse substring - This functions as for the substring rule, but the end offset is specified counting backwards from the end of the payload, and the length is counted backwards from the end offset.

Modify case - Modify the case of the payload, if applicable. The same settings are available as for the case modification payload type.

Encode - Encode the payload using various schemes: URL, HTML, Base64, ASCII hex or constructed strings for various platforms.

Decode - Decode the payload using various schemes: URL, HTML, Base64 or ASCII hex.

Hash - Carry out a hashing operation on the payload.

Add raw payload - Add the raw payload value before or after the current processed value. It is useful, for example, if you need to submit the same payload in both raw and hashed form.

Skip if matches regex - Skip the payload if the current processed value matches a specified regular expression. This is useful, for example, if you know that a parameter value must have a minimum length and want to skip any values in a list that are shorter than this length.

Invoke Burp extension - Invoke a Burp extension to process the payloads. The extension must have registered an Intruder payload processor. You can select the required processor from the list of available processors that have been registered by currently loaded extensions.

Replace placeholder with base value - Replace any parts of the payload that match {base} with the base value of the payload position.

Replace placeholder with collaborator payload - Replace any parts of the payload that match a specific regular expression with a Collaborator payload. You can choose whether to include the Collaborator server location in the Collaborator payload.

Configuring payload encoding

You can URL-encode selected characters for safe transmission within HTTP requests. As this setting is applied after payload processing rules have executed, you should use it for final URL-encoding. This enables you to apply encoding after the payload grep setting has checked for echoed payloads.

To configure final URL-encoding:

Go to Intruder. In the Payloads side panel, scroll down to the Payload encoding field.

Select URL-encode these characters.

Enter the characters you want to encode.

Related pages

For more information on the payload grep setting, see Burp Intruder attack settings.
