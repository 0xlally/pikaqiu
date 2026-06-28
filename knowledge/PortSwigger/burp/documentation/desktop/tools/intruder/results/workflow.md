# Burp Intruder workflow tools

Source: https://portswigger.net/burp/documentation/desktop/tools/intruder/results/workflow
Fetched: 2026-06-28T09:16:05.122680+00:00

Support Center

Documentation

Desktop editions

Tools

Intruder

Results

Workflow

ProfessionalCommunity Edition

Burp Intruder workflow tools

Last updated:

June 18, 2026

Read time:

3 Minutes

You can carry out actions on the attack results as part of your workflow. Right-click on any item in the results table to access the actions in the context menu.

Add payload position

Add payload markers on either side of the selected text, to set a single payload position.

Clear payload positions

Remove all payload positions. If you've selected some text, markers are removed from within the selected area only.

Scan

Professional Send selected items to Burp's scanner, to scan for content or vulnerabilities.

Send to...

Send selected items to other Burp tools. This enables you to perform further analysis and use Burp to drive your workflow. For example, you can send HTTP messages that you want to store for later investigation to Burp Organizer.

Show response in browser

Generate a unique URL for the response. Copy this and paste it into Burp's browser to render the response without the limitations of Burp's built-in HTML renderer.

Burp serves the resulting browser request with the exact response that you select: the request is not forwarded to the original web server. Burp's browser processes the response in the context of the originally requested URL. This means that relative links within the response are handled properly.

When Burp's browser renders the response it may make additional requests, for example for images or CSS. These are handled by Burp in the usual way.

Record an issue

Professional Manually record an issue for the selected request / response pair:

Create an issue - Add a new issue.

Add to manually created issue - Add a request / response pair to a pre-existing manually created issue.

The issue is saved to your project and can be included when you generate a report.

For more information, see Manually creating issues for reports.

Request in browser

Resend requests in Burp's browser:

In original session - Resend the request using the cookie header that appeared in the original request.

In current session - Resend the request using the cookies supplied by the browser.

Generate CSRF PoC

Create HTML which causes the selected request to be issued when viewed in a browser. For more information, see Generate CSRF PoC.

Add to site map

Add the selected items to the Target site map. This is useful when you identify new resources on the server which have not been added to the site map.

Request item again

Queue the selected items to be requested again by the attack engine. When the items are re-requested, the table entry for the items, and associated HTTP messages, are updated based on the new request. This is useful when:

Attack requests have failed due to network errors, or received an anomalous server response due to some intermittent problem.

You have modified the base request or other relevant configuration during the attack, and want to re-request items that were based on the original configuration.

Define extract grep from response

Open the response extraction rule dialog, and create a new extract grep item from the response. This enables you to extract the interesting part of the response. This is useful when an attack request generates a different type of response than the base request, as it enables you to quickly review the contents of similar responses. For example:

A particular format of error message when fuzzing. For more information, see Fuzzing for vulnerabilities.

A different login message when guessing credentials. For more information, see Enumerating identifiers.

Copy as curl command

This copies a curl command to the clipboard, that can be used to generate the current request.

Add comment

Add a comment to the selected items.

Highlight

Apply a highlight to the selected items.

Copy links

Parse the selected items for links, and copy these to the clipboard.

Save item

Save the details of selected items in XML format. This includes full requests and responses, and all relevant metadata such as response length, HTTP status code, and MIME type.
