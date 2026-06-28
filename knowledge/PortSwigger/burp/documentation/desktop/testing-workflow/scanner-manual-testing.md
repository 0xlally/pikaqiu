# Complementing your manual testing with Burp Scanner

Source: https://portswigger.net/burp/documentation/desktop/testing-workflow/scanner-manual-testing
Fetched: 2026-06-28T09:15:58.330411+00:00

Support Center

Documentation

Desktop editions

Testing workflow

Complementing manual testing with Burp Scanner

Professional

Complementing your manual testing with Burp Scanner

Last updated:

June 18, 2026

Read time:

3 Minutes

In addition to its automated testing capabilities, Burp Scanner can also be a powerful tool in your manual testing workflow, enabling you to investigate items or areas of interest without having to scan your entire application.

For example, you can use Scanner to perform targeted scans on specific requests, which you can then investigate further using Burp's manual testing tools.

To learn more about how you can use Burp Scanner to complement your manual testing, you can follow the tutorials below using our deliberately vulnerable website, ginandjuice.shop:

Scanning specific requests

Scanning user-defined insertion points

Scanning non-standard data structures

More information

To learn more about reviewing scan results, see Viewing scan results.

Scanning specific requests

Scanning a specific request is much faster than an application-wide scan, and often only takes seconds.

To scan a specific request:

In Burp Suite, go to Proxy > Intercept.

Click Open browser to open Burp's browser.

In Burp's browser, explore your target application.

In Burp, go to Proxy > HTTP history. Identify a request of interest, then right-click it and select one of the following scan methods:

Scan: Burp Scanner enables you to adjust the scan's configuration before it starts.

Do passive scan: Burp Scanner runs an audit-only scan of the unmodified request and the response it received.

Do active scan: Burp Scanner runs an audit-only scan of the target application using its default configuration. This involves sending modified requests containing payloads to probe for additional vulnerabilities.

The Dashboard tab flashes to indicate the scan has started. You can go to the Dashboard to review the progress and results of a scan.

Scanning user-defined insertion points

Burp Suite enables you to manually define insertion points and limit the audit phase of the scan to use only these insertion points. This means you can focus the scan on specific inputs that you want to test, reducing the number of requests required. Additionally, this lets you scan a request using inputs that Burp Scanner would normally ignore, such as custom header values.

Scanning a single insertion point

To scan a single user-defined insertion point:

In the message editor, highlight the part of the request you want to use as an insertion point.

Right-click the request, then select Scan selected insertion point.

Configure and launch your scan.

The Dashboard tab flashes to indicate the scan has started. To review the progress and results of your scan, go to the Dashboard.

Scanning multiple insertion points

You can also use Burp Intruder to define multiple insertion points in one request.

To scan multiple insertion points:

Send the relevant request to Intruder.

Go to Intruder.

In the message editor, highlight a substring you want to define as an insertion point and click Add §. Repeat this step for every insertion point you want to define.

Right-click the request, then select Scan defined insertion points.

To review the progress and results of your scan, go to the Dashboard.

If you define multiple insertion points, Burp scans each insertion point separately.

Scanning non-standard data structures

You might need to scan a specific part of a data format that Burp can't parse automatically. For example, you may want to scan:

A section of cleartext that's embedded in a cookie value.

Multiple data points that are separated by characters such as dashes or forward slashes.

You can highlight the content that you want to scan in the message window, then right-click and select Scan selected insertion point. For more information, see Scanning non-standard data structures.

Store HTTP traffic for review

Whether you've performed an application-wide scan or scanned a specific request, you can store requests and responses in Burp Organizer. For example, you might want to investigate a specific response at a later date without having to scan or browse through your target application again.

To do this, right-click a request or response, then select Send to Organizer.

To learn more about Burp Organizer, see Organizer.

Related pages

Burp Scanner

Viewing scan results

Burp Intruder

Lab: Discovering vulnerabilities quickly with targeted scanning

Lab: Scanning non-standard data structures
