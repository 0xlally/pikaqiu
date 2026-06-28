# Professional / Community 1.7.16

Source: https://portswigger.net/burp/releases/professional-community-1-7-16
Fetched: 2026-06-28T09:16:31.168161+00:00

This release adds various enhancements and fixes:

There is a new command-line option to launch Burp with a specified user configuration file:

--user-config-file=my_file.json

This can be used to set any user-level option, including Burp extensions to load. It is useful when running Burp on headless systems where there is no UI for configuring user-level options. By creating a suitable user-level config file, it is possible to launch Burp on a headless system with specific Burp extensions or any other user-level setting.

Some recent changes to Tomcat cause it to reject a wider range of raw characters in the URL query string, going beyond the standard practice of browsers and other web servers. Burp Scanner and Intruder now apply URL-encoding to the relevant characters by default, ensuring that their payloads are accepted by Tomcat and reach the application code.

A bug that was recently introduced that prevented license activation in headless mode has been fixed.

The Content Discovery function now correctly handles applications that have wildcard behavior for file extensions (e.g. those that return a specific response for admin.xxx regardless of the file extension). This eliminates the only known false positives reported by the new Content Discovery engine.

There are some new options in the Proxy for stripping request headers that offer to support encodings that may cause problems with intercepted traffic in Burp. These options are on by default.

Logging options have moved from the user level to the project level, and are now included in project-level configuration files and project files. This means that you can enable logging on a per-project basis and have this setting remembered when reopening a project file.

Unicode characters in URLs are now properly handled in the "Paste URL as request" function.

Various other minor bugfixes and enhancements have been made.
