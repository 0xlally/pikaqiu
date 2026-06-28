# Burp Scanner error reference

Source: https://portswigger.net/burp/documentation/scanner/burp-scanner-error-reference
Fetched: 2026-06-28T09:16:11.379114+00:00

Support Center

Documentation

Scanner

Burp Scanner error reference

DASTProfessional

Burp Scanner error reference

Last updated:

June 18, 2026

Read time:

49 Minutes

This is a quick reference guide to troubleshooting the most common Burp Scanner error messages. You can use Ctrl/Cmd + F to search for the error you've encountered to see more detailed information about the potential cause of the problem and some remediation advice. If you cannot find your error message listed, please contact our support team for more assistance.

Burp Scanner errors in Burp Suite Professional

When sending a request to X, the server responded with a rate-limiting header requesting to wait X seconds.

Cause

The server included a rate-limiting header in a response, explicitly telling Burp Scanner how long to wait before making another request. This is a server-specified rate limiting mechanism.

Remedy

This is normal behavior - Burp Scanner is respecting the server's rate limiting instructions. The scanner will automatically continue after waiting for the specified time.

If you want to disable this behavior and use Burp's own throttling instead, you can disable Automatic throttling in your resource pool settings.

Your seed URL X was redirected to X which is out of scope.

Cause

Burp Scanner only visits URLs that are in scope. This protects you from scanning sites that you don't have permission to scan.

Remedy

If you have permission to scan the URL that your seed URL was redirected to, you can add it to your scope and run the scan again. For more information, please refer to Scope settings.

Note

You may need to add specific subdomains to your scope. For example, https://www.portswigger.net redirects to https://portswigger.net. If you only include https://www.portswigger.net in your scope, the redirect URL will be out of scope.

Can't find existing log file!

Cause

Our technical support team may have asked you to enable debug logging for a scan in order to help diagnose a problem you reported. This creates a log file called something like crawlDebug-1-1234567890123.log when the scan runs. Burp Suite tried to load a scan at startup, but could not find the associated log file. This could be because it has been moved or deleted.

Remedy

If you moved this file from its original location, put it back and try again. To find the expected location:

From the Burp's Dashboard tab, click the settings icon for the related scan.

Go to the Scan configuration tab.

Under Crawl strategy, click the settings icon next to the Crawl strategy menu.

Check the Directory field.

Note

The logging option is not recommended for normal operation. Generally speaking, you should only enable it when asked to do so by our support team.

Can't write to log file: X.

Cause

Our technical support team may have told you to enable debug logging for a scan in order to help diagnose a problem you reported. This creates a log file called something like crawlDebug-1-1234567890123.log when the scan runs. Burp Scanner encountered errors while trying to write to this file. This could be caused by permissions or other file system problems with the location you have selected for the log file.

Remedy

Make sure that the burpsuite user has permission to write to the specified directory, or select a different directory to save the log file in.

Note

The logging option is not recommended for normal operation. Generally speaking, you should only enable it when asked to do so by our support team.

Failed to replay sequence X - X.

Cause

Burp Scanner was unable to successfully replay one or more steps of a recorded login sequence during the scan.

Remedy

Contact our Support team with the following:

An HTML snippet of the login form.

The login script (JSON) exactly as it is pasted into Burp.

A screen recording of the login sequence being performed by Burp Scanner. To do this, under Application Login, select your recorded login sequence and click Replay.

A screenshot of the event log (if any errors are visible) and the diagnostics from Help > Diagnostics.

Cannot replay sequence, failed to create a browser.

Cause

Burp Scanner was unable to start Burp's browser that it uses to replay recorded login sequences.

Remedy

Run the Health check for Burp's browser from the Help menu in Burp Suite. This will diagnose problems with the browser.

Skipping API definition. The data in the definition file is malformed and cannot be read by Burp Scanner.

Cause

Burp Scanner needs to be able to parse an API definition in order to scan it. Currently, this is only possible for definitions that:

Meet the API definition requirements.

Do not contain any external references.

Any definitions that do not meet these requirements will be skipped during the scan.

Remedy

Make sure that the API definition you're trying to scan meets the prerequisites outlined above. For more details, please refer to the documentation for API scanning.

Environment not supported by browser. (Use 'Health check for Burp's browser' for more details.)

Cause

Burp Scanner could not start Burp's browser as it is not supported by the current operating system environment.

Remedy

Run the Health check for Burp's browser from the Help menu in Burp Suite. This will diagnose problems with the browser.

Could not start browser.

Cause

Burp Scanner could not start Burp's browser due to an unexpected error.

Remedy

Run the Health check for Burp's browser from the Help menu in Burp Suite. This will diagnose problems with the browser.

Could not start Burp's browser sandbox because you are running as root. Either switch to running as an unprivileged user or allow running without sandbox.

Cause

For security reasons, on Linux, Burp's browser runs in sandbox mode by default. When logged in as root, this may prevent the browser from launching properly.

Remedy

You have the following options:

Switch to a different user. We recommend this option wherever possible.

Allow the browser to run without a sandbox. Configure this in the Settings dialog, under Tools > Burp's browser.

Warning

Scanning hostile websites without a sandbox can increase the risk of your local machine being compromised. Before enabling this setting, make sure that you understand the security implications.

Can not start Burp's browser sandbox because your kernel does not support user namespaces. Please either upgrade your kernel or allow running without sandbox.

Cause

Running Burp's browser in sandbox mode on Linux requires a Kernel that supports User namespaces.

Remedy

You can either upgrade to a Kernel that supports namespaces or allow the browser to run without the sandbox. Configure this in the Settings dialog, under Tools > Burp's browser.

Warning

Scanning hostile websites without a sandbox can increase the risk of your local machine being compromised. Before enabling this setting, make sure that you understand the security implications.

Can not start Burp's browser sandbox because the chrome-sandbox binary is not configured correctly and your kernel has user namespace cloning disabled. To enable, run the following command as root: "echo 1 > /proc/sys/kernel/unprivileged_userns_clone"

Cause

Burp Scanner will by default run Burp's browser in sandbox mode. This requires an operating system environment that supports namespace cloning. Sandbox mode is a security feature of Chromium that makes browsing more secure.

Remedy

If you enable namespace cloning Burp's browser can run in sandbox mode. Running the command in the error message will enable namespace cloning until you reboot. You can save this setting in your sysctl.conf file to enable this setting permanently. Please refer to the documentation for your operating system for more details.

Can not start Burp's browser sandbox because the chrome-sandbox binary is not configured correctly and your kernel has user namespace cloning disabled. To enable, run the following command as root: "echo 0 > /proc/sys/kernel/userns_restrict"

Cause

Burp Scanner will by default run Burp's browser in sandbox mode. This requires an operating system environment that supports namespace cloning. Sandbox mode is a security feature of Chromium that makes browsing more secure.

Remedy

If you enable namespace cloning Burp's browser can run in sandbox mode. Running the command in the error message will enable namespace cloning until you reboot. You can save this setting in your sysctl.conf file to enable this setting permanently. Please refer to the documentation for your operating system for more details.

Cannot handle streaming response: X.

Cause

Burp Scanner does not support streaming responses. It will skip pages that provide a streaming response.

Remedy

You can test streaming responses using Burp Suite's manual tool. For more information, please refer to the documentation on streaming responses.

Error generating report: X.

Cause

Burp Scanner encountered a file system error when trying to open or write to the scan report file. This can be caused by permissions or other file system errors.

Remedy

Check that the burpsuite user has permission to write to the folder you are trying to save the report to or try saving the report to a different folder.

The Burp Collaborator server used by the Burp Collaborator client is not reachable, change the settings to use this feature.

Cause

The Burp Collaborator client was unable to connect to the Burp Collaborator server that it uses to perform OAST checks. As a result, these checks were skipped for this scan.

Remedy

Run the Collaborator Server health check and double-check the Collaborator server settings. View these in the

Settings dialog, under the Project > Collaborator tab.

Failed to connect to the configured Collaborator server: X.

Cause

Burp Scanner was unable to connect to the selected Burp Collaborator server. As a result, OAST checks were skipped for this scan.

Remedy

Run the Collaborator Server health check and double-check the Collaborator server settings. View these in the

Settings dialog, under the Project > Collaborator tab.

Skipping X. Too many consecutive "unknown host" errors have occurred.

Cause

Burp Scanner could not resolve a hostname when making a request during the audit phase. This can be caused by a number of issues, including intermittent network problems, server load, or security measures like Web Application Firewalls.

Remedy

Experiencing intermittent problems accessing a site is normal and does not necessarily indicate a problem. Scans may overload servers and the unusual activity may cause Web Application Firewalls to start blocking requests, for example. To help avoid these issues, you can configure resource pools to control the number of requests you're sending and how frequently. By default, Burp Scanner will mark any failed requests for a follow-up pass, but you can also configure it to make more passes.

Skipping X. Too many consecutive "request timeout" errors have occurred.

Cause

Burp Scanner identifies insertion points where it can try injecting different payloads. Repeated attempts to insert a payload into the current insertion point or the current page have failed.

Remedy

Experiencing intermittent problems accessing a site is normal and does not necessarily indicate a problem. Scans may overload servers and the unusual activity may cause Web Application Firewalls to start blocking requests, for example. To help avoid these issues, you can configure resource pools to control the number of requests you're sending and how frequently. By default, Burp Scanner will mark any failed requests for a follow-up pass, but you can also configure it to make more passes.

Skipping X. Too many consecutive "request aborted" errors have occurred.

Cause

Burp Scanner identifies insertion points where it can try injecting different payloads. Repeated attempts to insert a payload into the current insertion point or the current page have failed.

Remedy

Experiencing intermittent problems accessing a site is normal and does not necessarily indicate a problem. Scans may overload servers and the unusual activity may cause Web Application Firewalls to start blocking requests, for example. To help avoid these issues, you can configure resource pools to control the number of requests you're sending and how frequently. By default, Burp Scanner will mark any failed requests for a follow-up pass, but you can also configure it to make more passes.

Skipping X. Too many consecutive "connection failed" errors have occurred.

Cause

Burp Scanner identifies insertion points where it can try injecting different payloads. Repeated attempts to insert a payload into the current insertion point or the current page have failed.

Remedy

Experiencing intermittent problems accessing a site is normal and does not necessarily indicate a problem. Scans may overload servers and the unusual activity may cause Web Application Firewalls to start blocking requests, for example. To help avoid these issues, you can configure resource pools to control the number of requests you're sending and how frequently. By default, Burp Scanner will mark any failed requests for a follow-up pass, but you can also configure it to make more passes.

Skipping X. Too many consecutive "empty response" errors have occurred.

Cause

Burp Scanner identifies insertion points where it can try injecting different payloads. Repeated attempts to insert a payload into the current insertion point or the current page have failed.

Remedy

Experiencing intermittent problems accessing a site is normal and does not necessarily indicate a problem. Scans may overload servers and the unusual activity may cause Web Application Firewalls to start blocking requests, for example. To help avoid these issues, you can configure resource pools to control the number of requests you're sending and how frequently. By default, Burp Scanner will mark any failed requests for a follow-up pass, but you can also configure it to make more passes.

Skipping X. Too many consecutive "missing link on path to crawled location" errors have occurred.

Cause

Burp Scanner's crawl engine accesses URLs in the same way as a human accessing a website would. It starts at the specified URLs and follows links through a website. A page discovered during the crawl could no longer be found by following links from the specified starting URL due to one of more links no longer being present, although it might still exist on the site.

Remedy

Experiencing intermittent problems accessing a site is normal and does not necessarily indicate a problem. Scans may overload servers and the unusual activity may cause Web Application Firewalls to start blocking requests, for example. To help avoid these issues, you can configure resource pools to control the number of requests you're sending and how frequently. By default, Burp Scanner will mark any failed requests for a follow-up pass, but you can also configure it to make more passes.

Skipping X. Too many consecutive "error on path to crawled location" errors have occurred.

Cause

Burp Scanner's crawl engine accesses URLs in the same way as a human accessing a website would. It starts at the specified URLs and follows links through a website. A page discovered during the crawl could no longer be found by following links from the specified starting URL due to one or more errors when following links, although it might still exist on the site.

Remedy

Experiencing intermittent problems accessing a site is normal and does not necessarily indicate a problem. Scans may overload servers and the unusual activity may cause Web Application Firewalls to start blocking requests, for example. To help avoid these issues, you can configure resource pools to control the number of requests you're sending and how frequently. By default, Burp Scanner will mark any failed requests for a follow-up pass, but you can also configure it to make more passes.

Skipping X. Too many consecutive "missing request at crawled location" errors have occurred.

Cause

Burp Scanner's crawl engine accesses URLs in the same way as a human accessing a website would. It starts at the specified URLs and follows links through a website. A page discovered during the crawl no longer triggered the expected requests when revisited for auditing.

Remedy

Experiencing intermittent problems accessing a site is normal and does not necessarily indicate a problem. Scans may overload servers and the unusual activity may cause Web Application Firewalls to start blocking requests, for example. To help avoid these issues, you can configure resource pools to control the number of requests you're sending and how frequently. By default, Burp Scanner will mark any failed requests for a follow-up pass, but you can also configure it to make more passes.

Skipping X. Too many consecutive "crawled location no longer in scope" errors have occurred.

Cause

Burp Scanner's crawl engine accesses URLs in the same way as a human accessing a website would. It starts at the specified URLs and follows links through a website. A page discovered during the crawl could no longer be found whilst adhering to scope rules, although it might still exist on the site.

Remedy

Experiencing intermittent problems accessing a site is normal and does not necessarily indicate a problem. Scans may overload servers and the unusual activity may cause Web Application Firewalls to start blocking requests, for example. To help avoid these issues, you can configure resource pools to control the number of requests you're sending and how frequently. By default, Burp Scanner will mark any failed requests for a follow-up pass, but you can also configure it to make more passes.

Skipping X. Too many consecutive "insertion point no longer present" errors have occurred.

Cause

Burp Scanner's audit phase cannot find an insertion point identified during the crawl phase. This can happen for a number of reasons and may not represent a problem. Intermittent connection issues can prevent pages from loading properly. Testing a Web Application can put a server under unusual load, leading to pages not loading properly. A Web Application Firewall can detect unusual activity and start blocking requests.

Remedy

Experiencing intermittent problems accessing a site is normal and does not necessarily indicate a problem. Scans may overload servers and the unusual activity may cause Web Application Firewalls to start blocking requests, for example. To help avoid these issues, you can configure resource pools to control the number of requests you're sending and how frequently. By default, Burp Scanner will mark any failed requests for a follow-up pass, but you can also configure it to make more passes.

Skipping X. Too many consecutive "streaming response" errors have occurred.

Cause

Burp Scanner does not support streaming responses. It will skip URLs that provide streaming responses.

Remedy

You can test streaming responses using Burp Suite's manual tool. For more information, please refer to the documentation on streaming responses.

Skipping X. Too many consecutive "browser crash" errors have occurred.

Cause

Burp's browser crashed while requesting a URL. By default, Burp Scanner attempts to request the URL one more time. Burp's browser crashed again during this follow-up pass.

Remedy

Configure Burp Scanner to make more passes.

If this occurs repeatedly on a single site, try manually navigating to the page and see if it crashes the browser while browsing manually.

If this occurs on multiple sites, try running the Health check for Burp's browser.

Skipping X. Too many consecutive "browser action failed" errors have occurred.

Cause

Burp's browser crashed while requesting a URL. By default, Burp Scanner attempts to request the URL one more time. Burp's browser crashed again during this follow-up pass.

Remedy

Configure Burp Scanner to make more passes.

If this occurs repeatedly on a single site, try manually navigating to the page and see if it crashes the browser while browsing manually.

If this occurs on multiple sites, try running the Health check for Burp's browser.

Skipping X. Too many consecutive "replayer error" errors have occurred.

Cause

Burp's browser crashed while requesting a URL. By default, Burp Scanner attempts to request the URL one more time. Burp's browser crashed again during this follow-up pass.

Remedy

Configure Burp Scanner to make more passes.

If this occurs repeatedly on a single site, try manually navigating to the page and see if it crashes the browser while browsing manually.

If this occurs on multiple sites, try running the Health check for Burp's browser.

Found 0 new locations after logging in.

Cause

Burp Scanner keeps track of whether or not the page shown after logging in is different from the page shown before logging in. In this case, after logging in, the pages available were not significantly different. This does not necessarily mean the login failed, but this is one possible cause.

Remedy

Try the following actions:

Double-check your application login settings to make sure the provided credentials are correct.

Run Burp Scanner in headed mode and watch it attempt to log in to see if you can spot any issues.

Try using a recorded login sequence if you aren't already. This allows Burp Scanner to handle much more complex login forms, like those featuring iFrames and SSO.

Failed to lookup host X while crawling.

Cause

Burp Scanner was unable to crawl a location because it could not resolve the hostname. This can be caused by either an incorrect hostname in the URLs provided or a DNS error.

Remedy

Check for typos or other errors in the URLs to Scan. Make sure you can access the host from a browser.

X consecutive requests have failed.

Cause

During the crawl phase, the scan will automatically be paused if the error handling threshold is exceeded. This prevents the scan from needlessly crawling a site that is currently down, for example.

Remedy

Check that the web application being scanned is still running and accessible.

You can also adjust the number of consecutive failed requests that cause Burp Scanner to pause the crawl in the crawl settings under Handling repeated timeouts during crawl.

More than X percent of requests have failed.

Cause

During the crawl phase, the scan can automatically be paused if more than a certain percentage of requests fail. This prevents the scan from needlessly crawling a site that is currently down, for example.

Remedy

Check that the web application being scanned is still running and accessible.

You can also adjust the number of consecutive failed requests that cause Burp Scanner to pause the crawl in the crawl settings under Handling repeated timeouts during crawl.

Could not connect to any seed URLs.

Cause

Burp Scanner was unable to send requests to any of the specified URLs to scan. This error can be caused by anything that prevents Burp Scanner from connecting to the URL. This can include timeouts, connection failed errors, and problems resolving hostnames.

Remedy

Try the following actions:

Check for typos and other errors in the URLs to Scan.

Check that you are able to connect to the target application from the machine running the scan.

If you have any trouble doing this, troubleshoot your connection to the hostname that is failing.

Check the firewall, proxy, and DNS server settings for the machine running the scan.

Crawl was configured to use Burp's browser, but a browser could not be started.

Cause

Burp Scanner was unable to start Burp's browser. This can be caused by various issues with the browser.

Remedy

Run the Health check for Burp's browser from the Help menu in Burp Suite. This will diagnose problems with the browser.

Cannot continue crawl started before version X.

Cause

Burp Scanner's crawl engine sometimes gets updated in such a way that it cannot open files created in previous versions. While this happens relatively infrequently, it can happen when adding new features or significantly changing how it operates.

Remedy

Recreate your scan in the new version.

Burp has detected that the project file may be corrupted. It is not advisable to continue working with this file.

Cause

There are multiple ways that a project file can be corrupted. One common way is to shut down a Windows machine while a project file is accessing a network file system (by closing the lid on your laptop, for example). This causes the OS to fail to sync the data correctly.

Remedy

Because this issue can have multiple causes, we recommend that you contact our Support team, including:

Your Burp Suite diagnostics information (Help > Diagnostics).

A list of any Burp tools you were using at the time of the issue.

(If possible), a copy of your Burp project file.

If you think that the issue might relate to your machine entering Sleep / Hibernate mode, then it may be worth reviewing your operating system's power saving settings.

The Collaborator server software is out of date. Some Burp features will not work properly with the configured Collaborator server.

Cause

The version of Burp Suite you are using is older than the configured Collaborator server.

Remedy

Upgrade to the latest version of Burp Suite Professional.

Scan stopped. Configured maximum crawl and audit time elapsed.

Cause

The scan cannot be completed within the maximum scan time specified. Burp Scanner has paused the scan's execution.

Remedy

If you want the scan to complete, restart its execution from the Dashboard. Note that the scan will complete without a crawl and audit time limit.

If you want to raise your scan's maximum scan time, you can edit this from the Audit strategy settings in the scanning configuration, under Total scan time. Leave this field blank if you do not want a limit.

Burp's browser could not be started. Using non-browser based navigation.

Cause

Something has prevented Burp's browser from starting. There are multiple reasons that this might happen.

Remedy

From the Help menu, run the Health check for Burp's browser tool.

Total available memory is only X MB - you should ideally set a larger maximum heap size, for example: X.

Cause

Insufficient memory (RAM) is available for Burp Suite to operate correctly. Some of Burp Suite's features may not work properly, including Burp's browser.

Remedy

See our tips on how to optimize Burp Suite's memory usage.

Skipping Hidden HTTP/2 scan check because HTTP/2 is disabled.

Cause

HTTP/2 is disabled. This means that Burp Scanner can't check for the hidden HTTP/2 vulnerability.

Remedy

To enable HTTP/2, go to HTTP settings under Network in the Settings dialog. Scroll to HTTP/2, and select Default to HTTP/2 if the server supports it.

Throttling HTTP/2 requests to X due to server concurrent stream limit.

Cause

The server is limiting the number of concurrent requests that can be made to it. Because of this, Burp Suite is throttling the number of concurrent HTTP/2 requests to the server's maximum.

Remedy

N/A (Information only)

X: Automatic update failed: X.

Cause

BApps require a connection to the BApp Store in order to receive updates. A likely cause of this error is that your connection to the BApp Store is failing. For more information, see our

troubleshooting guide.

Remedy

To test your connection to the BApp Store, click Extensions > BApp Store > Refresh list. If your connection fails, you will see an error in the bottom right hand corner of the screen.

Skipping brute force of JWT token as maximum time exceeded.

Cause

JWT tokens use a signature to validate their contents. In some cases, Burp Scanner will attempt to brute-force this signature in order to compromise the token. This error has been caused by Burp Scanner running out of time during the brute-forcing process.

Remedy

To increase the amount of time that Burp Scanner spends brute-forcing JWT token signatures, from the Audit strategy menu, set Audit speed to Thorough.

Failed to find additional locations after recorded sequence: X.

Cause

When using a recorded login, Burp Scanner first runs a crawl without using your recorded login. It then compares it to a crawl using your recorded login. If no additional content is discovered, then this error appears.

This can occur for a number of reasons:

Your recorded login has failed.

Your recorded login ends on a page that is out of scope for your scan. Note that Burp Scanner ignores scope while performing a recorded login sequence. However, any out of scope locations are not crawled and / or audited as part of that scan.

Burp Scanner is not finding any additional content, because the selected crawl strategy is not complete enough.

Remedy

If you think your recorded login has failed, then see our documentation on troubleshooting recorded login sequences in Burp Suite Professional.

If your recorded login ends on a page that is out of scope for your scan and you want to adjust your scope to include that page, then you can do this from the Target Scope menu.

If you want to try a more complete crawl strategy, then select this under Crawl settings.

Blocked out-of-scope request to X.

Cause

Burp Scanner has attempted to make a request that has been blocked, because the target URL is outside of its scope. Note that Burp Scanner uses its own scope, that is separate from Burp Suite's Target Scope.

There are a number of reasons that Burp Scanner might have attempted to make this request - one example is link redirection.

Remedy

If you want Burp Scanner to make requests to this URL, from the Dashboard tab, click New scan > Webapp scan. From the web application scan launcher, under Scan details, add the URL to the list of URLs to Scan.

Crawl aborted due to too many requests being made.

Cause

Burp Scanner has reached its Maximum request count.

Remedy

From Crawl configuration settings, change your Crawl limits settings to allow an increased Maximum request count.

Maximum time exceeded in static code analysis of: X.

Cause

Burp Scanner's static JavaScript analysis feature has reached the maximum time it is allocated for analysis of an individual item.

Remedy

There are a number of ways to remedy this error:

To increase the time Burp Scanner is allocated for static JavaScript analysis, from Audit configuration, change your JavaScript analysis settings to increase the Maximum static analysis time per item.

If you do not want Burp Scanner to perform static JavaScript analysis, then from Audit configuration, under JavaScript analysis, uncheck Use static analysis techniques.

Failed to allocate memory - behavior may be unstable.

Cause

Insufficient memory (RAM) is available for Burp Suite to operate correctly. This means that problems may occur - for example, you may not be able to start Burp's browser.

Remedy

See our tips on how to optimize Burp Suite's memory usage.

Found API definition at location X.

Cause

Burp Scanner's API scanning feature has found an API definition.

Remedy

If you do not want Burp Scanner to parse API definitions, then you can turn off this feature. From Crawl settings, uncheck Parse API definitions.

Skipping location X in API definition because it is out of scope.

Cause

Burp Scanner's API scanning feature has identified an API endpoint that is outside of its scope. Scanning of this endpoint is blocked because it is out of scope. Note that Burp Scanner uses its own scope, which is separate from Burp Suite's Target Scope.

Remedy

If you want Burp Suite to make requests to this endpoint, from the Dashboard tab, click New scan > Webapp scan. From the web application scan launcher, under Scan details, add the endpoint URL to the list of URLs to Scan.

Maximum time exceeded in dynamic code analysis of: X.

Cause

Burp Scanner's dynamic JavaScript analysis feature has reached the maximum time it is allocated for analysis of an individual item.

Remedy

There are a number of ways to remedy this error:

To increase the time Burp Scanner is allocated for dynamic JavaScript analysis, from Audit configuration, change your JavaScript analysis settings to increase the

Maximum dynamic analysis time per item.

If you do not want Burp Scanner to perform dynamic JavaScript analysis, then from Audit configuration, under JavaScript analysis, uncheck Use dynamic analysis techniques.

Your machine specification does not meet the recommended requirements for crawling and auditing using Burp's browser. If you want to try using Burp's browser anyway, open the crawl configuration, go to

Discovery logic > Use Burp's browser for crawl and audit and select Use Burp's

browser.

Cause

Your machine does not have sufficient resources for Burp's browser to operate correctly. You can try using Burp's browser anyway, but problems may occur. For example, the browser may not start.

Remedy

Review Burp Suite's system requirements. You may also find it useful to see our tips on how to optimize Burp Suite's memory usage.

Successfully connected to the configured Collaborator server.

Cause

Burp Suite Professional / Burp Scanner can use Burp Collaborator to perform out-of-band application security testing (OAST). This message indicates that Burp Collaborator was able to connect to its configured server.

To disable Burp Collaborator, or change the server it connects to, go to Project > Collaborator in the

Settings dialog.

Remedy

N/A (Information only)

Audit started.

Cause

Burp Scanner has started the audit phase of the scanning process.

Remedy

N/A (Information only)

Audit finished.

Cause

Burp Scanner has completed the audit phase of the scanning process.

Remedy

N/A (Information only)

Your system is running low on physical memory. You may experience problems using Burp's browser.

Cause

There is not enough RAM available for Burp Suite to operate correctly. This means that problems may occur. For example, you may not be able to start Burp's browser.

Remedy

See our tips on how to optimize Burp Suite's memory usage.

Crawl started.

Cause

Burp Scanner has started the crawl phase of the scanning process.

Remedy

N/A (Information only)

Crawl finished.

Cause

Burp Scanner has completed the crawl phase of the scanning process.

Remedy

N/A (Information only)

Found X new locations after logging in (X).

Cause

Burp Scanner used the login credentials or recorded login sequence you provided and found a number of new locations to scan.

Remedy

N/A (Information only)

No new locations found after logging in (X).

Cause

Burp Scanner used the login credentials or recorded login sequence you provided but did not find any new locations to scan.

Remedy

N/A (Information only)

Task deleted.

Cause

The task was deleted while the scan was running.

Remedy

N/A (Information only)

Unrecoverable error.

Cause

Something went wrong.

Remedy

Contact our Support team, who will assist you.

Scan canceled by REST API, so tasks marked as failed.

Cause

The scan was canceled by a user.

Remedy

N/A (Information only)

Failed to lookup host X while auditing.

Cause

Burp Scanner was unable to audit a location because it could not resolve the hostname. This can be caused by either an incorrect hostname in the URLs provided or a DNS error.

Remedy

Check for typos or other errors in the URLs to Scan. Make sure you can access the host from a browser.

X consecutive audit items have failed.

Cause

An error handling threshold has been exceeded.

Remedy

Look in the event log and follow the remediation steps for the errors shown. Alternatively, increase the threshold for Handling repeated timeouts during audit.

More than X% of audit items have failed.

Cause

An error handling threshold has been exceeded.

Remedy

Look in the event log and follow the remediation steps for the errors shown. Alternatively, increase the threshold for Handling repeated timeouts during audit.

When sending a request to X, Burp Scanner received a warning from the server for sending too many requests in quick succession. Automatically added a X ms delay between requests.

Cause

The server issued a response status code that triggered automatic throttling in Burp Scanner. This can prevent the scan from running properly and is likely to impact coverage.

By default, Burp Scanner incrementally adds a short delay between requests until it complies with the server's rate limit. This enables the scan to continue as normal, but increases the overall duration. You can disable this behavior from your resource pool settings by deselecting Automatic throttling.

Remedy

You don't need to do anything, Burp Scanner attempts to resolve this issue automatically by default.

To prevent this from happening again, you can adjust your resource pool settings to manually set a suitable delay between requests.

If you're scanning one of your own sites in a test environment, where you aren't concerned about impacting the website's performance for other users, you may be able to disable server rate limiting and allow the scan to run at full speed.

Note

Although Burp Scanner attempts to reduce the rate of requests it sends, if the server uses IP-based rate limiting, you may also need to throttle any other automated tools that are sending requests to the server from the same address

The X BCheck didn't run Collaborator checks, as Collaborator has been disabled.

Cause

The BCheck calls Burp Collaborator, but you have disabled Collaborator in Burp. When running the BCheck, Burp Scanner used a random string instead of the Collaborator payload, and didn't poll the Collaborator server.

Remedy

You have the following options:

Continue to use the BCheck without the Collaborator function. The other functions of the BCheck will run.

Enable Burp Collaborator.

Disable the BCheck, or modify it so that it doesn't call Collaborator.

Burp Scanner can't use the confirmation text to confirm authentication because it appears while unauthenticated.

Cause

Burp Scanner found the confirmation text in the response from the URL you specified before running recorded login: X

Remedy

Choose confirmation text that only appears in the response from the URL after authentication. For example, your username or a personalized welcome message.

Recorded login sequence failed to replay

Cause

Burp Scanner was unable to successfully replay the recorded login sequence during the scan.

Remedy

Check the event log for specific error details about the login failure.

Use the Replay function to test your recorded login sequence manually.

Verify that the application's login mechanism is still functional.

Re-record the login sequence if the application has changed.

Burp Scanner can't verify that it's logged in.

Cause

Either the login sequence didn't authenticate successfully, or the confirmation text didn't appear on the page you specified for the following recorded logins: X

Remedy

Use the Replay function to make sure the recorded login successfully authenticates.

If it doesn't authenticate successfully:

Check which actions were successful.

Re-record the login sequence from the last successful action.

If the same step fails again, Burp Scanner may not support the next action.

Burp Scanner errors in Burp Suite DAST

Your start URL X was redirected to X which is out of scope.

Cause

Burp Scanner only visits URLs that are in scope. This protects you from scanning sites that you don't have permission to scan.

Remedy

If you have permission to scan the URL that your start URL was redirected to, you can add it to your scope and run the scan again. For more information, please refer to Setting the site scope.

Note

You may need to add specific subdomains to your scope. For example, https://www.portswigger.net redirects to https://portswigger.net. If you only include https://www.portswigger.net in your scope, the redirect URL will be out of scope.

Could not start browser.

Cause

Burp Scanner could not start Burp's browser due to an unexpected error.

Remedy

First, read our documentation on Burp Suite DAST's system requirements, and check that your system specification is high enough. You may also find it useful to read our reference page on browser-powered scanning.

If you are unable to resolve the issue, contact our Support team, including the following information:

Your Scan Debug Log.

Your Scan Event Log.

Your Support Pack.

Your scanning machine hardware specification, including CPU cores, RAM, operating system (OS) type and version.

The Collaborator server software is out of date. Some Burp features will not work properly with the configured Collaborator server.

Cause

The version of Burp Suite you are using is older than the configured Collaborator server.

Remedy

Upgrade to the latest version of Burp Suite DAST.

Scan stopped. Configured maximum crawl and audit time elapsed.

Cause

The scan cannot be completed within the total scan time specified.

Remedy

If you want your crawl to be more complete, first either create a custom scan configuration or edit an existing custom scan configuration. Under Auditing > Audit strategy, set Total scan time to a higher value. Leave this field blank if you do not want a limit.

Burp's browser could not be started. Using non-browser based navigation.

Cause

Burp Scanner uses Burp's browser to perform browser-powered scanning. This error indicates that something has prevented Burp's browser from starting. There are multiple reasons that this might happen.

Remedy

First, read our documentation on Burp Suite DAST's system requirements, and check that your system specification is high enough. You may also find it useful to read our reference page on browser-powered scanning.

If you are unable to resolve the issue, contact our Support team, including the following information:

Your Scan Debug Log.

Your Scan Event Log.

Your Scanning Machine Log.

Your Support Pack.

Your scanning machine hardware specification, including CPU cores, RAM, operating system (OS) type and version.

Total available memory is only X MB - you should ideally set a larger maximum heap size, for example: X.

Cause

Insufficient memory (RAM) is available for a Burp Suite DAST scanning machine to operate correctly. This means that problems may occur - for example, browser-powered scanning may not work.

Remedy

There are multiple ways to remedy this situation:

Reduce the number of concurrent scans running on the scanning machine, refer to the Assigning scan limits page.

Increase the memory (RAM) available to the scanning machine. For more information, see the Burp Suite DAST's system requirements page.

If you are using a lot of extensions to scan this site, try removing some of them. Note that if you are using extensions downloaded from the BApp Store, an Estimated system impact rating is available from the BApp Store.

Skipping Hidden HTTP/2 scan check because HTTP/2 is disabled.

Cause

You have imported a custom scan configuration that has HTTP/2 disabled. This means that Burp Scanner is not checking for the hidden HTTP/2 vulnerability.

Remedy

To enable HTTP/2 for this scan, create and upload a new custom scan configuration that has HTTP/2 enabled.

Throttling HTTP/2 requests to X due to server concurrent stream limit.

Cause

The server is limiting the number of concurrent requests that can be made to it. Because of this, Burp Suite DAST is throttling the number of concurrent HTTP/2 requests to the server's maximum.

Remedy

N/A (Information only).

Skipping brute force of JWT token as maximum time exceeded.

Cause

JWT tokens use a signature to validate their contents. In some cases, Burp Scanner will attempt to brute-force this signature in order to compromise the token. This error has been caused by Burp Scanner running out of time during the brute-forcing process.

Remedy

To increase the amount of time that Burp Scanner spends brute-forcing JWT token signatures, from the settings menu select Scan configurations and select the scan. From Auditing > Audit strategy set Audit speed to Thorough.

Failed to find additional locations after recorded sequence: X.

Cause

When using a recorded login, Burp Scanner first runs a crawl without using your recorded login. It then compares it to a crawl using your recorded login. If no additional content is discovered, then this error appears.

This can occur for a number of reasons:

Your recorded login has failed.

Your recorded login ends on a page that is out of scope for your scan. Note that Burp Scanner ignores scope while performing a recorded login sequence. However, any out of scope locations are not crawled and / or audited as part of that scan.

Burp Scanner is not finding any additional content, because the selected crawl strategy is not complete enough.

Remedy

If you think your recorded login has failed, then see our documentation on troubleshooting recorded login sequences in Burp Suite DAST.

If your recorded login ends on a page that is out of scope for your scan and you want to adjust your scope to include that page, you can add the page to the list of Include URLs for the site you are scanning.

If you want to try a more complete crawl strategy, create a new scan configuration. Here you can select a Crawl strategy from the Crawl settings.

Blocked out-of-scope request to X.

Cause

Burp Scanner has attempted to make a request that has been blocked, because the target URL is not included in the list of Include URLs for this site.

There are a number of reasons that Burp Scanner might have attempted to make this request - one example is link redirection.

Remedy

If you want Burp Suite DAST to make requests to this URL, add it to the list of Include URLs for the site you are scanning.

Note that any URLs that begin with this URL prefix will also be scanned - unless you add them to the list of Exclude URLs.

Crawl aborted due to too many requests being made.

Cause

Burp Scanner has reached its Maximum request count.

Remedy

Using a custom Scan configuration, change your Crawling setting to allow an increased Maximum request count.

Maximum time exceeded in static code analysis of: X.

Cause

Burp Scanner's static JavaScript analysis feature has reached the maximum time it is allocated for analysis of an individual item.

Remedy

There are a number of ways to remedy this error:

To increase the time Burp Scanner is allocated for static JavaScript analysis, from the settings menu select Scan configurations and select the scan. From JavaScript analysis , increase the Maximum static analysis time per item.

If you do not want Burp Scanner to perform static JavaScript analysis, turn off Use static analysis techniques.

Failed to allocate memory - behavior may be unstable.

Cause

Insufficient memory (RAM) is available for a Burp Suite DAST scanning machine to operate correctly. This means that problems may occur - for example, browser-powered scanning may not work.

Remedy

There are multiple ways to remedy this situation:

If you have Burp extensions installed that you are not using, try removing some.

Increase the memory (RAM) available to the scanning machine. For more information, see the Burp Suite DAST's system requirements page.

Reduce the number of concurrent scans running on the scanning machine. Refer to Assigning scan limits.

Found API definition at location X.

Cause

Burp Scanner's API scanning feature has found an API definition.

Remedy

If you do not want Burp Scanner to parse API definitions, then you can turn off this feature. From the settings menu select Scan configurations and select the scan. From Crawling > Discovery logic, deselect Parse API definitions.

Skipping location X in API definition because it is out of scope.

Cause

Burp Scanner's API scanning feature has identified an API endpoint that is not included in the list of Include URLs for this site. Scanning of this endpoint is blocked.

Remedy

If you want Burp Scanner to make requests to this API endpoint, add it to the list of Include URLs for the site you are scanning.

Note that any URLs which begin with this URL prefix will also be scanned - unless you add them to the list of Exclude URLs.

Maximum time exceeded in dynamic code analysis of: X.

Cause

Burp Scanner's dynamic JavaScript analysis feature has reached the maximum time it is allocated for analysis of an individual item.

Remedy

There are a number of ways to remedy this error:

To increase the time Burp Scanner is allocated for dynamic JavaScript analysis, from the settings menu select Scan configurations and select the scan. Select Auditing > JavaScript analysis and increase the Maximum dynamic analysis time per item.

If you do not want Burp Scanner to perform dynamic JavaScript analysis, turn off Use dynamic analysis techniques.

Your machine specification does not meet the recommended requirements for crawling and auditing using Burp's browser. If you want to try using Burp's browser anyway, open the crawl configuration, go to Discovery logic > Use Burp's browser for crawl and audit and select Use Burp's browser.

Cause

A Burp Suite DAST scanning machine does not have sufficient resources for Burp's browser to operate correctly. This means that problems may occur. For example, browser-powered scanning may not work.

Remedy

Review Burp Suite DAST's system requirements.

Review Browser-powered scanning.

Successfully connected to the configured Collaborator server.

Cause

Burp Scanner can use Burp Collaborator to perform out-of-band application security testing (OAST). This message indicates that Burp Collaborator was able to connect to its configured server.

You can disable Burp Collaborator or change the server it connects to using a custom config file. Contact our Support team for details of how to create this.

Remedy

N/A (Information only)

Audit started.

Cause

Burp Scanner has started the audit phase of the scanning process.

Remedy

N/A (Information only)

Audit finished.

Cause

Burp Scanner has completed the audit phase of the scanning process.

Remedy

N/A (Information only)

Your system is running low on physical memory. You may experience problems using Burp's browser.

Cause

There is not enough RAM available for Burp Suite DAST's scanning machines to operate correctly. This means that problems may occur. For example, browser-powered scanning may not work.

Remedy

There are multiple ways to remedy this situation:

Increase the memory (RAM) available to the scanning machines. For more information, see the Burp Suite DAST's system requirements page.

Reduce the number of concurrent scans running on the scanning machine, refer to the Assigning scan limits page.

Remove any Burp extensions that you are not using.

Crawl started.

Cause

Burp Scanner has started the crawl phase of the scanning process.

Remedy

N/A (Information only)

Crawl finished.

Cause

Burp Scanner has completed the crawl phase of the scanning process.

Remedy

N/A (Information only)

Found X new locations after logging in (X).

Cause

Burp Scanner used the login credentials or recorded login sequence

you provided and found a number of new locations to scan.

Remedy

N/A (Information only)

No new locations found after logging in (X).

Cause

Burp Scanner used the login credentials or recorded login sequence

you provided but did not find any new locations to scan.

Remedy

If you think your recorded login has failed, then see our documentation on troubleshooting recorded login sequences in Burp Suite DAST.

If your recorded login ends on a page that is out of scope for your scan and you want to adjust your scope to include that page, you can add the page to the list of Include URLs for the site you are scanning.

If you want to try a more complete crawl strategy, create a new scan configuration. Here you can select a Crawl strategy from the Crawl settings.

Task deleted.

Cause

The task was deleted while the scan was running.

Remedy

N/A (Information only)

Unrecoverable error.

Cause

Something went wrong.

Remedy

Contact our Support team, including the following information:

Your Scan Debug Log.

Your Scan Event Log.

Your Scanning Machine Log.

Your Support Pack.

Your scanning machine hardware specification, including CPU cores, RAM, operating system (OS) type and version.

Scan canceled by REST API, so tasks marked as failed.

Cause

The scan was canceled by a user.

Remedy

N/A (Information only)

Failed to lookup host X while auditing.

Cause

Burp Scanner was unable to audit a location because it could not resolve the hostname. This can be caused by either an incorrect hostname in the URLs provided or a DNS error.

Remedy

Check for typos or other errors in the URLs to Scan, refer to Site level view.

Make sure that the hostname can be resolved from the scanning machine.

X consecutive audit items have failed.

Cause

An error handling threshold has been exceeded.

Remedy

Look in the event log and follow the remediation steps for the errors shown. Alternatively, increase the threshold for Handling repeated timeouts during audit.

More than X% of audit items have failed.

Cause

An error handling threshold has been exceeded.

Remedy

Look in the event log and follow the remediation steps for the errors shown. Alternatively, increase the threshold for Handling repeated timeouts during audit.

Failed to replay sequence X - X.

Cause

Burp Scanner was unable to replay the recorded login sequence because one of the steps could not be completed. If the sequence has previously replayed successfully, the issue may be caused by changes to the application's login flow or credentials.

Remedy

Run a pre-scan check to identify which step in the login sequence is failing.

Re-record the login sequence.

Run the pre-scan check again to confirm that Burp can now replay the login sequence successfully.

Cannot replay sequence, failed to create a browser.

Cause

Burp Scanner was unable to start Burp's browser that it uses to replay recorded login sequences.

Remedy

Check your system requirements.

Skipping API definition. The data in the definition file is malformed and cannot be read by Burp Scanner.

Cause

Burp Scanner needs to be able to parse an API definition in order to scan it. Currently, this is only possible for definitions that:

Meet the API definition requirements.

Do not contain any external references.

Any definitions that do not meet these requirements will be skipped during the scan.

Remedy

Make sure that the API definition you're trying to scan meets the prerequisites outlined above. For more details, please refer to the documentation for API scanning.

Environment not supported by browser.

Cause

Burp Scanner could not start Burp's browser as it is not supported by the current operating system environment.

Remedy

Check your system requirements.

Could not start Burp's browser sandbox because you are running as root. Either switch to running as an unprivileged user or allow running without sandbox.

Cause

For security reasons, on Linux, Burp's browser runs in sandbox mode by default. When logged in as root, this may prevent the browser from launching properly.

Remedy

You have the following options:

Switch to a different user. We recommend this option wherever possible.

Allow the browser to run without a sandbox. Configure this in the Settings dialog, under Tools > Burp's browser.

Warning

Scanning hostile websites without a sandbox can increase the risk of your local machine being compromised. Before enabling this setting, make sure that you understand the security implications.

Cannot start Burp's browser sandbox because your kernel does not support user namespaces. Please either upgrade your kernel or allow running without sandbox.

Cause

Running Burp's browser in sandbox mode on Linux requires a Kernel that supports User namespaces.

Remedy

Upgrade to a Kernel that supports namespaces.

Cannot start Burp's browser sandbox because the chrome-sandbox binary is not configured correctly and your kernel has user namespace cloning disabled. To enable, run the following command as root: "echo 1 > /proc/sys/kernel/unprivileged_userns_clone"

Cause

Burp Scanner will by default run Burp's browser in sandbox mode. This requires an operating system environment that supports namespace cloning. Sandbox mode is a security feature of Chromium that makes browsing more secure.

Remedy

If you enable namespace cloning Burp's browser can run in sandbox mode. Running the command in the error message will enable namespace cloning until you reboot. You can save this setting in your sysctl.conf file to enable this setting permanently. Please refer to the documentation for your operating system for more details.

Cannot start Burp's browser sandbox because the chrome-sandbox binary is not configured correctly and your kernel has user namespace cloning disabled. To enable, run the following command as root: "echo 0 > /proc/sys/kernel/userns_restrict"

Cause

Burp Scanner will by default run Burp's browser in sandbox mode. This requires an operating system environment that supports namespace cloning. Sandbox mode is a security feature of Chromium that makes browsing more secure.

Remedy

If you enable namespace cloning Burp's browser can run in sandbox mode. Running the command in the error message will enable namespace cloning until you reboot. You can save this setting in your sysctl.conf file to enable this setting permanently. Please refer to the documentation for your operating system for more details.

Cannot handle streaming response: X.

Cause

Burp Scanner does not support streaming responses. It will skip pages that provide a streaming response.

Remedy

N/A (Information only)

The Burp Collaborator server used by the Burp Collaborator client is not reachable, change the settings to use this feature.

Cause

The Burp Collaborator client was unable to connect to the Burp Collaborator server that it uses to perform OAST checks. As a result, these checks were skipped for this scan.

Remedy

Make sure that your network and firewall settings are correct.

Failed to connect to the configured Collaborator server: X.

Cause

Burp Scanner was unable to connect to the selected Burp Collaborator server. As a result, OAST checks were skipped for this scan.

Remedy

Make sure that your network and firewall settings are correct.

Skipping X. Too many consecutive "unknown host" errors have occurred.

Cause

Burp Scanner could not resolve a hostname when making a request during the audit phase. This can be caused by a number of issues, including intermittent network problems, server load, or security measures like Web Application Firewalls.

Remedy

Check your host names and your DNS server settings.

Skipping X. Too many consecutive "request timeout" errors have occurred.

Cause

Burp Scanner identifies insertion points where it can try injecting different payloads. Repeated attempts to insert a payload into the current insertion point or the current page have failed.

Remedy

Experiencing intermittent problems accessing a site is normal and does not necessarily indicate a problem.

The site may have changed. Try rerunning the scan.

Scans may overload servers and the unusual activity may cause Web Application Firewalls to start blocking requests, for example. In this case, change the following settings in New Scan Configuration and rerun the scan:

In Handling repeated timeouts during audit, increase consecutive audit checks fail and/or consecutive insertion points fail.

In Handling repeated timeouts during audit, increase follow-up passes to retry requests that timed out.

In Request throttling, decrease Maximum concurrent requests, enable a Throttle request interval with more retries, decrease concurrent requests, or enable throttling.

Skipping X. Too many consecutive "request aborted" errors have occurred.

Cause

Burp Scanner identifies insertion points where it can try injecting different payloads. Repeated attempts to insert a payload into the current insertion point or the current page have failed.

Remedy

Experiencing intermittent problems accessing a site is normal and does not necessarily indicate a problem.

The site may have changed. Try rerunning the scan.

Scans may overload servers and the unusual activity may cause Web Application Firewalls to start blocking requests, for example. In this case, change the following settings in New Scan Configuration and rerun the scan:

In Handling repeated timeouts during audit, increase consecutive audit checks fail and/or consecutive insertion points fail.

In Handling repeated timeouts during audit, increase follow-up passes to retry requests that timed out.

In Request Throttling, decrease Maximum concurrent requests, enable a Throttle request interval with more retries, decrease concurrent requests, or enable throttling.

Skipping X. Too many consecutive "connection failed" errors have occurred.

Cause

Burp Scanner identifies insertion points where it can try injecting different payloads. Repeated attempts to insert a payload into the current insertion point or the current page have failed.

Remedy

Experiencing intermittent problems accessing a site is normal and does not necessarily indicate a problem.

The site may have changed. Try rerunning the scan.

Scans may overload servers and the unusual activity may cause Web Application Firewalls to start blocking requests, for example. In this case, change the following settings in New Scan Configuration and rerun the scan:

In Handling repeated timeouts during audit, increase consecutive audit checks fail and/or consecutive insertion points fail.

In Handling repeated timeouts during audit, increase follow-up passes to retry requests that timed out.

In Request Throttling, decrease Maximum concurrent requests, enable a Throttle request interval with more retries, decrease concurrent requests, or enable throttling.

Skipping X. Too many consecutive "empty response" errors have occurred.

Cause

Burp Scanner identifies insertion points where it can try injecting different payloads. Repeated attempts to insert a payload into the current insertion point or the current page have failed.

Remedy

Experiencing intermittent problems accessing a site is normal and does not necessarily indicate a problem.

The site may have changed. Try rerunning the scan.

Scans may overload servers and the unusual activity may cause Web Application Firewalls to start blocking requests, for example. In this case, change the following settings in New Scan Configuration and rerun the scan:

In Handling repeated timeouts during audit, increase consecutive audit checks fail and/or consecutive insertion points fail.

In Handling repeated timeouts during audit, increase follow-up passes to retry requests that timed out.

In Request Throttling, decrease Maximum concurrent requests, enable a Throttle request interval with more retries, decrease concurrent requests, or enable throttling.

Skipping X. Too many consecutive "missing link on path to crawled location" errors have occurred.

Cause

Burp Scanner's crawl engine accesses URLs in the same way as a human accessing a website would. It starts at the specified URLs and follows links through a website. A page discovered during the crawl could no longer be found by following links from the specified starting URL due to one of more links no longer being present, although it might still exist on the site.

Remedy

Experiencing intermittent problems accessing a site is normal and does not necessarily indicate a problem.

The site may have changed. Try rerunning the scan.

Scans may overload servers and the unusual activity may cause Web Application Firewalls to start blocking requests, for example. In this case, change the following settings in New Scan Configuration and rerun the scan:

In Handling repeated timeouts during audit, increase consecutive audit checks fail and/or consecutive insertion points fail.

In Handling repeated timeouts during audit, increase follow-up passes to retry requests that timed out.

In Request Throttling, decrease Maximum concurrent requests, enable a Throttle request interval with more retries, decrease concurrent requests, or enable throttling.

Skipping X. Too many consecutive "error on path to crawled location" errors have occurred.

Cause

Burp Scanner's crawl engine accesses URLs in the same way as a human accessing a website would. It starts at the specified URLs and follows links through a website. A page discovered during the crawl could no longer be found by following links from the specified starting URL due to one or more errors when following links, although it might still exist on the site.

Remedy

Experiencing intermittent problems accessing a site is normal and does not necessarily indicate a problem.

The site may have changed. Try rerunning the scan.

Scans may overload servers and the unusual activity may cause Web Application Firewalls to start blocking requests, for example. In this case, change the following settings in New Scan Configuration and rerun the scan:

In Handling repeated timeouts during audit, increase consecutive audit checks fail and/or consecutive insertion points fail.

In Handling repeated timeouts during audit, increase follow-up passes to retry requests that timed out.

In Request Throttling, decrease Maximum concurrent requests, enable a Throttle request interval with more retries, decrease concurrent requests, or enable throttling.

Skipping X. Too many consecutive "missing request at crawled location" errors have occurred.

Cause

Burp Scanner's crawl engine accesses URLs in the same way as a human accessing a website would. It starts at the specified URLs and follows links through a website. A page discovered during the crawl no longer triggered the expected requests when revisited for auditing.

Remedy

Experiencing intermittent problems accessing a site is normal and does not necessarily indicate a problem.

The site may have changed. Try rerunning the scan.

Scans may overload servers and the unusual activity may cause Web Application Firewalls to start blocking requests, for example. In this case, change the following settings in New Scan Configuration and rerun the scan:

In Handling repeated timeouts during audit, increase consecutive audit checks fail and/or consecutive insertion points fail.

In Handling repeated timeouts during audit, increase follow-up passes to retry requests that timed out.

In Request Throttling, decrease Maximum concurrent requests, enable a Throttle request interval with more retries, decrease concurrent requests, or enable throttling.

Skipping X. Too many consecutive "crawled location no longer in scope" errors have occurred.

Cause

Burp Scanner's crawl engine accesses URLs in the same way as a human accessing a website would. It starts at the specified URLs and follows links through a website. A page discovered during the crawl could no longer be found whilst adhering to scope rules, although it might still exist on the site.

Remedy

Experiencing intermittent problems accessing a site is normal and does not necessarily indicate a problem.

The site may have changed. Try rerunning the scan.

Scans may overload servers and the unusual activity may cause Web Application Firewalls to start blocking requests, for example. In this case, change the following settings in New Scan Configuration and rerun the scan:

In Handling repeated timeouts during audit, increase consecutive audit checks fail and/or consecutive insertion points fail.

In Handling repeated timeouts during audit, increase follow-up passes to retry requests that timed out.

In Request Throttling, decrease Maximum concurrent requests, enable a Throttle request interval with more retries, decrease concurrent requests, or enable throttling.

Skipping X. Too many consecutive "insertion point no longer present" errors have occurred.

Cause

Burp Scanner's audit phase cannot find an insertion point identified during the crawl phase. This can happen for a number of reasons and may not represent a problem. Intermittent connection issues can prevent pages from loading properly. Testing a Web Application can put a server under unusual load, leading to pages not loading properly. A Web Application Firewall can detect unusual activity and start blocking requests.

Remedy

Experiencing intermittent problems accessing a site is normal and does not necessarily indicate a problem.

The site may have changed. Try rerunning the scan.

Scans may overload servers and the unusual activity may cause Web Application Firewalls to start blocking requests, for example. In this case, change the following settings in New Scan Configuration and rerun the scan:

In Handling repeated timeouts during audit, increase consecutive audit checks fail and/or consecutive insertion points fail.

In Handling repeated timeouts during audit, increase follow-up passes to retry requests that timed out.

In Request Throttling, decrease Maximum concurrent requests, enable a Throttle request interval with more retries, decrease concurrent requests, or enable throttling.

Skipping X. Too many consecutive "streaming response" errors have occurred.

Cause

Burp Scanner does not support streaming responses. It will skip URLs that provide streaming responses.

Remedy

N/A (Information only)

Skipping X. Too many consecutive "browser crash" errors have occurred.

Cause

Burp's browser crashed while requesting a URL. By default, Burp Scanner attempts to request the URL one more time. Burp's browser crashed again during this follow-up pass.

Remedy

Configure Burp Scanner to make more passes.

If this occurs repeatedly on a single site, try manually navigating to the page from Burp Suite Professional or Community Edition and see if it crashes the browser.

Skipping X. Too many consecutive "browser action failed" errors have occurred.

Cause

Burp's browser crashed while requesting a URL. By default, Burp Scanner attempts to request the URL one more time. Burp's browser crashed again during this follow-up pass.

Remedy

Configure Burp Scanner to make more passes.

If this occurs repeatedly on a single site, try manually navigating to the page from Burp Suite Professional or Community Edition and see if it crashes the browser.

Skipping X. Too many consecutive "replayer error" errors have occurred.

Cause

Burp's browser crashed while requesting a URL. By default, Burp Scanner attempts to request the URL one more time. Burp's browser crashed again during this follow-up pass.

Remedy

Configure Burp Scanner to make more passes.

If this occurs repeatedly on a single site, try manually navigating to the page from Burp Suite Professional or Community Edition and see if it crashes the browser.

Found 0 new locations after logging in.

Cause

Burp Scanner keeps track of whether or not the page shown after logging in is different from the page shown before logging in. In this case, after logging in, the pages available were not significantly different. This does not necessarily mean the login failed, but this is one possible cause.

Remedy

Double-check your application login settings to make sure the provided credentials are correct.

Try using a recorded login sequence if you aren't already. This allows Burp Scanner to handle much more complex login forms, like those featuring iFrames and SSO.

Failed to lookup host X while crawling.

Cause

Burp Scanner was unable to crawl a location because it could not resolve the hostname. This can be caused by either an incorrect hostname in the URLs provided or a DNS error.

Remedy

Check for typos or other errors in the URLs.

X consecutive requests have failed.

Cause

During the crawl phase, the scan fails if more than 10 consecutive requests fail. This prevents the scan from needlessly crawling a site that is currently down, for example.

Remedy

Check that the web application being scanned is still running and accessible.

You can also adjust the number of consecutive failed requests that cause a scan to fail. Create a new scan configuration, select Crawling > Handling repeated timeouts during crawl and adjust the consecutive requests time out value.

More than X percent of requests have failed.

Cause

During the crawl phase, the scan can automatically be paused if more than a certain percentage of requests fail. This prevents the scan from needlessly crawling a site that is currently down, for example.

Remedy

Check that the web application being scanned is still running and accessible.

You can also adjust the percentage of request time outs that cause a scan to fail. Create a new scan configuration, select Crawling > Handling repeated timeouts during crawl and adjust the % of requests time out value.

Could not connect to any start URLs.

Cause

Burp Scanner was unable to send requests to any of the specified URLs. This error can be caused by anything that prevents Burp Scanner from connecting to the URL. This can include timeouts, connection failed errors, and problems resolving hostnames.

Remedy

Check for typos and other errors in the URLs.

Check that you are able to connect to the target application from the machine running the scan.

If you have any trouble doing this, troubleshoot your connection to the hostname that is failing.

Check the firewall, proxy, and DNS server settings for the machine running the scan.

Crawl was configured to use Burp's browser, but a browser could not be started.

Cause

Burp Scanner uses Burp's browser to perform browser-powered scanning. This error indicates that something has prevented Burp's browser from starting. There are a number of things that can cause this issue.

Remedy

Make sure that your system meets Burp Suite DAST's system requirements. You may also find it useful to read our reference page on browser-powered scanning. If you are unable to resolve the issue, contact PortSwigger Technical Support and include the following information:

Your Support Pack.

Your Scanning Machine Logs.

Your scanning machine hardware specification, including CPU cores, RAM, operating system (OS) type and version.

When sending a request to X, Burp Scanner received a warning from the server for sending too many requests in quick succession. Automatically added a X ms delay between requests.

Cause

The server issued a response status code that triggered automatic throttling in Burp Scanner. This can prevent the scan from running properly and is likely to impact coverage.

By default, Burp Scanner incrementally adds a short delay between requests until it complies with the server's rate limit. This enables the scan to continue as normal, but increases its overall duration. You can disable this behavior using a custom scan configuration. To do so, go to Request throttling configuration and deselect Automatic throttling.

Remedy

You don't need to do anything, Burp Scanner attempts to resolve this issue automatically by default.

To prevent this from happening again, you can use a custom scan configuration to manually set a suitable delay between requests. To do this, go to Request throttling configuration > Throttle request interval.

If you're scanning one of your own sites in a test environment, where you aren't concerned about impacting the website's performance for other users, you may be able to disable server rate limiting and allow the scan to run at full speed.

Note

Although Burp Scanner attempts to reduce the rate of requests it sends, if the server uses IP-based rate limiting, you may also need to throttle any other automated tools that are sending requests to the server from the same address

The X BCheck didn't run, as it contains one or more errors.

Cause

The BCheck contains one or more errors.

Remedy

Edit the BCheck to fix the errors. Burp Suite Professional can automatically identify errors in BChecks. To do this:

In Extensions > BChecks, click Import. Select the relevant file.

Select the BCheck, then click Edit to open the BChecks editor.

Click Validate. Burp identifies any errors in the BCheck.

To fix the errors, use the BCheck definition reference documentation.

When sending a request to X, the server responded with a rate-limiting header requesting to wait X seconds.

Cause

The server included a rate-limiting header in a response, explicitly telling Burp Scanner how long to wait before making another request. This is a server-specified rate limiting mechanism.

Remedy

This is normal behavior - Burp Scanner is respecting the server's rate limiting instructions. The scanner will automatically continue after waiting for the specified time.

To use Burp Scanner's own throttling, edit Request Throttling in the scan configuration settings. For more information, see Using custom scan configurations.

Burp Scanner can't verify that the recorded login was successful.

Cause

Burp Scanner cannot find the confirmation text in the response from the URL after running recorded login: X

Remedy

Run a pre-scan check to make sure the recorded login successfully authenticates.

If you haven't already, configure an authentication status check so Burp Scanner can confirm when it's authenticated.

If you've already configured an authentication status check, check that:

The URL is correct.

The confirmation text only appears after authentication.

If the recorded login still fails, re-record it and assign it again.
