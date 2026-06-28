# Professional / Community 2023.10.2.2

Source: https://portswigger.net/burp/releases/professional-community-2023-10-2-2
Fetched: 2026-06-28T09:16:40.240069+00:00

This release introduces new functionality for BChecks, including the ability to test your checks from within the editor and create definitions from a blank template. We have also added a notes feature to Repeater tabs.

For Burp Scanner, we have added new issue filters to the Issue Activity Dashboard panel and improved the quality of the text displayed on the Crawl paths tab.

Test BChecks in the editor

You can now test your BChecks from within the editor, enabling you to quickly confirm whether a check is working as expected without having to run a scan manually.

BCheck tests use pre-selected requests and responses as test cases. When you run a test, Burp Scanner runs the BCheck on the selected HTTP messages and reports the results.

For more information about the new BCheck test features, see Testing BChecks.

Make notes on Repeater tabs

You can now add notes to Repeater tabs. This feature enables you to record key information about a tab, making it easier to return to at a later time. If you subsequently send the item to Organizer, the new Organizer entry contains the existing note content.

To record a Repeater note, select the Notes panel in the tab sidebar and enter the required text.

Blank BCheck template

You can now start from a blank template when creating BChecks, rather than copying and modifying one of the default checks. We have added the new template to the BCheck templates list, which is displayed when creating a new BCheck.

Scanner improvements

We have made the following improvements to the Scanner:

The crawler can now access any available alt text for its target items. This has enabled us to improve the quality of the information displayed on the Crawl paths tab.

We have added three new filter buttons to the Issue Activity Dashboard panel:

BCheck generated filters the list to display only issues that were identified via a BCheck.

Extensions filters the list to display only issues that were identified via an extension-generated scan check.

Scan checks filters the list to display only issues that were found by a regular Burp scan check (i.e. not by a BCheck or extension).

Brotli and Deflate decoding support for the Montoya API

The Montoya API's decode method now supports Brotli and Deflate encodings.

Decoder improvements

When you pass a base64 string without padding to Decoder, it now decodes the string as if it were padded. This brings Decoder's behavior in line with that of the Inspector. Previously, Decoder required the appropriate padding to be added before the string was passed.

Bug fixes

We have fixed the following bugs:

Previously, the Send to Repeater context menu option was not sending WebSocket tabs to Repeater in certain circumstances. This function now works as expected.

We have fixed an issue with the BCheck validator whereby variables incorrectly defined outside of the define block were not causing the check to fail validation.

We have fixed some performance issues when viewing and searching large responses in the request/response viewer.

Browser upgrade

We have upgraded Burp's built-in browser to 118.0.5993.70 for Mac and Linux and 118.0.5993.70/.71 for Windows. This update contains security fixes.
