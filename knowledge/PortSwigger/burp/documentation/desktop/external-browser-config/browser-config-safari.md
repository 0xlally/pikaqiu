# Configuring Safari to work with Burp Suite

Source: https://portswigger.net/burp/documentation/desktop/external-browser-config/browser-config-safari
Fetched: 2026-06-28T09:15:49.196751+00:00

Support Center

Documentation

Desktop editions

External browser configuration

Safari

ProfessionalCommunity Edition

Configuring Safari to work with Burp Suite

Last updated:

June 18, 2026

Read time:

1 Minute

You need to configure Safari so that you can use it for testing with Burp Suite.

Note

These steps are only necessary if you want to use an external browser for manual testing with Burp. If you prefer, you can just use Burp's browser, which is preconfigured to work with Burp Proxy already. To access Burp's browser, go to the Proxy > Intercept tab, and click Open Browser.

To configure Safari, follow these steps:

In Safari, go to the Safari menu and click Preferences.

Click the Advanced tab and, under Proxies, click the Change Settings button. This will open the network configuration settings for your current network adapter.

In the Proxies tab, check the Web Proxy (HTTP) box and enter your Burp Proxy listener address in the Web Proxy Server field (by default, 127.0.0.1), and your Burp Proxy listener port in the (unlabelled) port field (by default, 8080).

Repeat these steps for the Secure Web Proxy (HTTPS) checkbox.

Ensure the Bypass proxy settings for these Hosts & Domains box is empty.

Click OK and Apply and close the open dialogs.

Next step

Check your browser proxy configuration.
