# Check that Burp's proxy listener is active

Source: https://portswigger.net/burp/documentation/desktop/external-browser-config/check-listener
Fetched: 2026-06-28T09:15:52.444493+00:00

Support Center

Documentation

Desktop editions

External browser configuration

Check proxy listener is active

ProfessionalCommunity Edition

Check that Burp's proxy listener is active

Last updated:

June 18, 2026

Read time:

2 Minutes

Burp's proxy listener is a local HTTP proxy server that listens for incoming connections from your browser. It allows you to monitor and intercept all HTTP requests and responses sent and received by your browser. This lies at the heart of Burp's user-driven workflow.

By default, Burp creates a single listener on port 8080 of the loopback interface. The first time you start Burp, you need to check that this listener is active and running.

In Burp, go to the Tools > Proxy tab in the Settings dialog.

In the Proxy listeners panel, you should see an entry for the interface 127.0.0.1:8080 with the Running checkbox selected, indicating that the listener is active and running. If so, everything is fine and you can move on to configuring your browser.

If not, click the icon in the Proxy listeners field and select Restore defaults. Look at the Running checkbox again to see if the proxy listener is now running. If the checkbox is now selected, the listener is active. Otherwise, continue with the following steps.

If it is still not running, the default port 8080 might not be available, for example, because it is already being used by another application. In this case, you need to try using a different port. Select the entry 127.0.0.1:8080 and click the Edit button. The Edit proxy listener dialog opens.

In the Bind to port field, enter the number of a new port that you think is free and click OK.

Try to activate the listener by selecting the Running checkbox. If you still can't activate it, then the new port that you selected is probably also blocked. Repeat this process to try a different port.
