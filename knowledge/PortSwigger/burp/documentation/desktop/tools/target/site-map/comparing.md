# Comparing site maps

Source: https://portswigger.net/burp/documentation/desktop/tools/target/site-map/comparing
Fetched: 2026-06-28T09:16:08.995888+00:00

Support Center

Documentation

Desktop editions

Tools

Target

Site map

Comparing site maps

ProfessionalCommunity Edition

Comparing site maps

Last updated:

June 18, 2026

Read time:

4 Minutes

You can use this function to compare URLs for two site maps. This can help you find access control vulnerabilities, and identify areas to inspect manually. For example:

You can use accounts with different privilege levels to map the application, and compare the results. This enables you to identify functionality that is visible to one user but not the other.

You can use an account with high privileges to map the application, and then re-request the entire site map from a low-privileged account. This enables you to identify whether access to privileged functions is properly controlled.

You can use two different accounts of the same type to map the application, and compare the results. This enables you to identify cases where user-specific identifiers are used to access sensitive resources, and determine whether per-user data is properly segregated.

To access the comparison wizard, right-click the site map and select Compare site maps from the context menu. The wizard enables you to configure:

The sources of the site maps you want to compare.

How requests are matched between the site maps.

How to perform the response comparison.

Site map sources

You need to select the sources of the site maps that you want to compare:

Use current site map - Use the site map in Burp's Target tab.

Professional

Load from Burp project file - Use a site map from a saved Burp project file. This is useful if you have already mapped an application using accounts with different privilege levels.

Either of the above, re-requested in a different session context.

You can use all of the contents of the site map, or you can restrict the comparison to selected or in-scope items.

If you re-request a site map in a different session context, please note:

You need to create session handling rules so that the requests occur in the correct session context. Configure the rules to apply to requests made by the Target tool:

In simple cases, you may be able to use a rule that updates requests from the Target tool with cookies from Burp's cookie jar. The session uses the browser to acquire the desired session context before the comparison is done.

In other cases, you may need to create more complex session handling rules to validate the current session context and log in again. To learn more, see the session handling help.

We recommend that you exclude any requests that could disrupt the session context. These include login, logout, and user impersonation functions. To exclude these requests, restrict the comparison to selected or in-scope items.

Request matching

Burp compares the two site maps and matches each request across them, to identify any differences.

Burp matches requests based on the URL file path, HTTP method and the names of parameters in the query string and message body.

For some applications, you may want to customize how Burp performs the matches:

URL file path - You need to include this for each comparison. It identifies that two requests are equivalent.

HTTP method - We recommend that you include this. In most cases, applications use GET and POST requests to the same URL for different purposes.

URL query string - In most cases, you need to include this. Requests with different URL parameters are normally used for different application functions. There are two options:

Match parameter names only - Match query strings with the same parameter names but different values. This is useful if parameter values contain user-specific or ephemeral data. Deselect this setting if parameter names identify the application function being performed, for example action=CreateUser.

Ignore these parameters - Specify parameters that are ignored when matching query strings.

Request body - We recommend you include this, because requests with different body parameters are normally used for different application functions. You can choose from the same two options as URL query string.

Request headers - Prevents requests with different HTTP headers after the first line from being matched. In most cases, you don't need to select this setting: browsers may modify request headers for reasons that have nothing to do with application-level functionality. Enable this setting if the application uses script-generated requests with custom HTTP headers, to identify the function of requests.

Response comparison

Burp compares the responses to matched requests, to identify any differences. You can customize the response comparison to suit your target application:

Response headers - Include all headers, or restrict the comparison to specific headers. We recommend that you include response headers with values that reflect the application's functionality and state, such as Set-Cookie.

Form field values - Include all form field values, or restrict the comparison to specific values. Form field values often reflect differences that can identify access control problems. To analyze these:

Highlight the form field values for manual review.

Modify the setting to exclude irrelevant fields.

Repeat the comparison.

Whitespace - Choose to ignore whitespace-only variations in responses. These are not normally relevant to access control issues.

MIME type - Skip comparisons of non-text content. These comparisons are computationally intensive. Also, the responses are likely to contain static content such as images, which are not relevant to access control issues.

The default settings work well in most situations. They are designed to reduce noise, by ignoring various common HTTP headers and form fields that have ephemeral values, and whitespace-only variations in responses.

The results are displayed in a table. You can customize and sort the table contents. For more information, see Customizing Burp's tables.
