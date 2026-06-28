# Configuring an iOS device to work with Burp Suite Professional

Source: https://portswigger.net/burp/documentation/desktop/mobile/config-ios-device
Fetched: 2026-06-28T09:15:51.672546+00:00

Support Center

Documentation

Desktop editions

Mobile testing

Configuring an iOS device to work with Burp Suite Professional

ProfessionalCommunity Edition

Configuring an iOS device to work with Burp Suite Professional

Last updated:

June 18, 2026

Read time:

2 Minutes

You can test web applications and mobile apps using an iOS device. To do this, you need to do the following:

Configure your Burp Proxy listener to accept connections on all network interfaces.

Connect both your device and your computer to the same wireless network.

To interact with HTTPS traffic, you need to install a CA certificate on your iOS device.

Step 1: Configure the Burp Proxy listener

To configure the proxy settings for Burp Suite Professional:

Open Burp Suite Professional click Settings to open the

Settings dialog.

Go to Tools > Proxy.

In Proxy listeners, click Add.

In the Binding tab, set Bind to port to 8082 (or another port that is not in use).

Select All interfaces and click OK.

At the prompt, click Yes.

Step 2: Configure your device to use the proxy

To configure the proxy settings for your iOS device:

In your iOS device, go to Settings > Wi-Fi.

Make sure that the Wi-Fi button is on and connect to your Wi-Fi network.

Select the information icon (i) next to your Wi-Fi network.

Set Configure Proxy to Manual.

Set Server to the IP address of the computer that is running Burp Suite Professional.

Set Port to the port value that you configured for the Burp Proxy listener, in this example 8082.

Touch Save

.

Step 3: Install a CA certificate on your iOS device

In order to interact with HTTPS traffic, you need to install a CA certificate from your Burp Suite Professional installation on your iOS device.

To install the CA certificate to your iOS device:

Make sure that Burp Suite Professional is running on your computer.

Use the browser on your iOS device to go to http://burpsuite and select CA Certificate.

When the CA certificate downloads, select Profile downloaded in the Settings menu.

On the Install Profile screen, select Install.

On the Installing Profile screen, select Install.

When the profile is installed, select Done.

Go to Settings > General > About > Certificate Trust Settings.

Activate the toggle switch for Portswigger CA.

Step 4: Test the configuration

To test the configuration:

Open Burp Suite Professional.

Go to Proxy > Intercept and click Intercept is off to switch intercept on.

Open the browser on your iOS device and go to an HTTPS web page.

The page should load without any security warnings. You should see the corresponding requests within Burp Suite Professional.
