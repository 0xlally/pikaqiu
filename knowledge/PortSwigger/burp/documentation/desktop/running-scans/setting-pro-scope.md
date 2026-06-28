# Setting the scan scope in Burp Suite Professional

Source: https://portswigger.net/burp/documentation/desktop/running-scans/setting-pro-scope
Fetched: 2026-06-28T09:15:54.279814+00:00

Support Center

Documentation

Desktop editions

Running scans

Setting the scan scope in Burp Suite Professional

Professional

Setting the scan scope in Burp Suite Professional

Last updated:

June 18, 2026

Read time:

3 Minutes

The Scan details section of the scan launcher enables you to define the details of what will be scanned, including the URL from which the scan should start.

URLs to scan

This section is displayed for Crawl and audit and Crawl scan types. You can configure one or more start URLs from which Burp will start the crawl. Burp Scanner follows any links from these URLs into the application. For more information on how Burp Scanner uses start URLs when crawling a site, see the Crawling page of the Scanner documentation.

By default, the scope of the crawl is restricted to the configured URLs, ending with the final directory (if any). For example, if you specify a start URL of https://example.org/myapp/welcome.php, the crawler begins at this URL and crawls content within the path https://example.org/myapp/.

Note

Burp identifies the directory based on the final slash (/) in the URL. For example, if you enter https://example.org/myapp/myfolder, all content within the path https://example.org/myapp/ is considered in-scope. To limit the scope to the myfolder directory, you would need to enter https://example.org/myapp/myfolder/.

You can override the default behavior and provide a different scope configuration by opening the Detailed scope configuration toggle. This enables you to define the scope of the crawl using either URL prefixes or advanced matching rules.

Note

You still need to specify the URLs to scan because these are the starting point for the crawl. The URLs must fall within the defined scope for your project. For more information, see Setting the target scope.

Fragment handling

For scans using Burp's browser, Burp accepts URLs with fragments (#). This enables Burp Scanner to handle client-side routing found in React apps and single-page applications. However, the legacy crawling engine does not support URL fragments. If you disable browser-powered scanning in your scan configuration by deselecting the Crawl settings > Discovery logic > Use Burp's browser for crawl and audit option, you cannot include a fragment in any start URLs.

Protocol settings

To control which protocols are used to scan your URLs, select one of the following options:

Scan using HTTP & HTTPS - When this option is selected, Burp Scanner scans all of your URLs using both HTTP and HTTPS, regardless of whether you explicitly specified a protocol in the list of URLs.

Scan using my specified protocols - When this option is selected, Burp Scanner scans the URLs using the protocols that you specify. For example, if you only include the URL http://example.org, the URL https://example.org is not scanned. Any URLs for which no protocol is specified are still scanned using both HTTP and HTTPS.

Note

If Burp identifies that the content at a given location is the same for both protocols then it only scans that location once, even if you choose to scan using both HTTP and HTTPS.

Advanced scan parameters

This section contains the Run isolated scan setting. Results from isolated scans do not appear in the Target > Site map, Target > Crawl paths, or Dashboard > All issues tabs. It can be useful to isolate a scan if you want to test scan configurations without impacting "live" scan results, for example.

Note

You can view site map and crawl path information for an isolated scan from the Dashboard by selecting the relevant entry from the Tasks list. For more information, see:

Crawl paths

Site map

Items to scan

This section is displayed for the Audit selected items scan type. The URLs of the selected items are listed. Note that the same URL appears more than once if there are multiple requests to the same URL with different parameters.

Where you have a lot of items to scan, it is often useful to consolidate the selected items to improve the efficiency of the scan. Click Consolidate items to display a wizard that enables you to choose to remove certain items:

Duplicate items in the selection (those with matching URL and parameter names).

Out-of-scope items (based on the current suite scope).

Items with no parameters.

Items with specific file extensions.

For each option, Burp shows the number of affected items. Any options that would result in none or all of the items being removed are unavailable.

The consolidation wizard then displays the full list of items that will be scanned. You can double-click any item in the list to view the full request and response. You can also remove any further items that you do not wish to scan manually.
