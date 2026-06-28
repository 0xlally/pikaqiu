# Audit settings

Source: https://portswigger.net/burp/documentation/scanner/scan-configurations/audit-settings
Fetched: 2026-06-28T09:16:10.911275+00:00

Support Center

Documentation

Scanner

Scan configurations

Audit settings

DASTProfessional

Audit settings

Last updated:

June 18, 2026

Read time:

11 Minutes

Burp Scanner offers numerous settings that control how scans behave during the audit phase. You can select these settings when you create or edit scan configurations in Burp Suite Professional or Burp Suite DAST.

Related pages

Using custom scan configurations (Burp Suite DAST).

Configuration library (Burp Suite Professional).

Audit behavior

Use these settings to configure how Burp manages the audit process and handles timeouts.

Audit strategy

These settings enable you to tune Burp Scanner's audit coverage and speed, to reflect the objectives of the audit and the nature of the target application.

Audit speed

This setting determines how thoroughly Burp Scanner undertakes certain audit checks:

Fast makes fewer requests, and checks for fewer derivations of some vulnerabilities.

Thorough makes many more requests and checks for more derivative types of vulnerabilities.

Normal is mid-way between the two, and represents a suitable trade-off between speed and thoroughness for many applications.

Audit accuracy

This option determines the amount of evidence that the Scanner requires before it can report certain vulnerability types.

Some issues can only be detected using blind techniques, in which Burp infers the probable existence of a vulnerability based on observed behavior, such as a time delay or a differential response. Because these behaviors can also occur in the absence of the associated vulnerability, blind techniques are inherently more prone to false positives than other detection methods.

To attempt to reduce false positives, Burp repeats certain tests a number of times when it first infers a potential issue. Use the Audit accuracy setting controls to set how many times Burp retries these tests:

Minimize false negatives performs fewer retries, and so is more likely to report false positives but less likely to miss genuine issues.

Minimize false positives performs many more retries, and so is less likely to report false positives. However this setting may result in Burp Scanner missing some genuine issues, because some of the retry requests might not return the result being tested for.

Normal is mid-way between the two, and represents a suitable trade-off between false positive and false negative issues for many applications.

Skip checks unlikely to be effective

This setting makes scans more efficient by omitting checks that appear irrelevant given the base value of the parameter at each insertion point.

For example, if a parameter's value contains characters that do not normally appear in filenames, Burp skips file path traversal checks for this parameter. Use this option to speed up your scans, with a relatively low risk that you will miss vulnerabilities.

Automatically maintain session

This setting controls whether Burp maintains session automatically during the audit phase of the scan. This is only applicable to crawl-driven audits where the navigational pathways identified during the crawl phase can be used to maintain session during the audit phase.

In modern applications, it is normally essential to maintain session to achieve good audit coverage. However, there is an overhead to maintaining session in terms of numbers of requests made. You can disable this option if you know it is not necessary.

Related pages

Auditing: Automatic session handling.

Follow redirections where necessary

Some vulnerabilities (for example, cross-site scripting in an error message that is only returned after following a redirect) can only be detected by following redirects.

Burp does not follow all redirects by default, because some applications issue redirects that contain parameter values that you submitted to third-party URLs. This protects you against inadvertently attacking third-party applications.

If the request being scanned is within the defined target scope, Burp only follows redirects that are within that same scope. If the request being scanned is not in scope, Burp only follows redirects that are:

To the same host/port as the request being scanned.

Not explicitly covered by a suite-wide scope exclusion rule, for example "logout.aspx".

Related pages

Target scope.

Allow crawl and audit phases to run in parallel

Use this setting to control whether Burp begins auditing while the crawl is still in progress.

When enabled, this can make issue discovery more efficient by allowing Burp to start auditing as soon as the first issue is found, instead of first waiting for the entire crawl to finish.

Related pages

Auditing.

Total scan time

This setting defines the maximum total run time for each scan, in minutes. It is not available for audit-only scans, or scans that are currently in progress. If a scan reaches the time limit then it pauses and an entry is added to the event log.

Issue noise reduction

Use this setting to control whether Burp consolidates frequently-occurring passive issues. This option reduces noise when the same issue (for example, Clickjacking) appears in many locations or even throughout an entire application.

Related pages

Auditing: Consolidation of frequently occurring passive issues.

Audit network timeouts

These settings enable you to specify timeout values for the audit. These values override any you may have configured in the global settings.

Handling repeated timeouts during audit

These settings control how Burp Scanner responds to repeated timeouts (connection failures and transmission timeouts) that arise during the audit phase of the scan.

You can configure the following options:

The number of consecutive failed audit checks that can occur before Burp Scanner skips the remaining checks in the current insertion point.

The number of consecutive failed insertion points that can occur before Burp Scanner skips the remaining insertion points and flags the audit item as failed.

The number of consecutive failed audit items, or the overall percentage of failed audit items, that can occur before Burp Scanner pauses the task.

The number of follow-up passes that Burp Scanner performs on completion of each audit phase to retry requests that timed out.

To disable any of these functions, leave the corresponding setting blank.

Related pages

Auditing: Handling application errors

Scan checks

These settings control scan checks Burp uses during the scan.

Each check that Burp Scanner performs increases the number of requests made and the overall audit time. You may want to disable scanning for some issue types based on your knowledge of an application's technologies.

For example, if you know that an application does not use any LDAP, you could turn off LDAP injection. Likewise, if you know which back-end database the application uses, you can turn off SQL injection detection methods that are specific to other database types.

You can select scan checks in two ways:

Scan type - Select checks by the nature of the audit activity involved in detecting them. You can select from the following options:

Passive.

Light active.

Medium active.

Intrusive active.

JavaScript analysis.

Individual issues - Use the checkboxes on the side of the scan check list to select the scan checks you want Burp to use. Use the search bar to find individual scan checks or click the column headers to sort the list of issues.

Note

For active issue types, Burp Scanner sends requests to the application designed to detect those issues. Depending on the issues selected, these requests might be reasonably viewed as malicious, or might damage the application and its data.

JavaScript analysis

These settings control how Burp Scanner detects DOM-based vulnerabilities in JavaScript. The following settings are available:

Use static/dynamic analysis techniques - Controls whether Burp Scanner uses static or dynamic techniques, or both, for JavaScript analysis. To configure whether to use static or dynamic techniques for individual issue types, edit the enabled detection methods for DOM-based issues.

Make requests for missing site resources - Controls whether Burp Scanner makes HTTP requests for any missing dependencies, such as JavaScript files.

Fetch previously undiscovered resources and data from out-of-scope hosts - Controls whether resources and data that are referenced by a page but were not discovered by Burp Scanner during crawling are loaded from locations that are out of scope for the scan. You may encounter this scenario if you run an audit-only scan on:

Items that you discovered while manually exploring the site.

Items that were added to the site map by a previous scan but have since been changed on the live website.

If you disable this option, the scan does not load these resources during auditing and may miss vulnerabilities as a result. For example, a page may be safe until it loads an external JavaScript file that introduces vulnerabilities on execution.

Maximum static/dynamic analysis time per item - Controls the maximum time that Burp spends on static or dynamic analysis for each item that is scanned. This setting is useful if Burp encounters items containing very large or complex scripts, which may cause the static analysis engine to consume excessive system resources. If Burp Scanner truncates analysis because the maximum time is reached, it shows an alert identifying the item affected. You can specify zero or a blank value to indicate that there is no time limit.

Note

JavaScript analysis can consume large amounts of system resource. As a result, you may want to restrict the analysis to key targets. It may also be necessary to launch Burp with greater amounts of memory when performing JavaScript analysis. To do so, launch Burp from the command line.

Related pages

DOM-based vulnerabilities.

JavaScript analysis phase.

Insertion points strategy

Configure how Burp uses insertion points during the audit. An insertion point is a location in the message where Burp inserts payloads to test for vulnerabilities.

Set insertion point types

These settings control the types of insertion point that Burp Scanner can insert payloads into during the audit.

Burp Scanner can add the following types of insertion point:

URL parameter values - Standard parameter values within the URL query string.

Body parameter values - Parameter values in the message body, including:

Standard form-generated parameters.

Attributes of multipart-encoded parameters, such as uploaded file names.

XML parameter values and attributes.

JSON values.

Cookie values - The values of HTTP cookies.

Parameter name - The name of an arbitrarily added parameter. Burp Scanner always adds a URL parameter. It also adds a body parameter to all POST requests. Testing an added parameter name can often detect unusual bugs that are not detected if only parameter values are tested.

HTTP headers - HTTP header values. Burp Scanner can test the Referer and User-Agent headers, as well as any custom header beginning with x-. Testing these insertion points can often detect issues such as SQL injection or persistent XSS within logging functionality.

Entire body - The whole of the request body. This applies to requests with XML or JSON content in the request body.

URL path filename - The value of the filename part of the URL path. This is the portion of the URL after the final path folder and before the query string.

URL path folders - The values of all folder tokens within the URL path, before the filename.

Ignore specific insertion points

These settings enable you to specify request parameters for which Burp Scanner skips audit checks. You can choose to either skip server-side injection checks (such as SQL injection) or skip all checks for a given parameter.

Skipping all checks may be useful if a parameter is handled by an application component that you do not wish to test, or if modifying a parameter is known to cause application instability.

Server-side injection checks mean that Burp needs to send multiple requests to probe for various blind vulnerabilities on the server. If you believe that certain parameters that appear within requests are not vulnerable (for example, built-in parameters used only by the platform or web server), you can tell Burp not to test them.

To add a parameter to the ignored insertion point lists:

Click Add on the list you want to add the parameter to (either Skip server-side injection tests or Skip all tests) to display a dialog.

Select a Match item. This is the type of parameter you want to skip.

Select whether you want to match the parameter on Name or Value.

Select a Match type. This can be either a literal string or a regex.

Enter the Match expression that you want to match the parameter on.

Click OK to add the parameter to the selected list.

Note

You can identify parameters within URL path folders either by their position (slash-delimited) within the URL path or the folder name.

To filter by URL path position:

Select URL path folder from the Match item drop-down.

Select Name from the Name or value drop-down.

Select is from the Match type drop-down.

Enter the index number (1-based) of the position within the URL path that you wish to exclude from testing in the Match expression drop-down.

To filter by folder name, select the following:

Select URL path folder from the Match item drop-down.

Select Value from the Name or value drop-down.

Select is from the Match type drop-down to match an exact string, or select matches expression to match regex.

Enter the folder name or regex you want to match in the Match expression drop-down.

Handling frequent insertion points

These settings enable you to configure whether Burp Scanner avoids duplication in frequently occurring insertion points. You can select to apply this optimization to the following insertion points:

URL parameter values.

Body parameter values.

Cookie parameter values.

Parameter name.

HTTP headers.

Entire body.

URL path filename.

URL path folders.

When configured, Burp identifies insertion points that have proven to be uninteresting (that is, occurring frequently without any issues generated) and performs a more lightweight audit of those insertion points.

Related pages

Auditing: Handling of frequently occurring insertion points.

Nested insertion points

Some applications apply multiple layers of encoding to the same data, effectively nesting one format within another. For example, a URL parameter might contain Base64-encoded data, and the decoded value might in turn contain JSON or XML data.

If you select Use nested insertion points, Burp Scanner detects this behavior, and automatically applies the same layers of encoding to payloads. Burp creates suitable insertion points for each separate item of input at each level of nesting.

Nested insertion points impose no overhead when you scan requests that contain only conventional request parameters. Despite this, they enable Burp to reach more of the attack surface of complex applications where data is encapsulated within different formats.

Insertion point limits

You can set a limit on the number of insertion points that can be generated for each base request. This prevents your scans from stalling if they encounter requests containing huge numbers of parameters.

When Burp needs to curtail the number of insertion points, the item's entry in the audit indicates the number of insertion points that were skipped. This enables you to review the base request manually and decide if it is worth performing a full scan of all its possible insertion points.

Payload relocation rules

These settings enable you to configure the Scanner to insert payloads for one insertion point type into other insertion point types within the request. This enables input to be tested in a range of locations. For example, you could move each URL parameter into the message body and retest it there.

The following options are available:

URL to body.

URL to cookie.

Body to URL.

Body to cookie.

Cookie to URL.

Cookie to body.

Moving parameters in this way can often bypass defensive filters. Many applications and firewalls perform per-parameter input validation. This assumes that each parameter is in its expected location within the request. If you move the parameter to a different location, you can evade this validation.

When the application code later retrieves the parameter to implement its main logic, it may use an API that does not factor the parameter's location. If this is the case, moving the parameter may enable you to reach vulnerable code paths by using input that would normally be filtered before being processed.

Changing parameter locations results in many more scan requests, because each request parameter is effectively scanned multiple times.

Related pages

Payload relocation rules.
