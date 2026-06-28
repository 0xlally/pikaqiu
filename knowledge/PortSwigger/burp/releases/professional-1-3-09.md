# Professional 1.3.09

Source: https://portswigger.net/burp/releases/professional-1-3-09
Fetched: 2026-06-28T09:16:23.349217+00:00

Any HTTP response within Burp can now be rendered in your browser, to avoid the limitations of Burp's built-in HTML renderer. This feature is accessed by selecting any item with a response, and choosing the "show in browser" item from the context menu. Burp then gives you a unique URL which you can paste into your browser (configured to use the current instance of Burp as its proxy), to render the response. The resulting browser request is served by Burp with the exact response that you selected (the request is not forwarded to the original web server), and yet the response is processed by the browser in the context of the originally requested URL. Hence, relative links within the response will be handled properly by your browser. As a result, your browser may make additional requests (for images, CSS, etc.) in the course of rendering the response - these will be handled by Burp in the usual way.

The function to save Burp's state now includes an option to include only in-scope items. When working on a client engagement, this enables you to save only relevant items for archiving or sharing with colleagues. The new option is available in the save state wizard, in the automatic backup feature, and in scheduled tasks that save state.

IBurpExtenderCallbacks now includes the following methods for loading and saving configuration:

java.util.Map saveConfig()

void loadConfig(java.util.Map config)

Configuration information is handled as a map of name/value pairs. Any settings not specified in the Map will be restored to their default values. To selectively update only some settings and leave the rest unchanged, you should first call saveConfig to obtain Burp's current configuration, modify the relevant items in the Map, and then call loadConfig with the same Map.

IBurpExtenderCallbacks now includes the following method for adding arbitrary items to Burp's site map:

void addToSiteMap(IHttpRequestResponse item)

This method allows extensions to write custom interfaces to import the output from other tools.

IHttpRequestResponse now includes the following methods for accessing user-annotated comments in items belonging to Burp tools that support comments:

java.lang.String getComment()

void setComment(java.lang.String comment)

Burp Intruder now includes a built-in payload list containing User-Agent strings for numerous browsers. This can be used for testing whether applications return different content to different mobile devices, etc.

The Suite-wide options now include a default-off option to enable all supported cipher suites during SSL negotiation. This option is not normally necessary but may be useful when attempting to connect to unusually configured SSL stacks.

This release fixes another source of UI instability when running on Mac. Soon, Burp is going to be so stable on this platform that it will prevent OSX itself from crashing.
