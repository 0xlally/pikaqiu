# Professional / Community 2020.7

Source: https://portswigger.net/burp/releases/professional-community-2020-7
Fetched: 2026-06-28T09:16:33.687564+00:00

In this release, we've greatly improved the usability of Burp Suite by removing the need to perform many of the initial configuration steps for Burp Proxy.

Use Burp's preconfigured browser for testing

You can now use Burp's embedded Chromium browser for manual testing. This browser is preconfigured to work with the full functionality of Burp Suite right out of the box. You no longer need to manually configure your browser's proxy settings or install Burp's CA certificate. The first time you launch Burp you can immediately start testing, even with HTTPS URLs.

To launch the embedded browser, go to the "Proxy" > "Intercept" tab and click "Open Browser".

Note that if you want to use an external browser for testing. you can still configure any browser to work with Burp in the same way as you could before.

Other improvements

Burp now provides feedback in the request and response when it successfully communicates using HTTP/2. The first request you send to a server will display HTTP/1. However, once Burp has established that the website supports HTTP/2, all subsequent messages will indicate this in the request line and status line respectively. For more information about Burp's experimental HTTP/2 support, please refer to the documentation.

Performance of the experimental browser-powered scanning feature has been improved.

The embedded browser has been upgraded to Chromium 84.

Bug fixes

Multiple Cookie headers are now displayed correctly in the "Params" tab.

We have also fixed a security bug that was reported via our bug bounty program. With a significant amount of user interaction, an attacker could potentially steal comma-delimited files from the local filesystem. The attacker would have to induce a user to visit a malicious website, copy the request as a curl command, and then execute it via the command line.
