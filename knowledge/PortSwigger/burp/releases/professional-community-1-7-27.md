# Professional / Community 1.7.27

Source: https://portswigger.net/burp/releases/professional-community-1-7-27
Fetched: 2026-06-28T09:16:32.475374+00:00

This release adds various minor enhancements:

There is a new hotkey for adding an Intruder payload position marker. This is not mapped to any keystroke by default, but this can be done at User options / Misc / Hotkeys.

There is a new option on startup to disable extensions. This can help resolve situations where a misbehaving extension causes problems during startup.

Burp Collaborator server now responds to DNS lookups containing the subdomain "spoofed" with the IP address 127.0.0.1. This is to prevent the Collaborator being wrongly incriminated when a server being scanned is vulnerable to client IP spoofing, as happened here.

The option to strip the "Accept-Encoding" header in incoming requests to the Proxy has been modified so that it normalizes the header to a default value rather than stripping it altogether. The previous behavior caused problems with some WAFs configured to drop requests without this header.

The default max heap size requested by the platform installer has been reduced from 75% to 50% of total physical memory, in order to prevent OS performance issues on some platforms. This can be modified after installation by editing the vmoptions file in the installation directory.

MacOS App Nap has been disabled as this can cause Burp's automated activity (like scanning) to be suspended when the Burp window is in the background.

Additionally, a number of bugs have been fixed:

A bug that caused temporary data saved by Burp extensions and the sessions tracer to actually get stored in project files.

A bug that caused the Spider not to honor the "Maximum parameterized requests per URL" setting.

A bug that caused some lightweight popups to have full window decoration on some Linux desktop managers.

A bug that incorrectly handled loading of IP addresses from file into the scope configuration UI.

A bug that prevented upstream SNI from working when proxying traffic through Burp from an Android emulator.

A bug that caused report generation to fail altogether when it encountered an incomplete issue due to project file corruption.
