# Professional / Community 2021.12

Source: https://portswigger.net/burp/releases/professional-community-2021-12
Fetched: 2026-06-28T09:16:34.509293+00:00

This release enables you to configure Intruder attacks against multiple hosts and adds several new options for customizing the Inspector. These include docking the panel to the left or right of the screen and toggling line wrapping within each widget. As of this release, there is also a dedicated installer for Mac machines with the M1 chip.

Multi-host Intruder attacks

You can now add payload positions to the target host field in Burp Intruder, enabling you to target multiple hosts from a single attack. This is useful in situations where you want to test for issues across many web applications simultaneously.

As part of this change, the settings previously included in Intruder's Target tab have been incorporated into its Positions tab.

New Inspector panel options

We have added a toolbar at the top of the Inspector panel. This contains buttons that let you:

Toggle whether the Inspector is docked to the left or right of the screen.

Collapse all widgets.

Expand all widgets that contain data.

You can also toggle line wrapping by clicking the icon in the upper-right corner of each table.

Support for Mac M1(Arm64) chips

Burp Suite now supports the latest Apple Mac models equipped with M1 (Arm64) processors. We now provide a dedicated installer for these machines.

If you're not sure which installer you need, please refer to the documentation for details.

Proxy Intercept is now off by default (new installations only)

Due to overwhelming customer demand, Burp Proxy's Intercept feature is now off by default on new installations of Burp Suite. This removes the common problem of users forgetting to disable it before attempting to use the browser.

Please note that if you have upgraded an existing installation, you are not affected by this change. However, you can adjust this setting manually under User options > Misc > Proxy Interception.

Embedded browser upgrade

We have upgraded Burp's browser to Chromium 96.0.4664.45.

Bug fixes

We have also fixed a number of minor bugs. Most notably, we have fixed a bug that prevented Burp from completing the TLS handshake with servers whose certificate chain was longer than 10 but less than 30.
