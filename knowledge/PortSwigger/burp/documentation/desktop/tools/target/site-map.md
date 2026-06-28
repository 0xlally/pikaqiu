# Site map

Source: https://portswigger.net/burp/documentation/desktop/tools/target/site-map
Fetched: 2026-06-28T09:16:09.184728+00:00

Support Center

Documentation

Desktop editions

Tools

Target

Site map

ProfessionalCommunity Edition

Site map

Last updated:

June 18, 2026

Read time:

5 Minutes

The site map shows the information that Burp collects as you explore your target application. You can toggle between the URL view, and Crawl paths view. The URL view creates a hierarchical representation of the information, organizing it alphabetically by root domain then by subdomain. Content comes from various sources, including scan results and the URLs you discover as you browse the target manually. You can also see:

A list of the contents.

Full requests and responses for individual items.

Full information about any security issues that Burp discovers.

You can filter and annotate this information to help you to manage it. You can use the site map to send content to Burp's other tools, and to drive your testing workflow.

Accessing the site map

You can access the site map in two locations:

To view a combined map containing information from all regular, non-isolated scans in the current project, go to Target > Site map. Any new non-isolated scans that you run add to the information displayed in this tab.

To view the site map information found by an isolated scan, go to the Dashboard and select the scan from the Tasks list. In the main panel, go to the Target > Site map tab. This tab doesn't include information from any other scans. It is only displayed for scans that have the Run isolated scan setting selected.

More information

For information on running isolated web application scans, see Running a full crawl and audit.

URL view

The URL view in the left-hand pane contains a hierarchical representation of content. The URLs are shown as:

Domains.

Directories.

Files.

Parameterized requests.

The URL view is organized alphabetically, first by root domain and then by subdomain.

Requests are shown with their HTTP method (for example, GET, PUT, or

OPTIONS). This enables you to easily distinguish between requests to the same endpoint with different methods.

You can expand interesting branches to see more details. If you select one or more parts of the URL view, you can see details about the items in the Contents and Issues panes. The panes also show items that are in child branches of your selection.

URL view icons

Professional When Live audit or Burp Scanner detect issues, they display colored circles on the relevant icons in the tree view. The color of the circle indicates the most significant security issue within each branch or item. Click on the icon to show the relevant issues in the Issues window. We use the same color circles on the URL view and the Issues window.

If the text next to an icon is black, the URL has been requested. If the text is grayed out, the URL has not yet been requested. You can edit the site map layout.

Contents pane

The Contents pane lists information for any items selected in the tree view:

All the resources directly requested via the Proxy.

Content that is likely to exist, based on Burp's analysis of responses to proxy requests.

Content that the Scanner or content discovery functions discover.

Any items that you manually add, from the output of other tools.

If an item is black, the URL has been requested. If the item is gray, the URL has not yet been requested. When you make requests, Burp uses any links to discover other content, which it shows in gray.

To help you to analyze the target application, you can use the site map filters and the target scope to hide content that you're not interested in.

You can also customize and sort the table, and copy column data to your clipboard. For more information, see Customizing Burp's tables.

Note

If you deselect passive crawling, the Contents pane doesn't show linked content or content that is only likely to exist.

Requests and responses

Select an item in the Contents pane to see the related Request and Response in the lower pane. You can use the Inspector to analyze the messages. Right-click a message if you want to send it to another of Burp's tools.

Burp includes a large number of functions to help you quickly analyze the messages further, drive Burp's core workflow, and carry out other useful tasks. For more information, see Burp Suite message editor.

Issues pane

The Issues pane shows any issues that Burp Scanner identifies, for items selected in the tree view. Select an issue to see more details in the tabs:

Advisory - View a description of the issue type and its remediation.

Request / Response - View the full requests and responses that are the basis for reporting the issue. Where applicable, the parts of the request and response that are relevant to the issue are highlighted.

If relevant, you can see details of any interactions with the Burp Collaborator server that were the basis for reporting the issue.

To quickly reproduce and verify an issue, right-click the message in the Contents pane and send the request to Burp Repeater. Alternatively, for GET requests, you can copy the URL and paste it into Burp's browser. Then you can reissue the request, and if necessary fine-tune the proof-of-concept attack that was generated by Burp.

Every issue that Burp Scanner reports is rated for severity (high, medium, low, informational) and confidence (certain, firm, tentative). If Burp uses a technique that is inherently less reliable (such as for blind SQL injection) to identify an issue, the confidence level reduces.

These ratings are indicative, you should review them based on your knowledge of the application's functionality and business context.

Editing the Issues pane

You can use the context menu to perform the following actions:

Report selected issues - Use Burp Scanner's reporting wizard, to generate a formal report of the selected issues.

Set severity - Change the severity level to high, medium, low, or informational. You can also flag the issue as a false positive.

Set confidence - Change the confidence level of the issue to certain, firm or tentative.

Delete selected issues - Delete the selected issues. If Burp rediscovers the issue (for example, if you rescan the same request), the issue is reported again. You can mark the issue as a false positive to avoid this. We recommend this tool if you want to remove hosts or paths you are not interested in. If you want to remove issues for hosts or paths you are still working on, use the false positive option.

Related pages

Getting started with the site map.

Workflow tools.

Filtering the site map.

Filtering the site map with scripts.

Comparing site maps.

Site map comparison results.

Editing the site map layout.
