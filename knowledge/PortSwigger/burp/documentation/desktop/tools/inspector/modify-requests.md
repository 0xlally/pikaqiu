# Modifying requests using the Inspector

Source: https://portswigger.net/burp/documentation/desktop/tools/inspector/modify-requests
Fetched: 2026-06-28T09:16:03.868978+00:00

Support Center

Documentation

Desktop editions

Tools

Inspector

Modifying requests

ProfessionalCommunity Edition

Modifying requests using the Inspector

Last updated:

June 18, 2026

Read time:

2 Minutes

The Inspector has several features to make it easier to modify requests and perform basic operations, such as reordering headers:

Adding new items to a request

To add a new item, such as an HTTP header:

Expand the relevant category in the Inspector panel.

Click the Add button at the bottom of the list.

Enter a name and value and click Add.

The message editor updates to contain the new item.

Removing items from a request

To remove an item from the request, select the item and click the trash icon at the bottom of the list.

You can remove multiple items at the same time. To select multiple items, click and drag the mouse.

Reordering items in a request

To quickly reorder items in a request, select the item and use the arrow buttons at the bottom of the list.

Editing the name or value of an item

To edit the name or value of an item, double-click the entry in the main Inspector panel.

If the data that you edited was automatically decoded by the Inspector, the same sequence of encodings are applied to your changes before they are injected into the request. This saves time when you work with encoded data.

Note

If you want to see the sequence of decoding steps that are being applied to your input, click the arrow to the right of the item.

Injecting newlines

You can inject newlines from the detailed view of the Inspector:

Click the arrow to the right of the item that you want to edit.

Select the location in the Name or Value field where you want to inject the characters.

Press Shift + Return. The carriage return and line feed characters are injected into the entry field, represented by the \r\n icons.

This is essential for exploiting a number of HTTP/2-exclusive vulnerabilities that were discovered by James Kettle. For more details, see his whitepaper on our research page.

PortSwigger Research

HTTP/2: The Sequel Is Always Worse

Injecting other non-printing characters

To inject any non-printing character in the Inspector:

Add a random placeholder character in the appropriate location.

Select the placeholder.

Use the Inspector's Selection widget to change its code point. For example, set the code point to 00 to replace the character with a null byte.

To inject non-printing characters without the need to add a placeholder, switch to the message editor's Hex tab.

Copying items from the Inspector

You can copy one or more items from the Inspector panel to paste them elsewhere, such as into another request. You can also copy just the name or value of an item: select the item and choose Copy name or Copy value from the context menu.

If you copy encoded data, the original encoded value is copied to your clipboard rather than the decoded version that you see in the Inspector.

Related pages

Getting started with the Inspector.
