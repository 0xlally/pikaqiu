# Troubleshooting common errors within Burp Suite

Source: https://portswigger.net/burp/documentation/desktop/troubleshooting/troubleshooting
Fetched: 2026-06-28T09:16:09.905289+00:00

Support Center

Documentation

Desktop editions

Troubleshooting

Troubleshooting

ProfessionalCommunity Edition

Troubleshooting common errors within Burp Suite

Last updated:

June 18, 2026

Read time:

6 Minutes

If you are new to Burp and are having problems, please first read the help on Getting Started with Burp Suite, and follow the instructions there. Otherwise, the problems and solutions below might help you.

Burp doesn't run

Try launching Burp from the command line. Look at any error messages or other output that appears on the command line, which should indicate the cause of the problem.

I get an error message saying NoClassDefFoundError

When running Burp from the command line, make sure you have included the -jar argument followed by the location of the Burp JAR file. If you're still having problems, check that your command is launching the correct version of Java. Run the command java -version and confirm that the version being executed is 21 or later. If you have installed a later version of Java but an older version is still being executed, then replace java with an absolute path to the correct java executable on your system. If you're still having problems, your Java installation might be corrupted, so reinstall it.

If you get this error message when trying to launch Burp with an extension created using the legacy Extender API, check that your BurpExtender class is declared in the burp package, and resides inside a folder called burp within your extension's JAR file.

I've unpacked the Burp JAR file; what next?

You don't need to unpack or unzip the Burp JAR file. This probably happened because your computer is associating the .JAR file extension with some archiving software. You can change this association to associate with Java, or better, you can launch Burp from the command line.

My browser can't make any requests

If the browser is always waiting and not showing any actual content, then please try the following steps. After each step, check whether you are still having problems, and only continue to the next step if things are not working.

In Burp, go to the Proxy > Intercept tab. If this is showing intercepted HTTP requests, then turn off interception (set the intercept toggle to Intercept off). The browser should now work as normal. See What is Burp Proxy? for more help on the basics of using Burp Proxy.

Try visiting another domain with the browser (ideally a well-known public domain). If this works, then the problem might relate to the specific web site you originally visited.

Go to the Tools > Proxy page in the Settings dialog. In the Proxy Listeners section, the table should show at least one entry where the Running checkbox is checked. If this is unchecked, try to check it. If the box cannot be checked, and an error message box saying Failed to start proxy service appears then Burp is not able to open the specified port and interface. This is often because the port is in use by another process. Select the item in the table, click the Edit button, and change the port number to a different one. Click OK and see whether the listener can now be enabled. You may need to try a few different ports, or query your computer's configuration to locate an available port. Then proceed to the next step to update your browser's proxy configuration with the new port number.

Check that your browser's proxy settings are correctly configured, and are using the same IP address and port number as configured in a running Proxy listener (in Burp's default settings, this is IP address 127.0.0.1 and port 8080, may be different in your current configuration). For further details, see the documentation on configuring an external browser.

In Burp, go to the Network > Connections tab in the Settings dialog. In the Upstream Proxy Servers section, confirm whether any upstream proxies are configured, and if so whether these settings are correct for your network's setup.

Make some more requests from your browser (e.g. press refresh a few times). Look in the Event log tab to see if any new entries are being generated. If so, these entries might indicate the cause of the problem.

Go to the Settings dialog. Click on Manage global settings and select Restore defaults for both

User and Project settings. Then close Burp down gracefully by selecting Exit from the Burp menu. Start Burp again. Shut down all your browser instances, and then open a new browser window.

Burp isn't intercepting anything

In Burp, go to the Proxy > HTTP history tab. Make some more requests from your browser (e.g. press refresh a few times), and check whether any new entries are appearing in the Proxy > HTTP history tab. If so, then Burp is processing your browser traffic but is not presenting any messages for interception. Go to the Proxy > Intercept tab, and enable master interception (set the intercept toggle to Intercept on). Then go to the Tools > Proxy tab in the

Settings dialog. Click the button by Request interception rules and Response interception rules sections. Select Restore defaults for both these sections. Make some more requests from your browser, and these should now appear in the Proxy > Intercept tab.

If your browser is loading pages correctly but no items are appearing in the Proxy > HTTP history tab, you need to check your browser proxy settings. Your browser should be configured to use Burp for both HTTP and HTTPS; any "automatic" proxy settings should be disabled, and any "exceptions" to the proxy settings should be removed. If you are unsure, follow carefully the steps in Configuring Your Browser to ensure your browser is correctly set up.

Burp isn't intercepting HTTPS requests

If your browser is sending HTTP requests through Burp, but not HTTPS requests, then your browser is probably configured to proxy only HTTP. Check in your browser proxy settings that the browser is configured to use Burp for both protocols. If you are unsure, follow carefully the steps in for configuring an external browser to ensure your browser is correctly set up.

HTTPS websites don't work properly

If your browser is able to load HTTPS websites via Burp, but these do not function properly (e.g. the user interface is not complete or fully functional), then the application is probably attempting to load script code or other resources over HTTPS from another domain, and your browser is generating a security alert when loading these resources via Burp. You need to install Burp's CA certificate in your browser, to ensure that applications using HTTPS function properly.

I get authentication failures when using Burp

If the application you are testing uses platform authentication (which normally shows as a popup login dialog within your browser), and you get authentication failure messages when your browser is configured to use Burp, then you need to configure Burp to handle the platform authentication instead of your browser. Go to the Settings > Network > Connections tab, and the Platform Authentication section. Add a new entry for each hostname used by your application, configuring the authentication type and your credentials. If you aren't sure of the authentication type, then first try NTLMv2, then NTLMv1, and then the other types. You may need to close all browser windows and open a new browser window, to prevent any browser caching from interfering with the authentication process.

I'm having performance issues

See Troubleshooting performance details for more details.

How do I run a scan?

You can launch an automated crawl-and-audit scan simply by clicking New scan on the Dashboard tab and supplying the start URL. You can also launch scans in various other ways. See Scanning web sites for more details.

I cannot route traffic from mobile devices to Burp.

This issue could be due to your computer's firewall rules. Ensure that they are configured to allow connections from your mobile device.

Also, refer to configuring mobile devices to work with Burp.

I encounter scaling issues on Windows 10 between my 4k and normal screens

Try starting Burp Suite with these settings:

start javaw -Dsun.java2d.d3d=false -Dsun.java2d.noddraw=true -jar burpsuite_pro_vXXXX.X.jar
