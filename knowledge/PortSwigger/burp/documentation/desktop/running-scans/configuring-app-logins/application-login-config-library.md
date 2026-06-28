# Managing application logins using the configuration library

Source: https://portswigger.net/burp/documentation/desktop/running-scans/configuring-app-logins/application-login-config-library
Fetched: 2026-06-28T09:15:52.830506+00:00

Support Center

Documentation

Desktop editions

Running scans

Configuring application logins

Managing application logins using the configuration library

Professional

Managing application logins using the configuration library

Last updated:

June 18, 2026

Read time:

1 Minute

Burp Suite's configuration library enables you to store sets of login credentials and recorded login sequences so that you can use them in later scans. You can save and load application logins from the scan launcher.

To load application logins from the library, click Select from library and select the required login. Burp Suite adds the selected credentials or recorded login sequence to the list.

To save all of the scan's application logins to the configuration library:

Click Save to library to display the Save configuration to library dialog.

Enter a Configuration name.

Click Save.

Burp Suite saves all of the credentials or recorded login sequences in the list to the configuration library. If you select this configuration for a different scan then Burp Suite adds the application logins to that scan.

Note

You can also add application logins directly to the configuration library from the Settings dialog. For more information, see Configuration library.
