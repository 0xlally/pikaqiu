# Temporary file location settings

Source: https://portswigger.net/burp/documentation/desktop/settings/suite/temp-files-location
Fetched: 2026-06-28T09:15:56.326612+00:00

Support Center

Documentation

Desktop editions

Settings

Suite

Temporary files location

ProfessionalCommunity Edition

Temporary file location settings

Last updated:

June 18, 2026

Read time:

1 Minute

These settings let you configure where Burp stores its temporary files.

By default, Burp creates a directory in the temporary file location provided by the platform. If required, you can specify a custom directory instead. For example, you might want to use a different volume, or a location that is not externally readable.

Note

On MacOS, you may find that the operating system sometimes clears the default temporary file location following system hibernation, causing Burp to lose any temporary files. To resolve this problem, configure a custom location for Burp to store temporary files.

Changes to this setting take effect the next time that Burp starts up.

The Temporary files location settings are user settings. They apply to all installations of Burp on your machine.
