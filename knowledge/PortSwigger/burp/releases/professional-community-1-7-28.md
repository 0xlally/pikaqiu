# Professional / Community 1.7.28

Source: https://portswigger.net/burp/releases/professional-community-1-7-28
Fetched: 2026-06-28T09:16:31.883135+00:00

This release introduces simplified scope control.

Burp's existing scope mode employs complex rules allowing you to specify each component of the URL individually (protocol, host, port, and path). You can specify each component using simple expressions, wildcards, and regular expressions. These rules are sometimes complex to create and interpret, and are computationally expensive to apply.

The new scope mode uses simple URL prefixes to define what is in and out of scope. Wildcard expressions are not supported. However, you can omit the URL protocol to match both HTTP and HTTPS:

The new simplified scope control is flexible enough for most purposes, and is enabled by default. You can still enable advanced scope control if you require the power of the old-style scope rules.

State files no longer support saving and reloading of project options. Only project state (site map, Proxy history, etc.) is now included. You can save and reload project options via project configuration files. State files in general are deprecated, and Burp project files should be used instead.

A number of bugfixes and enhancements have been made:

A false positive for external service interaction, from certain Collaborator payloads placed into the URL request line when using an upstream proxy, has been fixed.

Burp now includes the SNI extension in SSL negotiations even when the hostname doesn't contain a dot.

Burp Clickbandit has been updated to fix some issues on Chrome and Edge.

The BApp Store tab now shows the popularity, date of last update, and link to source code on Github, for each BApp.

A bug in the sessions rules UI, where session rules' references to macros were not reflected after reloading settings, has been fixed.

A bug in the filter UI, where a entering a long search string caused the text field to outgrow the window, has been fixed.

Burp's colors and graphics have been updated in line with our website. Additionally, the free edition of Burp has been renamed to Burp Suite Community Edition. We are planning some brand new editions of Burp in the future, and the new name will sit better alongside those. It will, of course, remain free of charge.
