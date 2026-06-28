# Installing Burp's CA certificate

Source: https://portswigger.net/burp/documentation/desktop/external-browser-config/certificate
Fetched: 2026-06-28T09:15:49.256043+00:00

Support Center

Documentation

Desktop editions

External browser configuration

Installing Burp's CA certificate

ProfessionalCommunity Edition

Installing Burp's CA certificate

Last updated:

June 18, 2026

Read time:

3 Minutes

Note

These steps are only necessary if you want to use an external browser for manual testing with Burp. If you prefer, you can just use Burp's browser, which is preconfigured to work with Burp Proxy already. To access Burp's browser, go to the Proxy > Intercept tab, and click Open Browser.

The process for installing Burp's CA certificate varies depending on which browser you are using. Please select the appropriate link below for detailed information about installing the certificate on your chosen browser.

Installing Burp's CA certificate in Firefox.

Installing Burp's CA certificate in Chrome:

Windows.

Linux.

MacOS.

Installing Burp's CA certificate in Safari.

If you're having trouble downloading Burp's CA certificate, take a look at the troubleshooting page.

When you have done this, you can confirm things are working properly by closing all your browser windows, opening a new browser session, and visiting any HTTPS URL. The browser should not display any security warnings, and the page should load in the normal way (you will need to turn off interception again in the Proxy > Intercept tab if you have re-enabled this).

Installing Burp's CA certificate on a mobile device

Additionally, you may want to install Burp's CA certificate on a mobile device. First, ensure that the mobile device is configured to work with Burp Suite. Use the links below for help on installing the certificate:

iOS device

Android device

Why do I need to install Burp's CA certificate?

One of the key functions of TLS is to authenticate the identity of web servers that your browser communicates with. This authentication process helps to prevent a fraudulent website from masquerading as a legitimate one, for example. It also encrypts the transmitted data and implements integrity checks to protect against man-in-the-middle attacks. In order to intercept the traffic between your browser and destination web server, Burp needs to break this TLS connection. As a result, if you try and access an HTTPS URL while Burp is running, your browser will detect that it is not communicating directly with the authentic web server and will show a security warning.

To prevent this issue, Burp generates its own TLS certificate for each host, signed by its own Certificate Authority (CA). This CA certificate is generated the first time you launch Burp, and stored locally. To use Burp Proxy most effectively with HTTPS websites, you need to install this certificate as a trusted root in your browser's trust store. Burp will then use this CA certificate to create and sign a TLS certificate for each host that you visit, allowing you to browse HTTPS URLs as normal. You can then use Burp to view and edit requests and responses sent over HTTPS, just as you would with any other HTTP messages.

Although this step isn't strictly mandatory, especially if you only want to work with non-HTTPS URLs, we still recommend completing this step. You only need to do it once, and it is required to get the most out of your experience with Burp Suite when using an external browser.

Note

If you install a trusted root certificate in your browser, then an attacker who has the private key for that certificate may be able to man-in-the-middle your TLS connections without obvious detection, even when you are not using an intercepting proxy. To protect against this, Burp generates a unique CA certificate for each installation, and the private key for this certificate is stored on your computer, in a user-specific location. If untrusted people can read local data on your computer, you may not wish to install Burp's CA certificate.

In-browser interface

You can access the Burp Proxy in-browser interface by visiting http://burpsuite with the browser, or by entering the URL of your Proxy listener, for example: http://127.0.0.1:8080.

You can download a copy of your Burp CA certificate.

You can disable the in-browser interface if required, in the Proxy settings.
