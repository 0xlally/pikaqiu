# Predefined payload lists

Source: https://portswigger.net/burp/documentation/desktop/tools/intruder/configure-attack/payload-lists
Fetched: 2026-06-28T09:16:03.978225+00:00

Support Center

Documentation

Desktop editions

Tools

Intruder

Configure attack

Payload lists

Professional

Predefined payload lists

Last updated:

June 18, 2026

Read time:

2 Minutes

Burp Intruder includes a range of built-in payload lists. You can use these to quickly and easily generate payloads for various attacks.

Using predefined payload lists

You can use a predefined payload list with any payload type that uses a list of strings:

Go to Intruder. In the Payloads side panel, select an appropriate option from the Payload type drop-down menu.

Click Add from list... in the Payload configuration field.

Select a list from the drop-down menu. The list displays in the Payload configuration field.

If the list includes placeholders, set up a rule to process them under Payload processing.

Note

You can load your own directory of custom payload lists. Do this in Burp's Settings dialog. To open the dialog, click on Settings in the top toolbar. For more information, see

Intruder settings.

Placeholders

Some of the predefined payload lists include placeholders that you can replace with your own values:

Predefined payload list

Placeholders used in the list

CGI Scripts

{file}, {domain}

Fuzzing - full

{base},

{domain},

foo@{domain}

Fuzzing - JSON_XML injection

{base}

Fuzzing - out of band

{domain}

Fuzzing - path traversal (single file)

{file}

Fuzzing - path traversal

{base}

Fuzzing - quick

{base}

Processing placeholders

Before you run an attack with one of the payload lists above, you need to replace placeholders with actual values. The table below details how each of the placeholders can be used:

Placeholder

Use

Example placeholder replacement

{file}

Specify a filename.

/etc/passwd

{base}

Replaces {base} with value marked as payload.

1337

{domain}

Specify a web domain.

COLLAB_ID.oastify.com

foo@{domain}

Specify a web domain as part of an email address.

example.com

Processing a placeholder in your attack

To add a placeholder to your attack, set up a processing rule:

Go to Intruder. In the Payloads side panel, scroll down to the Payload processing field.

Click Add. A window opens with a drop-down list of processing rules.

Select Match/replace.

In the Match regex field, type in the placeholder used in the payload. For example, \{file\} or \{domain\}.

In the Replace with field, type the item you want to replace the placeholder with. For example, application.exe instead of \{file\}, or portswigger.net instead of \{domain\}.
