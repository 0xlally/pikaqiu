# Professional / Community 2020.4

Source: https://portswigger.net/burp/releases/professional-community-2020-4
Fetched: 2026-06-28T09:16:33.710115+00:00

This release mainly provides usability improvements to the HTTP message editor. It also upgrades both Java support and Burp Scanner's embedded browser version.

HTTP message editor

The HTTP message editor now supports pretty printing of JSON, XML, HTML, CSS, and JavaScript. Take a look at the following video to see this feature in action:

Unformatted JSON data, for example, would previously be displayed as follows:

But as of version 2020.4, all of the supported formats mentioned above are prettified by default, meaning the JSON data in our example would now be displayed as follows:

You can toggle pretty printing on and off by clicking the "Pretty" button at the bottom of the editor. Alternatively, if you would prefer not to use pretty printing by default, you can disable this setting under "User options" > "Display" > "HTTP Message Display".

Java support

As of this release, we now support Java 13. Unfortunately, we will no longer be able to support Java 8. The vast majority of users will be unaffected by this change. However, if you normally launch Burp directly from the JAR file instead of using the provided installer, you need to make sure that you have one of Java versions 9 to 13 before attempting to launch the new JAR file.

Chromium update

We have updated Burp Scanner's experimental embedded browser to Chromium 81.0.4044.122 in order to implement the latest security fixes.

Other improvements

This release also provides the following minor improvements:

Provided you have Java 13, Burp Proxy now supports TLS 1.3.

Burp now notifies you if the proxy listener is disabled for any reason, and provides guidance on how to reactivate it.

When running Burp in headless mode, you can now execute multiple commands at once by using pipes, heredocs, and so on.

The search bar in the editor is now displayed correctly on smaller screens.

Bug fixes

We have also implemented several minor bug fixes, including:

The response time is now displayed correctly for each request you send in Burp Repeater.

Configured extensions are no longer lost when Burp Suite closes unexpectedly.

The text editor no longer scrolls infinitely when embedded inside another scrolling component.
