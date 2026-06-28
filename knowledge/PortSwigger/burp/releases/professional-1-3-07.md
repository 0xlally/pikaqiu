# Professional 1.3.07

Source: https://portswigger.net/burp/releases/professional-1-3-07
Fetched: 2026-06-28T09:16:23.328376+00:00

1. Burp now supports more types of redirection in situations where redirects are to be followed automatically (e.g. some Intruder attacks). The types of redirects which Burp understands can be controlled in a new configuration section in the global options tab:

The redirection targets which Burp will actually follow are still determined by the configuration within each individual tool (e.g. based on target scope).

2. Burp Repeater now has the facility to manually follow redirects where desired. When a redirect response is received which Repeater has not followed automatically, a "follow redirect" button appears, enabling you to manually follow the redirect after viewing it. This feature is useful for walking through each request and response in a redirection sequence. New cookies will be processed in these manual redirects if this option has been set in Repeater's configuration.

3. Burp Extender now provides the facility to register custom menu items which will appear on the context menus used throughout Burp to receive user actions. Extensions which need to add custom menu items should provide an implementation of the new IMenuItemHandler interface, and use the registerMenuItem method of IBurpExtenderCallbacks to register each custom menu item. Burp will then display the custom menu items whenever a context menu is shown to the user, and will invoke the relevant handler when the user clicks the menu item.

Burp passes to the menu item handler the full request and response details of the user-selected item(s) for which the context menu was generated. This new functionality enables extensions to inter-operate in user-driven ways with third-party software, or, using the various methods in IBurpExtenderCallbacks, extend Burp's own functionality in new ways.

4. Rendering of multi-byte character sets is improved, and most charsets should now render properly in the HTTP message editor when the appropriate encoding is set on the command line, for example:

-Dfile.encoding=SHIFT_JIS

Note that cursor positioning when editing content that uses some multi-byte charsets may be unreliable, due to the varying lengths of multi-byte sequences used in many charsets. Specific support for the SHIFT_JIS, EUC-JP and UTF-8 charsets has been provided. If you encounter any multi-byte charsets which are not handled properly in either viewing or editing, please let me know the encoding type and a sample URL, and proper support will be added.

Other future work in this area will enable Burp to dynamically determine the relevant charset from the contents of HTTP responses and use this when rendering, thus avoiding the need to set command line options for specific charsets.

5. The proxy history context menu now has a "clear history" option.

6. In XML exports of scan issues and request/response details, the "host" element now has an "ip" attribute which shows the IP address of the host. Note that for performance reasons fresh lookups are not performed during reporting, and the value of the "ip" attribute will be an empty string if Burp has not resolved the hostname.

7. The configuration for client SSL certificates now has a default-off option to allow unsafe renegotiation, which is apparently necessary when using some client certificates.

8. The state restore wizard now includes a default-on option to pause the spider and active scanner when the saved state is restored. This helps to avoid inadvertently attacking targets when loading old state files into Burp that include ongoing tasks in the spider and scanner queues.

9. There are numerous minor bugfixes.
