# Burp's browser settings

Source: https://portswigger.net/burp/documentation/desktop/settings/tools/burps-browser
Fetched: 2026-06-28T09:15:56.592300+00:00

Support Center

Documentation

Desktop editions

Settings

Tools

Burp's browser

ProfessionalCommunity Edition

Burp's browser settings

Last updated:

June 18, 2026

Read time:

1 Minute

The Burp's browser page in the Settings dialog contains settings for:

Browser data.

Browser running.

Browser data

The Store browser data checkbox determines whether Burp's browser stores settings and history in the specified browser data folder. To stop storing browser data, deselect the checkbox.

To delete past data, click Clear all.

The Browser data settings are user settings. They apply to all installations of Burp on your machine.

Browser running

Burp's browser is sandboxed by default. In some circumstances, such as when running in Linux as root, you might not be able to launch browser-powered scans using the sandbox.

Note

To determine whether the browser can launch browser-powered scans using the sandbox, use the Health check for Burp's browser tool in the browser's Help menu.

The Allow Burp's browser to run without a sandbox setting enables you to run Burp's browser without the sandbox. Before you select this setting, please make sure that you are aware of the associated security implications. Scanning hostile websites without the sandbox increases the risk of your local system being compromised.

The Use the GPU option enables Burp's browser to access the GPU. Note that crashes can occur if Burp's browser attempts to use a non-existent GPU.

The Browser running settings are project settings. They apply to the current project only.
