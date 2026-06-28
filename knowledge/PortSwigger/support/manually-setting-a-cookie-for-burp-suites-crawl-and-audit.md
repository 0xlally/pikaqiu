# Manually setting a cookie for Burp's Crawl and Audit

Source: https://portswigger.net/support/manually-setting-a-cookie-for-burp-suites-crawl-and-audit
Fetched: 2026-06-28T09:17:34.603747+00:00

This page may be out of date

We haven't updated it for a while because we're busy working on new, improved content to help you get the

most out of Burp Suite. In the meantime, please note that the information on this page may no longer be

accurate.

Visit our Support Center

Manually setting a cookie for Burp's Crawl and Audit

In some instances, usually involving authentication, it is necessary to manually set a cookie for use with Burp's automated tools. To do this, you'll need to create a session handling rule using the "Set a specific cookie or parameter value" function. This action updates the request and sets a specific value in a named parameter or cookie. If it is not already present, you can specify the type of parameter that should be added.

First, perform the login process and monitor the process in the HTTP history tab.

Go to Project options > Sessions and open the cookie jar.

Use the Edit cookie function to view the cookie name and value.

Leave this pop up window open to allow easy access to this information.

Next, go to Project options > Sessions and use the Add function to create a new rule.

Rename the rule and set a rule action.

Click the "Set a specific cookie or parameter value" option.

This will open the "Session handling action editor".

Copy and paste the name and value of the cookie from the Cookie editor.

Optionally, you can use ensure the cookie is added if it is not already present.

Each rule comprises a scope (what the rule applies to).

The scope for each rule can be defined based on any or all of the following features of the request being processed; the Burp tool that is making the request, the URL of the request, the names of parameters within the request.

To test the rule functions correctly, you can send request that requires authentication to Burp Repeater.

In Repeater, remove the cookie and use the "Go" button to send the request to the server.

The rule will add the cookie to the request automatically.

Now, when you perform a scan, the cookie will be added to each request.

We've used the Logger++ extension to observe this behavior.
