# Setting the site scope

Source: https://portswigger.net/burp/documentation/dast/user-guide/scanning-web-apps/setting-site-scope
Fetched: 2026-06-28T09:15:42.031058+00:00

DAST

Setting the site scope

Last updated:

June 18, 2026

Read time:

3 Minutes

Cloud

Self-hosted

When scanning a web app, the site scope defines which URLs you want to scan, and which you don't want to scan. Burp Scanner only visits URLs that are in scope.

Burp Suite DAST gives you two options for defining the scan scope:

Basic: Use URL prefixes. Burp Suite DAST derives these from your start URLs automatically.

Advanced: Use regex patterns to match URL components. This gives you more precise control.

Using basic scope control

In Basic mode, Burp Suite DAST automatically derives the scan scope from your start URLs. You can refine it further by adding or excluding URL prefixes.

Setting the scope to a domain

To scan everything under a domain, add the root domain as a start URL. For example, adding ginandjuice.shop/ scans everything under that domain. Burp Suite DAST automatically adds the prefix for all your start URLs.

Subdomains are not included by default. For example, admin.ginandjuice.shop is not in scope unless you add it as a separate start URL.

Setting the scope to a specific path

To restrict the scan to a directory, add a trailing slash to the URL. For example, adding ginandjuice.shop/catalog/ scans everything under /catalog/. If you use ginandjuice.shop/catalog without a trailing slash, Burp Suite DAST treats it as a domain-level URL and scans everything under ginandjuice.shop/ instead.

What happens when start URLs overlap

If your start URLs create overlapping scopes, the broadest scope takes precedence. For example, if you add both ginandjuice.shop/ and ginandjuice.shop/catalog/, the scope is set to ginandjuice.shop/.

Manually editing the scope

In Basic mode, you can view and edit your URL prefixes directly under the In scope URL prefixes and Out of scope URL prefixes tabs. You can add URLs that are part of the same web application but not contained under your start URLs, or exclude sections of your website that you don't want to scan.

To add URL prefixes that are in scope:

Add a new web app site, or edit an existing site.

Under Site scope > Refine scan scope, select Basic.

Go to the In-scope URL prefixes tab.

Enter the URL prefixes you want to include in the scope.

To add URL prefixes that are out of scope:

Add a new web app site, or edit an existing site.

Under Site scope > Refine scan scope, select Basic.

Go to the Out-of-scope URL prefixes tab.

Enter the URL prefixes you want to exclude from the scope.

Using advanced scope control

Advanced scope control lets you define scope rules using regex patterns to match URL components. Unlike Basic mode, the scope is not derived from your start URLs automatically. You must add rules to cover all the URLs you want to scan, including the domains of your start URLs.

Each rule consists of the following components:

Protocol - The protocol to match: HTTP, HTTPS, or any.

Host or IP range - A regex to match the hostname, or an IP range. For example, 10.1.1.1/24 or 10.1.1-20.1-127. Leave this blank to match any host.

Port - A regex to match one or more port numbers. Leave this blank to match any port.

File - A regex to match the path portion of the URL. Query strings are ignored. Leave this blank to match any path.

For a URL to match a rule, it must match all of the components you specify.

Adding in-scope rules

To add a rule that includes URLs in the scope:

Add a new web app site, or edit an existing site.

Under Site scope > Refine scan scope, select Advanced.

Go to the In-scope URLs tab.

Click Add advanced scope control. The Add in-scope URL dialog opens.

Fill in the relevant fields and click OK.

Adding out-of-scope rules

To add a rule that excludes URLs from the scope:

Add a new web app site, or edit an existing site.

Under Site scope > Refine scan scope, select Advanced.

Go to the Out-of-scope URLs tab.

Click Add advanced scope control. The Add out-of-scope URL dialog opens.

Fill in the relevant fields and click OK.

Note

Your start URLs must be covered by your in-scope rules. If they're not, you won't be able to save the site.

Related pages

Adding a web app site - explains how to add a new web app site to scan.

Editing existing sites - explains how to update the settings for an existing site.
