# Professional 1.3.08

Source: https://portswigger.net/burp/releases/professional-1-3-08
Fetched: 2026-06-28T09:16:23.676592+00:00

This release includes various new features and fixes:

Improved stability on Mac OSX. The UI hangs that sometimes occur are hopefully resolved reduced. I'm keen to eliminate the remaining Mac problems and be able to say that Burp officially runs on this platform, so if you are aware of any issues at all, please let me know and I'll get them fixed.

Added support for upstream SOCKS proxies:

Each individual configuration panel now has its own "restore defaults" button, so you can revert specific parts of Burp's configuration without needing to reset the configuration for a whole tool or the entire suite.

Added support for headless mode (this is when you pass -Djava.awt.headless=true as a command-line argument to your JRE, to prevent it from building a user interface). In this mode, the proxy will pass through all messages without interception, and no other UI-based control is possible. Full programmatic control of Burp via Burp Extender is still possible.

The default proxy request interception rule now ignores JS and ICO extensions, in addition to CSS and other common image file extensions.

Some issues identified with UI extensibility (introduced in v1.3.07) have been addressed. In the previous version, there were some unnecessary limitations on the IHttpRequestResponse objects passed to IMenuItemHandler.menuItemClicked(), which have now been removed:

The setRequest() and setResponse() methods now work when invoked on requests and responses currently displayed in the proxy interception view.

The getRequest() and getResponse() methods now return the currently displayed message (after any user edits) in the proxy interception view.

The getResponse() method now works in Burp Repeater provided the request currently displayed in the request panel has been issued and has not been subsequently edited by the user.

These enhancements enable Burp extensions to perform various useful functions via custom menu items. For example, if a client-side application component adds a checksum to request data, an extension could create a custom menu item to reapply the correct checksum to the currently displayed request, following any edits by the user.

The colours used for some encoding types in Burp Decoder have been changed to make them more legible on some platforms.

There is a function (on the help menu) to extract diagnostic information about the OS and JRE on which Burp is running, to help troubleshoot some issues.

The "send to comparer" context menu item now supports multiple selection of items in tables/trees.

Various minor bugs are fixed.
