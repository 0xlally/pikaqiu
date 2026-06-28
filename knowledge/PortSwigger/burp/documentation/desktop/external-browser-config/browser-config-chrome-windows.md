# Configuring Chrome to work with Burp Suite - Windows

Source: https://portswigger.net/burp/documentation/desktop/external-browser-config/browser-config-chrome-windows
Fetched: 2026-06-28T09:15:49.083227+00:00

Support Center

Documentation

Desktop editions

External browser configuration

Configuring Chrome to work with Burp Suite - Windows

ProfessionalCommunity Edition

Configuring Chrome to work with Burp Suite - Windows

Last updated:

June 18, 2026

Read time:

1 Minute

If you want to use Chrome with Burp Suite, you need to configure the proxy settings.

Note

These steps are only necessary if you want to use an external browser for manual testing with Burp. If you prefer, you can just use Burp's browser, which is preconfigured to work with Burp Proxy already. To access Burp's browser, go to the Proxy > Intercept tab, and click Open Browser.

To configure Chrome to work with Burp Suite, follow these steps:

Open Chrome and go to the Customize (hamburger) menu.

Select Settings and open the System menu.

Click Open your computer's proxy settings. The Proxy Settings window enables you to set up the proxy server.

Make sure that Automatically detect settings and Use setup script are Off.

Set Use a proxy server to On.

Enter your Burp Proxy listener address in the Address field (by default, 127.0.0.1).

Enter your Burp Proxy listener port in the Port field (by default, 8080).

Make sure that Don't use the proxy server for local (intranet) addresses is unchecked.

Click Save.

Next step

Check your browser proxy configuration.
