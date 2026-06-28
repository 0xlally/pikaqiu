# Configuring Firefox to work with Burp Suite

Source: https://portswigger.net/burp/documentation/desktop/external-browser-config/browser-config-firefox
Fetched: 2026-06-28T09:15:49.102850+00:00

Support Center

Documentation

Desktop editions

External browser configuration

Firefox

ProfessionalCommunity Edition

Configuring Firefox to work with Burp Suite

Last updated:

June 18, 2026

Read time:

1 Minute

You need to configure Firefox so that you can use it for testing with Burp Suite.

Note

These steps are only necessary if you want to use an external browser for manual testing with Burp. If you prefer, you can just use Burp's browser, which is preconfigured to work with Burp Proxy already. To access Burp's browser, go to the Proxy > Intercept tab, and click Open Browser.

To configure Firefox, follow these steps:

In Firefox, go to the Firefox Menu and select Preferences > Options.

Select the General tab and scroll to the Network Proxy settings. Click the Settings button.

Select the Manual proxy configuration option.

Enter your Burp Proxy listener address in the HTTP Proxy field (by default this is set to 127.0.0.1).

Enter your Burp Proxy listener port in the Port field (by default, 8080). Make sure the Use this proxy server for all protocols box is checked.

Delete anything that appears in the No proxy for field. Click OK to close all the options dialogs.

Next step

Check your browser proxy configuration.
