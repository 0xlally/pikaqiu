# Scanning single-page apps

Source: https://portswigger.net/burp/documentation/scanner/scanning-spas
Fetched: 2026-06-28T09:16:11.441388+00:00

Support Center

Documentation

Scanner

Scanning single-page apps

DASTProfessional

Scanning single-page apps

Last updated:

June 18, 2026

Read time:

2 Minutes

Burp Scanner can handle virtually all types of modern web application, including single-page applications (SPAs). The dynamic nature of SPAs means that you may need to use a custom configuration in order to scan them accurately.

Configuring scans of SPAs

To configure SPA scans, you will need to create a custom scan configuration. You can then apply this configuration to your SPA sites (in Burp Suite DAST) or select it when launching a scan of an SPA (in Burp Suite Professional).

More information

For more information on creating custom scan configurations, see:

Using custom scan configurations (Burp Suite DAST).

Configuring scans (Burp Suite Professional).

When you create a scan configuration to use with SPAs, consider the following:

Crawl strategy

If the scan's coverage is not as expected, change the crawl strategy to More Complete. If this does not have an effect, change it to Most complete. The Most complete crawl strategy is best suited for SPAs but significantly increases crawl time.

We do not recommend the Fastest crawl strategy to scan SPAs, as this configuration is only suitable for static sites without any stateful functionality. Also, the Fastest crawl strategy does not support links that require the scanner to click (for example, anything that uses onClick or element.addEventListener('click', fn)).

You can use the Crawling > Crawl strategy scan configuration setting to change the crawl strategy.

Routing fragments

SPAs often use URL fragments for client-side routing. This enables them to display what appear to be several distinct pages without the browser making additional requests to the server. Burp Scanner needs to know whether the target application uses fragments in this way in order to crawl it effectively. By default, if a fragment contains any of the following characters, the crawler assumes that it is used for client-side routing: / \ ? = &.

If an app that uses fragments for client-side routing does not perform as expected, make sure that the Crawling > Discovery logic > Application uses fragments for routing scan configuration option is selected.

Non-standard clickable elements

If the app uses non-standard clickable elements, select the Discovery logic > Click all clickable elements scan configuration setting.

Note

We continually look to improve our crawl coverage. If you encounter an application you think we should be better at scanning, and can provide us with access to the application and permission to scan it, we would be happy to test it remotely in our environment.

Related pages:

Crawl settings.

Audit settings.
