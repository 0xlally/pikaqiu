# Professional / Community 1.7.22

Source: https://portswigger.net/burp/releases/professional-community-1-7-22
Fetched: 2026-06-28T09:16:31.592678+00:00

This release introduces Burp Suite Mobile Assistant, a new tool to facilitate testing of iOS apps with Burp Suite. It supports the following key functions:

It can modify the system-wide proxy settings of iOS devices so that HTTP(S) traffic can be easily redirected to a running instance of Burp. (Supported on iOS 8 and later.)

It can attempt to circumvent SSL certificate pinning in selected apps, allowing Burp Suite to break their HTTPS connections and intercept, inspect and modify all traffic. (Supported on iOS 8 and 9).

Burp Suite Mobile Assistant runs on jailbroken devices running iOS 8 and later. For full details of how to install and use Burp Suite Mobile Assistant, please see the documentation.

A number of other minor enhancements and fixes have been made, including:

The selected column ordering in the Proxy history is now remembered in user-level settings.

Editing URL or cookie parameters in the "Params" view no longer loses the request body if it contains JSON/XML/etc.

Performance when deleting multiple selected items from the Proxy history is significantly improved.

Some memory problems encountered when scanning items with huge responses have been addressed.

A new method has been added to the API: IMessageEditor.getSelectionBounds().
