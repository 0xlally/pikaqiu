# Using Burp with Selenium

Source: https://portswigger.net/support/using-burp-with-selenium
Fetched: 2026-06-28T09:17:37.341727+00:00

This page may be out of date

We haven't updated it for a while because we're busy working on new, improved content to help you get the

most out of Burp Suite. In the meantime, please note that the information on this page may no longer be

accurate.

Visit our Support Center

Using Burp with Selenium

Selenium is a portable tool for automating browsers in the testing of web applications. You can use Burp Suite to check for vulnerabilities in the run of Selenium tests. This article demonstrates how to proxy Selenium test traffic through Burp Suite and how to passively and actively scan the traffic for vulnerabilities.

There are two ways to ensure that traffic from your Selenium tests proxies via Burp Suite.

Firstly, you can configure the Selenium driver to proxy via your instance of Burp Suite.

Or secondly, you can configure your proxy at the OS level.

When you configure the browser associated with the Selenium tests to use Burp, the proxy settings will be respected and traffic from the tests will pass through Burp Suite.

Before running your Selenium tests, go to the "Proxy Intercept" tab, and ensure that interception is off (if the button says “Intercept is on" then click it to toggle the interception status).

With your proxy configuration set, run your Selenium tests in the normal manner.

Traffic from the tests will now be captured in Burp Suite.

While the Selenium tests are running, Burp will passively report various issues that it observes.

After the Selenium tests have run, you can then carry out active scanning on the captured requests.

For example, you can select everything in the Proxy history and choose "Do an active scan" from the context menu.

Related articles

What is Burp Proxy?

Using Burp Scanner

Using Burp as a point-and-click scanner
