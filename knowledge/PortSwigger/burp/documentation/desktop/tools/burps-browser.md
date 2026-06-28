# Burp's browser

Source: https://portswigger.net/burp/documentation/desktop/tools/burps-browser
Fetched: 2026-06-28T09:16:01.823425+00:00

Support Center

Documentation

Desktop editions

Tools

Burp's browser

ProfessionalCommunity Edition

Burp's browser

Last updated:

June 18, 2026

Read time:

2 Minutes

Burp Suite comes with its own browser, which is ready to use for a variety of manual and automated testing purposes.

Manual testing with Burp's browser

Burp's browser is preconfigured to work with the full functionality of Burp Suite right out of the box. All of the necessary proxy listener settings are automatically adjusted for you. This means you can launch Burp for the first time and immediately start testing, even using HTTPS, without performing any additional configuration.

To launch Burp's browser, go to the Proxy > Intercept tab and click Open browser. You can then visit and interact with websites just like you would with any other browser. All in-scope traffic is automatically proxied through Burp. This means that as you browse your target website, you can take advantage of Burp Suite's manual testing features. For example, you can intercept and modify requests using Burp Proxy and study the complete HTTP history from the corresponding tabs. You can then send these requests to other tools, such as Burp Repeater and Burp Intruder, to perform additional testing of interesting items that you encounter.

While you browse, Burp's default live tasks will also passively crawl and audit the locations that you visit. This will automatically populate the site map and report any potential security issues as they are identified.

Read more

Penetration testing workflow

If you prefer, you can still use an external browser for testing. In this case, you just need to perform some additional configuration steps.

Scanning websites with Burp's browser

Burp's browser offers a convenient way to perform manual testing with minimal setup. However, it's even more powerful when integrated into your automated testing workflow through browser-powered scanning with Burp Scanner.

Health check for Burp's browser

If you are experiencing any issues with Burp's browser, you can use the Health check for Burp's browser tool to help diagnose the problem. You can access this tool from Burp's Help menu. The health check runs a series of tests to check whether the browser is working correctly and provides feedback on any issues that arise.
