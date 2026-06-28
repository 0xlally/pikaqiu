# Setting the initial test scope in Burp Suite

Source: https://portswigger.net/burp/documentation/desktop/testing-workflow/test-scope
Fetched: 2026-06-28T09:15:58.411247+00:00

Support Center

Documentation

Desktop editions

Testing workflow

Setting a test scope

ProfessionalCommunity Edition

Setting the initial test scope in Burp Suite

Last updated:

June 18, 2026

Read time:

2 Minutes

By default, as you use Burp's browser, Burp logs all HTTP or WebSocket messages for further analysis. By setting a scope, you can tell Burp which URLs you want to test and which you don't want to test. For example, you may want to exclude URLs that:

You don't have permission to test.

Aren't safe to test. For example, URLs that contain potentially dangerous functionality.

Aren't relevant. Once you have set the scope, you can use the filters in the Target site map and Proxy history to screen out some of the noise.

Note

In Burp Suite Community Edition, your scope settings are lost when you close Burp, along with any other data. You can save the scope settings as part of a project file in Burp Suite Professional. For more information, see

Project files.

Adding URLs to the scope

To add a URL to your scope:

Click Scope settings on the lower toolbar to open the Settings dialog.

Scroll to the Target scope setting.

Under Include in scope, click Add. The Add prefix for in-scope URLs dialog opens.

Enter the prefix for the URLs that you want to match, then click OK.

When prompted, choose whether to stop logging out-of-scope traffic. This can provide performance benefits.

The prefix is added to the Include in scope list. Any URL that starts with this exact prefix is now in scope. Any URL that doesn't start with a prefix from the list is out of scope. For example, if you add

https://example.com, requests to any path on this domain are in scope if they're accessed over HTTPS.

Excluding URLs from the scope

After you add a URL to your scope, you may want to exclude specific paths that are a subset of the in-scope prefixes, such as https://example.com/admin. To exclude a URL from your scope:

Click Scope settings on the lower toolbar to open the Settings dialog.

Scroll to the Target scope setting.

Under Exclude from scope, click Add. The Add prefix for out-of-scope URLs dialog opens.

Enter a prefix for the URLs that you want to exclude, then click OK.

The prefix is added to the Exclude from scope list. A URL is now in scope if it starts with an in-scope prefix, but does not start with an out-of-scope prefix.

Related pages

Target scope.

Scope settings - Target scope.

URL-matching rules - Advanced scope control.

You can directly add URLs to scope from the Target site map, Proxy history, and Logger. For a tutorial on this function, see

Setting the target scope.
