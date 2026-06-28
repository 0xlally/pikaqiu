# Professional 1.5.15

Source: https://portswigger.net/burp/releases/professional-1-5-15
Fetched: 2026-06-28T09:16:25.674306+00:00

This release includes a large number of updates to the Proxy tool.

SSL Pass Through

You can now specify destination web servers for which Burp will directly pass through SSL connections. Passing through SSL can be useful in cases where it is not straightforward to eliminate SSL errors on the client - for example, in mobile applications that perform SSL certificate pinning. If the application accesses multiple domains, or uses a mix of HTTP and HTTPS connections, then passing through SSL connections to specific problematic hosts still enables you to work on other traffic using Burp in the normal way.

If the option to automatically add entries on client SSL negotiation failure is enabled, then Burp will detect when the client fails an SSL negotiation (for example, due to not recognizing Burp's CA certificate), and will automatically add the relevant server to the SSL pass through list.

Startup Interception State

There is a new option to configure whether proxy interception should be enabled when Burp is started up. You can choose to always enable interception, always disable interception, or to restore the setting from when Burp was last closed.

Highlighting Unhidden Fields

When Burp is configured to automatically unhide hidden fields in responses, there is a new sub-option to prominently highlight unhidden fields on-screen, for easy identification:

Fix Newlines In Edited Requests

There is a new option to automatically fix missing or superfluous new lines at the end of requests that have been edited in the intercept view. If an edited request does not contain a blank line following the headers, Burp will add this. If an edited request with a body containing URL-encoded parameters contains any newline characters at the end of the body, Burp will remove these.

This new option, which is off by default, can be useful to correct mistakes made while manually editing requests in the interception view, to avoid issuing invalid requests to the server.

New Interception Rules

You can now configure interception rules for requests and responses based specifically on the names and values of cookies. You can configure rules for responses based on the MIME type and on whether the request was annotated (commented or highlighted) by the user.

New Match/Replace Rules

Various updates have been made to the match/replace functionality:

You can define rules based on parameter names and values.

You can configure a rule to operate only on the first line of requests, for making quick changes to the URL or request method.

You can optionally use literal or regular expressions in match rules.

You can add comments to rules to describe their purpose. This facilitates quick toggling of individual rules without needing to read them to understand what they are doing.

Various new default rules have been added for performing common tasks.

The documentation has been updated to describe how you can use regular expressions to match multi-line regions of message bodies, and how you can use regex groups in back-references and replacement strings.

Editing Target Server in Intercept View

You can now manually edit the target server to which an intercepted request will be sent, by clicking on the server caption or the button next to it.

Updated In-Browser Burp UI

Burp's in-browser UI has been updated in various ways:

There are more readable and informative messages when a request causes a problem.

Invalid client requests are reproduced in full in the error message, to assist debugging.

The interface is now available both at http://burp (when you have configured your browser to use Burp as its proxy) and at the URL of your Burp listener (for example, http://127.0.0.1:8080, even if your browser is not configured to use Burp).

Support for Firefox Plug-n-hack Plugin

Burp now supports the new Firefox plug-n-hack plugin. This enables faster configuration of the browser to work with Burp, by automatically configuring the browser to use Burp as its proxy, and installing Burp's CA certificate in the browser. If you are using Firefox and have installed the plug-n-hack plugin, you can configure your browser to use Burp by visiting the URL of your Burp listener (by default, http://127.0.0.1:8080) and following the "Plug-n-hack" link.

Quick Navigation of History In Repeater

The back/forward buttons for navigating the Repeater history now have drop-down lists showing numbered nearby items in the history, to enable quick navigation to a required item.
