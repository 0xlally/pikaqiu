# Professional 1.2.14

Source: https://portswigger.net/burp/releases/professional-1-2-14
Fetched: 2026-06-28T09:16:22.982448+00:00

Adds AMF support to all tools except for Burp Intruder. Anywhere you see an HTTP request or response with an AMF-encoded body, Burp will display a tab containing a tree view of the decoded message:

If the message is editable, you can double-click individual nodes in the tree to modify their values, and Burp will reserialise the message with your new data. Burp supports all primitive data types, and also the array and hashmap data structures.

Burp Scanner is also updated to automatically place attack payloads within string-based AMF values.
