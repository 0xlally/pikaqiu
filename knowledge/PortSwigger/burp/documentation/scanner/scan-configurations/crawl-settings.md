# Crawl settings

Source: https://portswigger.net/burp/documentation/scanner/scan-configurations/crawl-settings
Fetched: 2026-06-28T09:16:11.182459+00:00

Support Center

Documentation

Scanner

Scan configurations

Crawl settings

DASTProfessional

Crawl settings

Last updated:

June 18, 2026

Read time:

7 Minutes

Burp Scanner offers numerous settings that control how scans behave during the crawl phase. You can select these settings when you create or edit scan configurations in Burp Suite Professional or Burp Suite DAST.

Related pages

Using custom scan configurations (Burp Suite DAST).

Configuration library (Burp Suite Professional).

Crawl behavior

Use these settings to configure how Burp crawls your site to reflect the objectives of the scan and the nature of the target application.

Maximum crawl depth

Specify the maximum number of navigational transitions (clicking links and submitting forms) that the crawler can make from the start URL(s).

Modern applications tend to build navigation into every response, for example in menus and page footers. As such, it is normally possible to reach the vast majority of an application's content and functionality within a small number of hops from the start URL. Fully covering multi-stage processes (such as viewing an item, adding it to a shopping cart, and checking out) requires more hops.

Some applications contain extremely long navigational sequences that don't lead to interesting functionality. For example, a shopping application might have a huge number of product categories, sub-categories, and view filters. To a crawler, this can appear as a very deep nested tree of links, all returning different content. However, there are clearly diminishing returns to crawling deeply into a navigational structure such as this. It's sensible to limit the maximum crawl depth to a smaller number.

Crawl strategy

Real-world applications differ hugely in the way they organize content and navigation, the volatility of their responses, and the extent and complexity of the application state involved.

At one extreme, a largely stateless application may:

Employ a unique and stable URL for each distinct function.

Return deterministic content in each response.

Contain no server-side state.

On the other hand, a heavily-stateful application might use:

Ephemeral URLs that change each time a function is accessed.

Overloaded URLs that reach different functions through different navigational paths.

Volatile content that changes non-deterministically.

Functions where user actions cause changes in content and subsequent behavior.

The crawler can handle all of these cases. However, this imposes an overhead in the quantity of work involved in the crawl. The crawl strategy setting enables you to tune the approach taken to specific applications.

The default crawl strategy represents a trade-off between speed and coverage that is appropriate for typical applications. However, when you crawl an application with more stable URLs and no stateful functionality, you may want to select the Faster or Fastest setting. When you crawl an application with more volatile URLs or more complex stateful functionality, you may want to select the More complete or Most complete setting.

Related pages

Crawling: Core approach.

Crawling: Volatile content.

Crawling: Detecting changes in application state.

The Fastest crawl strategy differs from the other crawl strategies in some important ways:

Burp Scanner does not try to reset and reproduce the target application's state. It requests pages directly instead of navigating a path from the root directory.

Burp Scanner uses cookies from the cookie jar as initial values. This has a significant impact on authenticated crawling:

To perform an authenticated crawl, authenticate with the application using Burp's browser before crawling.

If you don't want to run an authenticated crawl, log out of the application before crawling.

Burp Scanner does not attempt to register a new user.

Burp Scanner attempts to authenticate when it discovers potential login forms, rather than in a separate phase. If you supply multiple sets of login credentials, only the first set is used.

Crawl limits

Crawling modern applications is sometimes an open-ended exercise due to stateful functionality, volatile content, and unbounded navigation. It's sensible to configure a limit to the extent of the crawl, based on your knowledge of the application being scanned. Burp Scanner uses various techniques to maximize discovery of unique content early in the crawl, to help minimize the impact of limiting the crawl length.

You can limit the crawl based on:

Time elapsed.

The number of unique locations discovered. A location represents a distinct unit of content or functionality, based on the selected crawl strategy.

The number of HTTP requests made.

Crawl network timeouts

These settings enable you to specify timeout values for the crawl. These values override any you may have configured in the global settings.

Handling repeated timeouts during crawl

These settings control how Burp Scanner responds to repeated request timeouts during the crawl phase of the scan, such as connection failures or transmission timeouts.

You can configure the following options:

The number of consecutive timed out requests before pausing the task.

The overall percentage of timed out requests before pausing the task.

The number of follow-up passes that the crawler performs once the crawl is complete, to retry requests that timed out.

You can leave any setting blank to deselect it.

Related pages

Handling application errors.

Login behavior

Use these settings to configure how Burp handles authentication when crawling your site.

Authenticated crawl only

Choose whether Burp skips the unauthenticated crawl and uses only the provided credentials. Burp doesn't attempt to self-register users or trigger login failures. This can reduce the overall crawl time.

If you don't set login credentials, Burp runs an unauthenticated crawl instead.

If you set credentials but don't enable this setting, Burp crawls the site both logged out and logged in. In some cases, this means the authenticated crawl may not find much extra content.

Testing login functions

These settings control how the crawler interacts with login functionality during the unauthenticated phase of the crawl.

Note

These settings are not compatible with recorded login sequences. When using recorded logins for a scan, the Testing login functions settings are ignored.

You can select whether the crawler should:

Attempt to self-register a new user on the target website. This removes the need to manually set up a user account before the crawl. You can still provide valid application logins in the scan launcher settings.

Use invalid usernames to deliberately trigger login failures. This enables you to reach account recovery features that can normally only be accessed when a user submits invalid credentials. Burp Scanner does not deliberately submit an invalid password for any of the usernames that you provide as application logins. This is to avoid triggering any account locking features on these accounts.

Related pages

Identifying login and registration forms.

Login credentials.

Recording login sequences.

API crawling

These settings enable you to configure how Burp detects and explores APIs when crawling your site:

Parse API definitions - Controls whether Burp Scanner attempts to parse any API definitions it encounters to identify potential endpoints to scan. For more information, please refer to the API scanning documentation.

Parse SOAP WSDL definitions - Controls whether Burp Scanner parses any SOAP WSDL files it finds when crawling to identify SOAP operations and endpoints to include in the scan.

Perform GraphQL introspection - Controls whether Burp Scanner runs introspection queries on any GraphQL endpoints it finds when crawling.

Test common GraphQL endpoints - Controls whether Burp Scanner attempts to guess GraphQL endpoints using a list of common endpoint suffixes. This setting is only available if Perform GraphQL introspection is selected. Note that Burp Scanner does not attempt to guess GraphQL endpoints if it has already found a GraphQL endpoint during the crawl.

Browser behavior

These settings enable you to control the behavior of Burp's browser:

Use Burp's browser for Crawl and Audit - This setting controls whether Burp Scanner uses Burp's browser to navigate the target site. This is known as browser-powered scanning. By default, Burp Scanner only uses Burp's browser if your machine appears to meet the required spec for browser-powered scanning. This setting enables you to force Burp Scanner to use the browser, or to disable browser-powered scanning completely. If browser-powered scanning is disabled, scans use the legacy crawling engine.

Customize User-Agent header - Enables you to specify a custom User-Agent header.

Fetch required resources and data from out-of-scope hosts - This setting controls whether Burp Scanner issues requests to out-of-scope hosts where necessary. Websites often require the browser to load externally hosted subresources or fetch data from an API to function correctly. Allow these requests to help maximize the coverage of your scans. Out-of-scope requests are not audited.

Read timeout for site resources - This setting determines how long the crawler waits in milliseconds when it attempts to load subresources during the crawl.

Note

If you watch the crawl in a headed browser, you may see the crawler open multiple windows and stop using existing ones. This is expected behavior and is not indicative of any issues with the scan. Any redundant windows close automatically after a certain period of time.

Discovery logic

These settings enable you to customize how Burp discovers and interacts with different types of content during the crawl:

Submit forms - Controls whether Burp Scanner submits forms during the crawl.

Request robots file - Controls whether Burp Scanner should fetch the target's robots.txt file and extract links from it.

Request site map - Controls whether Burp Scanner should fetch the target's sitemap.xml file and extract links from it. You can configure the maximum number of items to extract.

Follow hidden links in comments and JavaScript - Controls whether to parse HTML comments and JavaScript for URLs that are not visible within the page navigation. You can configure the maximum number of items to extract.

Click all pointer clickable elements - This setting controls whether Burp Scanner clicks all elements that are styled with a pointer cursor, for example, elements using cursor: pointer.

This can help identify interactive elements that are not standard links or buttons. Depending on the structure and styling of the target application, enabling this setting may increase total scan time.

Application uses fragments for routing - Single-page applications (SPAs) often use URL fragments for client-side routing. This enables them to display what appear to be several distinct pages, without the browser making additional requests to the server. Burp Scanner needs to know whether the target application uses fragments in this way to crawl it effectively. By default, if a fragment contains any of the following characters, Burp Scanner assumes that it is used for client-side routing: / \ ? = &. However, you can use this setting to control this function manually.
