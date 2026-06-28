# Professional / Community 1.6.31

Source: https://portswigger.net/burp/releases/professional-community-1-6-31
Fetched: 2026-06-28T09:16:30.615094+00:00

This release enhances Burp Scanner to report issues based on deferred interactions with the Burp Collaborator server.

Asynchronous server-side injection vulnerabilities are normally invisible in an application's responses, and completely elude conventional scanning techniques. To detect invisible vulnerabilities, Burp Scanner uses payloads that cause the application to make some kind of network connection to the Collaborator server. When an interaction with the Collaborator server is observed, this demonstrates that the payload was successful and a vulnerability is present.

In this release, invisible vulnerabilities are reported even when the interaction occurs after Burp has finished scanning the relevant item. After scanning has completed, Burp continues polling the Collaborator server in the background, and retrospectively reports issues when deferred interactions occur. This cutting-edge capability allows Burp to report all kinds of serious issues that are otherwise impossible to detect, for example:

Blind second-order SQL injection, where a payload gets stored and later used in an unsafe SQL query, with no behavioral evidence in the application's responses.

OS command injection in an overnight batch job that passes stored user input into shell commands in an unsafe way.

Asynchronous back-end SOAP/XML injection where user input is stored and later embedded in an XML-based message in an unsafe way.

Each Burp session uses a unique identifier to track Collaborator interactions, and this can optionally be included in the Burp state file when saving your work. This means that you can later reload a state file containing completed scans, and observe any asynchronous Collaborator interactions that have occurred since you finished the original scanning. On reloading the state file, Burp will poll the Collaborator server and report issues based on any new interactions that have occurred for that Burp session.

Burp polls the Collaborator for asynchronous interactions every few minutes. When an asynchronous interaction is detected, Burp reports the issue without making any in-band requests to the target application. This means that you can safely revisit completed scans to pick up any asynchronous vulnerabilities even if the time window for testing is over. So imagine this: you finish testing on Friday without any decent issues; you load the Burp state file on Monday to start writing your report, and discover that one of your payloads has detected a command injection vulnerability in a shell script that runs over the weekend. Pretty cool?

[In fact, Burp began optionally saving Collaborator identifiers in state files starting with version 1.6.29. So if you have a state file from a test that was carried out with Burp 1.6.29 or later, you can reload it into the latest release to see if any deferred Collaborator interactions have occurred since you completed your testing.]

People are accustomed to seeing Burp report vulnerabilities during scanning, and not afterwards. To help users identify when deferred Collaborator interactions have occurred, a number of related useful features have been added:

The Scanner has a new "Issue activity" tab that contains a sequential record of when issues are created or updated. You can monitor this tab to view everything that is reported by the Scanner in time order, including detection of deferred Collaborator interactions.

When an issue is reported based on a deferred Collaborator interaction, the issue detail indicates the approximate elapsed time between the relevant scan completing and the interaction occurring.

The active scan queue has two new columns indicating the times that scanning started and ended for each item. This can help correlate the timings of Scanner activity and observed Collaborator interactions.

Note: The reporting of elapsed time between scan and interaction depends on some new capabilities in the Collaborator server. It is recommended that users who have deployed a private Collaborator server should upgrade to the latest Burp release, to gain the benefit of this feature.

In addition, some other updates have been made:

The BlazeDS library used for analyzing AMF messages has been updated to the latest version. This fixes some additional security vulnerabilities in BlazeDS's handling of malicious messages, which were found by the Burp research team. Since Burp version 1.6.29, Burp has disabled support for AMF messages by default, due to security concerns about the BlazeDS library. Any users who have enabled the option to support AMF messages should upgrade to the new release of Burp.

A problem comparing site maps from certain Burp state files has been fixed.

A problem installing some PKCS#11 certificates has been fixed.

All available command line arguments can now be listed by specifying the --help argument on the command line.
