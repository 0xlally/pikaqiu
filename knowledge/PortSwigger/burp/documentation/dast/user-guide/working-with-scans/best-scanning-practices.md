# Best practices for scanning

Source: https://portswigger.net/burp/documentation/dast/user-guide/working-with-scans/best-scanning-practices
Fetched: 2026-06-28T09:15:44.411604+00:00

DAST

Best practices for scanning

Last updated:

June 18, 2026

Read time:

4 Minutes

Cloud

Self-hosted

Burp Suite DAST provides preset scan configurations for easy setup. These work for most cases, but some applications may need to use custom scan configurations, depending on the framework or complexity. Save custom configurations with a clear name that reflects their purpose.

To edit scan configurations, go to the settings menu and select Scan configurations.

Configurations by use case

You can adjust the scan configurations to suit certain use cases.

Single-page applications (SPAs)

Burp Scanner supports modern web applications, including SPAs. Because SPAs load content dynamically, they may need a custom scan configuration.

For all SPAs, we recommend you set Crawling > Crawl strategy to Most complete.

For SPAs that use fragments (#), also set Crawling > Discovery logic > Application uses fragments for routing to Yes.

Configurations for coverage

If coverage is your priority, choose Balanced or Deep preset scan configurations. The best choice depends on your needs and scan types.

Static modern web applications

For static, modern web apps, select a preset configuration based on scan frequency: Lightweight, Fast, Balanced, or Deep.

You may want to run regular lightweight scans, and schedule a deeper scan to run monthly.

Static legacy web applications (no JavaScript)

For legacy web apps with little or no JavaScript and simple authentication:

Set Crawling > Crawl strategy to Fastest.

Activate the toggle for Embedded Browser > Stop the embedded browser using the GPU.

This speeds up scanning by skipping unnecessary front-end content.

Adjusting scan duration

The settings described so far have a crawl duration of 2 hours 30 minutes.

However, scan times vary based on application size and insertion points.

To reduce scan time, adjust Crawling > Crawl limits > Maximum crawl time.

Different applications may take longer even with the same settings. This depends on the number of audit items.

Scope considerations

Scope settings control which URLs Burp Scanner can crawl and audit. Only in-scope URLs are scanned.

If you are scanning an app with a backend API (such as an SPA), add the API host to the scope. For simple cases, use URL prefixes (Basic mode). For more complex scenarios, such as matching specific paths or port ranges, use regex patterns (Advanced mode). For more information, see setting the site scope.

Start URL

The scanner begins crawling here. The start URL also defines the default in-scope URL, and URLs that are out of scope. For example:

Start URL: https://mydomain.com/app1/home

The scanner can crawl: https://mydomain.com/app1/

The scanner cannot crawl: https://mydomain.com/app2/page

In-scope URL prefixes

These define the URLs that Burp Scanner can crawl and audit. You can use these to define specific areas of your web app that you want to scan. This can also help to reduce scan times.

Out-of-scope URL prefixes

These define the URLs that Burp Scanner is not allowed to crawl or audit.

If your app contains sensitive areas that you don't want to scan, add them to your Out-of-scope URL prefixes.

Large web applications

For large applications, divide scans into separate sites using In-scope and Out-of-scope settings.

For example:

Site 1 (product catalog)

In-scope:

https://ginandjuice.shop/catalog

Out-of-scope:

https://ginandjuice.shop/blog

https://ginandjuice.shop/about

https://ginandjuice.shop/login

https://ginandjuice.shop/my-account

Site 2 (blog)

In-scope:

https://ginandjuice.shop/blog

Out-of-scope:

https://ginandjuice.shop/catalog

https://ginandjuice.shop/about

https://ginandjuice.shop/login

https://ginandjuice.shop/my-account

Repeat this approach as needed, based on site size and how you want to process the scan results.

Authentication

Make sure you configure authentication correctly, to make sure scans complete successfully and provide sufficient coverage.

Basic login forms

For single-step HTML login forms that do not redirect to out-of-scope domains (for example, SSO), use standard login credentials.

Recorded login sequences

For SSO and complex authentication flows, use recorded login sequences. For more information, see:

Recording login sequences

Best practice for recorded logins

Adding recorded login sequences

How to troubleshoot recorded logins

Burp's browser replays login actions multiple times during a scan. This can slow scanning. To minimize the impact of this, don't include unnecessary steps in the sequence.

To speed up scanning:

Use static authentication headers or cookies if possible.

Make sure user accounts allow multiple concurrent logins.

Validating recorded logins

To validate a recorded login:

Click Pre-scan check at the top of the Site page.

Expand the results and go to the Recorded logins tab.

Select Review replay.

Note

The recorded login process ignores the scope. If some of the URLs for the recorded login are shown as out-of-scope, you can ignore the message.

Multi-factor authentication (MFA)

MFA is designed to prevent automated attacks, and that also makes it difficult to integrate into a scanner.

For best results use a dedicated account that does not require MFA, or uses a fixed code.

For case-specific guidance, please email our support team.

Platform (HTTP) authentication

Authentication methods such as Basic and NTLM v1/v2 need to be handled separately from a recorded login or basic credentials. These occur at the network level, outside the browser.

Rate limiting

If the target site enforces rate limits, you can configure request throttling: Settings > Scan configurations > New configuration (or edit existing) > Request throttling.
