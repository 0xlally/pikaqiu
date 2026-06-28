# Professional / Community 2020.11

Source: https://portswigger.net/burp/releases/professional-community-2020-11
Fetched: 2026-06-28T09:16:33.137602+00:00

This release provides several new features for both manual and automated testing, as well as some major upgrades to the message editor UI.

Message inspector

The new message inspector is a collapsible panel displayed on the right-hand side of the message editor throughout Burp Suite. It provides a quick way to analyze and work with interesting features of HTTP and WebSocket messages without having to switch between different tabs.

The Hex, Params, Headers, and Cookies tabs that used to appear in the message editor have been removed. You can now access the same functionality, and some additional new features, directly in the inspector panel.

Perform basic operations such as viewing and manipulating any headers, parameters, and cookies found in HTTP messages. You can also add new ones to the request.

Instantly decode HTML, URL, and Base64-encoded values. The inspector automatically applies the appropriate sequence of transformations to decode headers, parameters, cookies, and any encoded text that you manually select in a message.

Work with encoded data more easily by editing it in its decoded form. The inspector automatically reapplies the necessary encodings as you type so that you can inject your modified value into the request with a single click or key press.

Inject non-printing characters by modifying the code point of a character.

You perform some of these actions by drilling down into items that were automatically identified by the inspector. Alternatively, you can manually select one or more characters in a message to work with them in the inspector panel.

For more information about using the inspector, please refer to the documentation.

API scanning

Burp Scanner is now able to scan both JSON and YAML-based APIs for vulnerabilities. By default, the crawler attempts to parse any API definitions that it encounters to identify potential endpoints, along with their supported methods and parameters. You can also explicitly provide the URL of an API definition when launching a scan. Based on the endpoints that it discovers, Burp Scanner is then able to derive new locations to crawl and audit.

If you prefer, you can disable API scanning by deselecting the "Parse API definitions" crawl option in your scan configuration. You can find this option under "Miscellaneous".

Please note that this initial release only supports scanning of a fairly limited range of REST APIs. For a full list of the prerequisites and limitations, please refer to the documentation. We plan to further develop this feature and gradually add support for a wider range of APIs in future releases.

Test recorded login sequences

In the previous release, we added new functionality for recording and uploading full login sequences to help Burp Scanner handle more complex authentication mechanisms. This release adds a new feature that allows you to replay your recorded login sequences in an embedded browser.

This makes it much easier to check whether the recording accurately captured your browser interactions. It may also help you to diagnose any problems if the login sequence is failing during scans.

For more information, please refer to the documentation.

Automatic updates

By default, Burp now automatically downloads any available updates. When a new update has been downloaded, a notification will prompt you to restart Burp in order to install it. Note that you will still need to download the 2020.11 release manually.

If you prefer, you can disable automatic updates in the user options.

Note for Windows users

To support automatic updates, Burp can no longer be installed in a directory that requires admin privileges. As a result, installing 2020.11 on Windows will likely create a new instance of Burp rather than upgrading your existing installation. Unfortunately, this means you will have to manually uninstall your old version of Burp.

This is a one-off inconvenience. Upgrading to any subsequent releases will not require you to repeat this process.

Other improvements

To help reduce clutter, the custom views that some Burp extensions add to the message editor are no longer accessed via individual tabs. Instead, you can now alternate between your extension-specific views using a new drop-down menu.

Bug fixes

We have fixed a bug that was causing the Burp UI to freeze in specific circumstances when the .NET Beautifier extension was enabled.

When hovering the mouse over a long, encoded token in an HTTP message, the decoded text no longer overflows the tooltip. We have also extended the tooltip so that it can display up to 2000 characters.

Launching an installed version of Burp now provides the same range of character sets as when launching Burp from a JAR file.
