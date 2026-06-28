# Viewing insertion points

Source: https://portswigger.net/burp/documentation/desktop/running-scans/results/audit-items/insertion-points
Fetched: 2026-06-28T09:15:53.488554+00:00

Support Center

Documentation

Desktop editions

Running scans

Viewing scan and live task results

Audit items

Insertion points

Professional

Viewing insertion points

Last updated:

June 18, 2026

Read time:

5 Minutes

The Insertion points panel in the Audit items tab contains a list of all the insertion points for a request. This enables you to better understand how much attack surface Burp Scanner covers.

Related pages

To learn more about insertion points, see Auditing - Insertion points.

To view the Insertion points panel, click on a request. To hide the panel, click Insertion points. The panel is replaced by the base response.

Tree view

The Insertion points panel contains a tree view of the insertion points for the request. All insertion points are listed, even those that won't be audited because they are outside the scope of the scan configuration.

Note

If an insertion point won't be audited, it'll be labeled as Skipped. For more information, see

Insertion point statuses.

Insertion points are grouped in the tree view as follows:

Detected insertion points - Insertion points that Burp Scanner identified from existing data in the base request.

Moved insertion points - Insertion points that Burp Scanner can create by moving existing parameters to other locations within the request. For example, by moving a URL parameter to the message body. Moved insertion points are further subdivided by the type of movement, for example Cookie to URL path.

Added insertion points - Parameters that Burp Scanner can add to the request. For example, Burp Scanner can add a body parameter to allPOST requests.

Note

Burp Scanner only moves URL parameters, body parameters, and cookies. If these aren't present in the request, the Moved insertion points group isn't shown.

Nested insertion points

Nested insertion points occur when an application applies multiple layers of encoding to the same data, nesting one format within another. They are listed under the original insertion point in the tree view.

To view nested insertion points, click beside an insertion point. The decoding function is shown, along with the decoded base value. Click beside the decoding function to view nested parameters.

Related pages

Audit

options - Nested insertion points.

PortSwigger YouTube channel - Burp Suite Shorts | Nested insertion points.

Insertion points information

Each insertion point is identified in the tree view by type and name. If the method was changed in the modified request, this is also identified. For example,

Body param "category" (Method changed: GET POST).

To learn more about an insertion point, click on the insertion point in the tree view. The insertion point is highlighted in the request. The Information panel is also populated with the following details:

Name - The name of the insertion point.

Type - The type of insertion point. For example, cookie, URL parameter, or HTTP header. If it's a nested insertion point, the decoding function is shown here.

Base value - The original value of the insertion point in the base request.

Related pages

For more information on the different types of insertion points, see Audit settings - Insertion point

types.

Insertion point statuses

The action that Burp Scanner takes in relation to an insertion point depends on:

The scan configuration. For example, a configuration may result in Burp Scanner skipping some types of

insertion points or parameters.

The observed behavior of that type of insertion point. For example, if the insertion point has occurred frequently

without raising interesting behavior, Burp Scanner may do a light-audit of the insertion point, or skip it

entirely.

To enable you to identify what action Burp Scanner has taken in relation to an insertion point, each insertion point is given one of the following statuses:

Pending - Burp Scanner has flagged this insertion point for auditing.

Auditing - Burp Scanner is currently auditing this insertion point.

Audited - Burp Scanner has performed a full audit of this insertion point.

Light-auditing - This insertion point occurs frequently. Burp Scanner is therefore sending a small number of requests

to it, to determine whether it behaves similarly to other insertion points of the same type.

Light-audited - Burp Scanner sent a small number of requests to this frequently occurring insertion point. It hasn't

been fully audited because it behaves similarly to other insertion points of the same type that didn't raise

interesting behavior.

Skipped due to repetitive behavior - Burp Scanner didn't audit this insertion point.

This type of insertion point has occurred frequently without raising interesting behavior. It's also likely that its behavior will

stay consistent, because the insertion point is one of the following types:

URL path folder

URL path filename

Entire body

Skipped as limit exceeded - Burp Scanner didn't audit this insertion point, because it reached the maximum limit of

insertion points to audit per request. You can edit the limit in the scan configuration, under Insertion point nesting and limits.

Skipped as parameter movement not enabled - Burp Scanner didn't audit this insertion point, because your scan

configuration doesn't enable this type of parameter movement. You can change this in the scan configuration, under

Payload relocation rules.

Skipped due to insertion point type - Burp Scanner didn't audit this insertion point, because your scan configuration

doesn't enable auditing of this type of insertion point. You can change this in the scan configuration, under

Insertion point types.

Skipped due to parameter type - Burp Scanner didn't audit this insertion point, because your scan configuration

doesn't enable auditing of this type of parameter. You can change this in the scan configuration, under

Ignore insertion points.

Skipped as insertion point checks not enabled - Burp Scanner didn't audit this insertion point, because you haven't

enabled any insertion point scan checks in your scan configuration. To change this, edit the scan checks Burp

Scanner uses. Do this in the scan configuration under Scan checks.

Skipped as nested insertion points not enabled - Burp Scanner didn't audit this insertion point, because your scan configuration doesn't enable auditing of nested insertion points. You can change this in the scan configuration, under Insertion point nesting and limits.

Related pages

For more information about audit scan configurations, see Audit settings.

PortSwigger YouTube channel - Burp Suite Shorts | Frequently occurring insertion points.
