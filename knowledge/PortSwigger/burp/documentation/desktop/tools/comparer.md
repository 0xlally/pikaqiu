# Burp Comparer

Source: https://portswigger.net/burp/documentation/desktop/tools/comparer
Fetched: 2026-06-28T09:16:02.206107+00:00

Support Center

Documentation

Desktop editions

Tools

Comparer

ProfessionalCommunity Edition

Burp Comparer

Last updated:

June 18, 2026

Read time:

2 Minutes

Burp Comparer enables you to compare any two items of data. You can use Comparer to quickly and easily identify subtle differences between requests or responses. For example:

To compare responses to failed logins that use valid and invalid usernames, for username

enumeration.

To compare large responses with different lengths that you have identified in an Intruder attack.

To compare similar requests that give rise to different application behavior.

To compare responses when testing for blind SQL injection bugs using Boolean condition injection, to see whether injecting different conditions results in a relevant difference in responses.

Carrying out comparisons

To carry out a comparison using Burp Comparer:

Locate the messages that you want to analyze within Burp Suite.

Right-click each message and select Send to Comparer. You can send a message from anywhere in Burp.

Go to the Comparer tab. The messages are listed in the two item tables.

Select the two messages you want to compare.

Select Words or Bytes to compare the messages. A new window opens with the results.

Note

The two item tables each display a list of all the messages that you have sent to Comparer. You need to select an item from each table.

To sort the contents of the table, click on any table header.

Controls

The Comparer tab contains the following controls:

Paste - Add an item from the clipboard.

Load - Add an item from a file.

Remove - Delete the highlighted item.

Clear - Delete all items in the list.

There are two analysis options available:

Words - Make a word comparison. This tokenizes each item of data based on whitespace delimiters, and identifies the token-level edits required to transform the first item into the second.

Bytes - Make a byte comparison. This identifies the byte-level edits required to transform the first item into the second.

Note

The byte-level comparison requires significantly more computing power. You should normally only use this option when a word-level comparison doesn't identify the relevant differences.

Results

The comparison results open in a new window, which displays the compared items in two panels. The items are color-coded to indicate each modification, deletion, and addition required to transform the first item into the second. Any text that isn't highlighted is found in both items.

The results window also contains a title bar that indicates the total number of differences between the items.

There are various controls in the results window that help you to analyze the results:

Sync views - Select this setting to scroll the two panels simultaneously.

Text - View both items in text form.

Hex - View both items in hex form.

Related pages

Burp Suite also enables you to compare two site maps. This function is found in the Target > Site

map tab. For more information, see Comparing site maps.
