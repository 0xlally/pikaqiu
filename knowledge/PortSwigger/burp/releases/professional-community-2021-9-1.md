# Professional / Community 2021.9.1

Source: https://portswigger.net/burp/releases/professional-community-2021-9-1
Fetched: 2026-06-28T09:16:36.299477+00:00

This release enables manual testing of hidden HTTP/2 attack surface and adds a number of improvements to Burp Intruder and Burp Scanner.

Manually test hidden HTTP/2 attack surface in Burp Repeater

You can now send HTTP/2 requests from Burp Repeater even if the server doesn't explicitly advertise HTTP/2 support via ALPN. This allows you to manually explore additional "hidden" HTTP/2 attack surface.

To enable this behavior, first select the Allow HTTP/2 ALPN override option from the Repeater menu, then switch the protocol to HTTP/2 from the Inspector panel.

Burp Intruder improvements

We have made the following improvements to Burp Intruder:

When configuring a list of payloads to send during your attack, you can now click the Deduplicate button to remove any duplicate entries. This helps to increase the efficiency of your attacks as you can avoid sending redundant, duplicate requests when combining multiple wordlists for example.

When using the Grep - Match or Grep - Payloads options, the results table now contains a column displaying the number of matches found in the response rather than just a checkbox.

In the resource pool configuration, there is now an option for setting the delay between requests to an incremental value. This enables you to study how the target application's behavior changes as requests become more spread out. You can use this to determine how long a session is kept alive between requests for example.

You can now select multiple rows and perform bulk operations on some of the tables in the Intruder configuration settings.

Improved scan check for server-side template injection

We have added payloads to the server-side template injection (SSTI) scan check to detect vulnerabilities in the following Java-based template engines:

SpEl

JSF

Freemarker

Thymeleaf

Velocity

JSTL

We have also integrated additional out-of-band detection methods using Burp Collaborator.

Audit asynchronous traffic in Burp Scanner

API calls that are triggered by the crawler interacting with elements on the page will now be sent for audit.

We have also improved the way the crawler interacts with forms on a page to better support modern single-page applications.

Improved handling of XML and JSON insertion points in Burp Scanner

We have made the following changes to improve the handling of XML and JSON insertion points during scans:

Payloads injected into unquoted JSON contexts are now automatically wrapped with quotation marks to ensure that Burp Scanner always generates valid JSON documents.

Insertion points in standard XML attributes such as xml:lang and xmlns:* are now ignored by default. If you prefer, you can override this setting in your scan configuration under Audit options > Ignored insertion points.

When appending payloads to insertion points within XML CDATA sections, Burp Scanner now removes the CDATA block and correctly entity-encodes the payloads.

Recorded login improvements

Burp Scanner can now handle iframes, multi-selects, scrolling elements, and SVG elements in recorded login sequences. We have also improved reliability of recorded logins by changing the way we locate and interact with elements on the page. For more details, please see our blog post on authenticated scanning improvements.

Other improvements

On the Logger tab, we have added an option to the context menu for exporting the log as a CSV file.

On the Dashboard tab, you can now rename tasks to help you identify them more easily. You can now also search for tasks by their name or other details.

You can now set a default preference for whether tasks are resumed or paused when you launch Burp. To change the default setting, go to User options > Misc > Tasks.

Security fix

We have updated Burp's embedded browser to Chromium version 95.0.4638.54, which fixes a number of high-severity bugs.

Bug Fixes

This release also provides a number of bug fixes, most notably for a bug when highlighting or selecting text in Burp Repeater.
