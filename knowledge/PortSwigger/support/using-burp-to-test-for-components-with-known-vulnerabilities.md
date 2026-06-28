# Using Burp to Test for Components with Known Vulnerabilities

Source: https://portswigger.net/support/using-burp-to-test-for-components-with-known-vulnerabilities
Fetched: 2026-06-28T09:17:36.726085+00:00

This page may be out of date

We haven't updated it for a while because we're busy working on new, improved content to help you get the

most out of Burp Suite. In the meantime, please note that the information on this page may no longer be

accurate.

Visit our Support Center

Using Burp to Test for Components with Known Vulnerabilities

To determine whether your application is vulnerable it is important to keep abreast of the security status of the components that it uses. Vulnerabilities are reported to central clearing houses such as CVE and NVD.

Attackers are able to identify a weak component through scanning or manual analysis of a web application. You can simulate this process using Burp. In this example we assess one potential vulnerability of a web server.

First, ensure that Burp is correctly configured with your browser.

Ensure Burp Proxy "Intercept is off".

Visit the web application you are testing in your browser.

Next, click the “HTTP history” tab.

In the HTTP history table select one of the captured request and response rows.

Click the “Response” tab.

Information regarding the web server used by the web application is provided in the response.

From either the “Raw” or “Headers” tab, make a note or copy the Server name and version number.

With the server information at your disposal you can now use a search engine or one of the central clearing houses to check whether your web server has any known vulnerabilities.

Vulnerable components are usually fixed in a later version of the software. Upgrading or patching any components used by your web application is critical when securing your applications.

Additionally, it is possible to use the "Software Version Reporter" from the BApp store to passively scan for server software version numbers.

Related articles:

What is Burp Proxy?

Scanning websites with Burp Scanner
