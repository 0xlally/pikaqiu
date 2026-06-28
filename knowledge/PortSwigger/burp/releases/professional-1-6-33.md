# Professional 1.6.33

Source: https://portswigger.net/burp/releases/professional-1-6-33
Fetched: 2026-06-28T09:16:27.894800+00:00

This release adds the ability to detect blind XSS, via Burp Collaborator.

Blind XSS is a special type of stored XSS in which the data retrieval point is not accessible by the attacker - for example, due to lack of privileges. This makes the vulnerability very difficult to test for using conventional techniques. In many cases, there is no hint whatsoever in the application's visible functionality that a vulnerability exists. Since security testers are in the habit of spraying target applications with alert(1) type payloads, countless admins have been hit by harmless alert boxes, indicating a juicy bug that the tester never finds out about. Due to the inherent difficulty in detecting blind XSS vulnerabilities, these bugs remain relatively prevalent, still waiting to be discovered. This new release of Burp empowers testers to easily find these critical vulnerabilities, with no special configuration or other tools required.

Previously, Burp Scanner has used purely in-band techniques to detect stored XSS. This involves first scanning the data entry point, later scanning the data retrieval point, identifying the connection between the two, and then supplying suitable payloads to the entry point to formulate a proof-of-concept attack. This approach can often be effective, but has some significant limitations:

It cannot detect blind XSS, because the data retrieval point is not accessible.

It requires that the entry and retrieval points are scanned in the correct order.

It is highly vulnerable to previously submitted data being overwritten by another user's actions in the time between scanning the entry and retrieval points.

Burp still uses conventional in-band techniques to detect stored XSS, but now also sends payloads like this:

This payload starts with a multi-context break-out sequence which, in all normal retrieval locations, will convert the HTML context to one where JavaScript can be executed. It then executes some script that triggers a connection to the Burp Collaborator server. This out-of-band interaction enables Burp to confirm when the payload has been successful. For more details on the breakdown of this payload, see our blog post on hunting asynchronous vulnerabilities.

The new approach to finding stored XSS has some significant benefits:

It can detect blind XSS, provided that another user, such as an administrator, eventually views a page containing the stored payload.

It only requires that the entry point be scanned by Burp. Other users' interaction with the application, or the Burp tester's own browser-based use of the application (if non-blind), is likely to lead to connections to the Collaborator server that enable Burp to report the issue.

Even where the stored data is short-lived, and has been overwritten by the time the Burp tester visits or scans the retrieval point, Burp may still detect the issue due to other users viewing the data.

As with other deferred Collaborator interactions, Burp can report stored XSS issues after the Burp user has finished testing, without any additional requests to the application.

Below is an example of what Burp's advisory looks like for a blind XSS issue that has been discovered via Burp Collaborator. This example uses a simpler payload that works in many situations. Note that Burp nicely identifies the Referer header from the incoming HTTP request to the Collaborator server, which will normally indicate the retrieval point where the payload appeared:
