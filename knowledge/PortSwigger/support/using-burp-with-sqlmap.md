# Using Burp with SQLMap

Source: https://portswigger.net/support/using-burp-with-sqlmap
Fetched: 2026-06-28T09:17:37.333752+00:00

This page may be out of date

We haven't updated it for a while because we're busy working on new, improved content to help you get the

most out of Burp Suite. In the meantime, please note that the information on this page may no longer be

accurate.

Visit our Support Center

Using Burp with SQLMap

SQLMap is a standalone tool for identifying and exploiting SQL injection vulnerabilities.

Using Burp with SQLMap

First, you need to load the SQLiPy plugin by navigating to the Extensions > "BApp Store" tab, selecting SQLiPy, and clicking the "Install" button.

You can find more about installing extensions and the required environments on our Installing extensions tutorial page.

With the SQLiPy extension installed, go to the SQLiPy "SQLMap Scanner" tab.

Fill out the form with the appropriate details.

In this example we have used the default IP and port configuration.

The other and better option would be to manually start the SQLMap API server on your system (or any other system on which SQLMap is installed).

The command line options are as follows:

python sqlmapapi.py -s -H <IP> -p <Port>

Ensure that the API is running correctly as a server.

Return to Burp and go to the intercepted request you wish to scan.

Right click to bring up the context menu.

The plugin creates a context menu option of "SQLiPy Scan".

Click "SQLiPy Scan" to send the request to SQLMap.

This will take the request and auto populate information in the SQLiPy "Sqlmap Scanner" tab.

In the same tab, configure the options that you want for the injection testing.

Then click the "Start Scan" button.

Progress and informational messages on scans and other plugin activities are displayed in the extensions SPLiPy "SQLMap Logs" tab.

If the tested page is vulnerable to SQL injection, then the plugin will add an entry to the Target "Site map" tab.
