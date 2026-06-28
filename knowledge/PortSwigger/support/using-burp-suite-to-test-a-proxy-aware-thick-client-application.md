# Using Burp Suite to Test a Proxy-Aware Thick Client Application

Source: https://portswigger.net/support/using-burp-suite-to-test-a-proxy-aware-thick-client-application
Fetched: 2026-06-28T09:17:35.659421+00:00

This page may be out of date

We haven't updated it for a while because we're busy working on new, improved content to help you get the

most out of Burp Suite. In the meantime, please note that the information on this page may no longer be

accurate.

Visit our Support Center

Using Burp Suite to Test a Proxy-Aware Thick Client Application

A thick client (or fat client) is a client in client–server relationship. It provides rich functionality, independent of the server, the major processing is done at the client side and can involve only sporadic connections to the server.

In this tutorial we demonstrate the process of configuring a proxy-aware thick client application for testing with Burp Suite.

Note: Often, thick clients don't support HTTP proxies, or don't provide an easy way to configure them to use one. Burp's support for invisible proxying allows non-proxy-aware clients to connect directly to a Proxy listener.

In some cases a thick client will respect the proxy settings of the system you are using to run Burp Suite.

You can test whether or not this is the case my configuring your system to use Burp Suite as proxy.

With Burp running and your system proxy settings configured, browse the application's functionality.

If the client application uses HTTP/S for its communications with the server and it honors the configured proxy settings then the traffic will pass through Burp Suite in the normal way.

You can then test the application using your normal testing methodology.

Note: In some cases restarting the application was necessary to ensure that the proxy settings of the system are respected.
