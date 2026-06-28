# Having trouble downloading Burp's CA certificate?

Source: https://portswigger.net/burp/documentation/desktop/external-browser-config/certificate/proxy-troubleshooting
Fetched: 2026-06-28T09:15:49.951246+00:00

Support Center

Documentation

Desktop editions

External browser configuration

Installing Burp's CA certificate

Troubleshooting

ProfessionalCommunity Edition

Having trouble downloading Burp's CA certificate?

Last updated:

June 18, 2026

Read time:

2 Minutes

In order to access http://burpsuite and download the CA certificate, your browser needs to be sending traffic through Burp's proxy listener. If you haven't already done so, you need to complete the steps to configure your browser to work with Burp.

If you did this already and were redirected to this page when you tried to access http://burpsuite, something has gone wrong with your proxy settings. But don't worry, it should be easy to fix. Please try the following common solutions:

Check that Burp is running

To access http://burpsuite, Burp needs to be running. Either restart Burp completely or open it if you haven't already.

Check your proxy listener is active

In Burp, go to the Tools > Proxy tab in the Settings dialog. In the Proxy Listeners panel, you should see an entry for the interface 127.0.0.1:8080 with the Running checkbox selected. If not, click the icon in the panel and then Restore defaults.

If the proxy listener is still not running, you might need to try using a different port.

Try a different port

By default, Burp's proxy listener uses port 8080. If you tried both of the previous steps and the proxy listener is still not running, port 8080 might not be available, for example, because it is already being used by another application. To try using a different port:

Identify a different port that you know is free.

In Burp, go to the Tools > Proxy tab in the Settings dialog.

In the Proxy Listeners panel, select the entry for 127.0.0.1:8080 and click the Edit button. The Edit proxy listener dialog opens.

In the Bind to port field, enter the number for the new port and click OK.

Try to activate the listener by selecting the Running checkbox. If you can activate it, great. You should now be able to access http://burpsuite.

If clicking the checkbox doesn't activate the listener, the new port you entered is probably also blocked, so you'll need to try another one.

For more information, please refer to our documentation on Burp Proxy settings.

What next?

If you're still being redirected to this page after trying all of the above, please feel free to get in touch with our technical support team. You can contact us in various ways from our Support page.
