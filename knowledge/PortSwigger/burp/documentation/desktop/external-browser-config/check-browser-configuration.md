# Checking your browser proxy configuration

Source: https://portswigger.net/burp/documentation/desktop/external-browser-config/check-browser-configuration
Fetched: 2026-06-28T09:15:50.240793+00:00

Support Center

Documentation

Desktop editions

External browser configuration

Check your browser configuration

ProfessionalCommunity Edition

Checking your browser proxy configuration

Last updated:

June 18, 2026

Read time:

1 Minute

Follow the steps below to check your browser proxy configuration.

Note

These steps are only necessary if you want to use an external browser for manual testing with Burp. If you prefer, you can just use Burp's browser, which is preconfigured to work with Burp Proxy already. To access Burp's browser, go to the Proxy > Intercept tab, and click Open Browser.

Make sure you have checked that the proxy listener is active and have configured your chosen browser.

In Burp Suite, go to the Proxy > Intercept tab. To activate HTTP interception, click Intercept is off.

With Burp Suite running, open the browser that you configured and go to any HTTP URL. Your browser should sit waiting for the request to complete, because Burp Suite has intercepted the HTTP request that your browser is trying to send.

In Burp Suite, go to the Proxy > Intercept tab. On the Intercept tab, the intercepted HTTP request displays in the main panel.

Click Forward to release the request from Burp Suite.

Go back to your browser. You should now see the requested page loading as it would during normal browsing.

To deactivate HTTP interception, click Intercept is on.

These steps enable you to test web applications that use HTTP. To test HTTPS URLs, you need to install Burp's CA certificate.

Next step

Install Burp's CA certificate.
