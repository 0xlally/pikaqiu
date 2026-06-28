# Using Burp's Invisible Proxy Settings to Test a Non-Proxy-Aware Thick Client Application

Source: https://portswigger.net/support/using-burp-suites-invisible-proxy-settings-to-test-a-non-proxy-aware-thick-client-application
Fetched: 2026-06-28T09:17:35.970942+00:00

This page may be out of date

We haven't updated it for a while because we're busy working on new, improved content to help you get the

most out of Burp Suite. In the meantime, please note that the information on this page may no longer be

accurate.

Visit our Support Center

Using Burp's Invisible Proxy Settings to Test a Non-Proxy-Aware Thick Client Application

In some cases a thick client application will respect the proxy settings of the system you are using to run Burp Suite. However, it is often the case that these clients don't support HTTP proxies, or don't provide an easy way to configure them to use one.

Burp's support for invisible proxying allows non-proxy-aware clients to connect directly to a Proxy listener. This option is sometimes useful when testing a desktop application, a thick client component that runs outside of the browser, a browser plugin that makes its own HTTP requests outside of the browser's framework, or if you do not wish to change your system proxy settings.

Redirecting Inbound Requests

You can effectively force the non-proxy-aware client to connect to Burp by modifying your DNS resolution to redirect the relevant hostname, and setting up invisible Proxy listeners on the port(s) used by the application. For example:

127.0.0.1 example.org

If it is not possible to modify your DNS resolution, you need to use DNAT to rewrite the destination address at the IP layer.

In some cases a thick client will respect the proxy settings of the system you are using to run Burp Suite.

You can test whether or not this is the case my configuring your system to use Burp Suite as a proxy.

Configuring Invisible Proxy Mode

To receive the redirected requests, you also need to create invisible Burp Proxy Listeners on the appropriate interface/s.

You can configure Burp's Proxy Listeners in Proxy > Options > Proxy Listeners.

In this example:

127.0.0.1:443

Go to Request handling in the Proxy listener window, fill in the appropriate host and port information and ensure invisible proxying is enabled.

In this example, all the invisibly proxied traffic is headed for a single domain. We can you can use the Proxy listener's redirection options to force the outgoing traffic to go to the correct IP address.

If the proxied traffic is headed for multiple domains, you can use Burp's own hostname resolution options (Project options > Connections > Hostname Resolution) to override the hosts file and redirect each domain individually back to its correct original IP address.

You can check that the thick client traffic is proxying via Burp in the Proxy tab.
