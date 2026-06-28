# Professional 1.3.04

Source: https://portswigger.net/burp/releases/professional-1-3-04
Fetched: 2026-06-28T09:16:23.115190+00:00

This release adds a number of new features and bugfixes:

IBurpExtender now defines the following proxy interception actions:

public final static int ACTION_FOLLOW_RULES_AND_REHOOK = 0x10;

public final static int ACTION_DO_INTERCEPT_AND_REHOOK = 0x11;

public final static int ACTION_DONT_INTERCEPT_AND_REHOOK = 0x12;

If an implementation of processProxyMessage sets one of these values as the interception action, then Burp will make a second call to processProxyMessage after the user has viewed/edited the message. This enables extensions to perform further processing on the message. For example, to handle an unusual encoding scheme that is not supported by Burp, an extension could deserialise a custom message format in the first call to processProxyMessage, allow the user to manually review and modify the raw data, and then reserialise the message in the second call to processProxyMessage.

The Intruder payload processor adds a new type of processing rule to skip the current payload if it matches a regex expression. This enables you to use word lists with #commented lines, and skip these with a regex like:

^\s*#

The request timestamp which appears in various places (proxy history, site map, etc) now displays the date as well as the time, which is useful when your work spans several days.

In sortable tables, clicking on a column header to change the table ordering now preserves the selection of the selected item. This makes it easier to analyse certain sets of results - for example, in Intruder, you can select an interesting result, and quickly use column sorting to find other results that are similar to it in different respects (same payload, status code, response length, etc.) without having to hunt through the results for your item following each sort.

File extension filters in the proxy history, site map and active scanning wizard are now case insensitive, which is virtually always what you want.

The URL-decode function in the editor context menu now decodes Unicode URL-encoded data (for example, %u0041 decodes as A).

The help menu now has a link to the main Suite help as well as the help for individual tools.

The function to restore default settings now prompts for confirmation.

A bug in the proxy match-replace feature, in which Burp only replaced the first occurrence of a matched expression when operating on headers, has been fixed.

Some anomalies when copying attack configuration between Intruder tabs have been fixed.

The Intruder config for a request to retrieve cookies now uses the new request editor, eliminating some editing anomalies on some platforms.

Burp's XML output (used in Scanner reporting and exporting of request/response details) now uses XML version 1.1. It had been noted that some of Burp's output was not XML standards-compliant, as some binary content within raw HTTP messages contained characters which are disallowed in XML documents, even when they appear within CDATA blocks. Switching to version 1.1 reduces the extent of this problem, as the only disallowed character is NULL. When reported messages do contain NULL bytes, for purposes of accuracy Burp still preserves these in its output. A comment has been added within the output that it may be necessary for you to remove or replace NULL bytes before processing Burp's output using a standards-compliant parser.

A bug in the Proxy, in which Burp failed to properly handle non-proxy-style requests when running in invisible mode in conjunction with an upstream proxy server, has been fixed. Burp now correctly converts the URL in the request into its absolute form in this situation, so it can be processed by the upstream proxy.

A bug in Repeater, in which an edited but unrequested message is not preserved when saving state, has been fixed.
