# Scope

Source: https://portswigger.net/burp/documentation/desktop/tools/target/scope
Fetched: 2026-06-28T09:16:08.694637+00:00

Support Center

Documentation

Desktop editions

Tools

Target

Scope

ProfessionalCommunity Edition

Scope

Last updated:

June 18, 2026

Read time:

3 Minutes

The Target > Scope tab enables you to tell Burp Suite which hosts and URLs you want to test. This has a number of advantages. For example, you can:

Apply display filters to the site map and proxy history so that they only show in-scope items. For more information, see Filtering the site map and Filtering the HTTP history.

Configure Burp Proxy to log or intercept in-scope requests only. In addition to reducing the noise caused by out-of-scope requests, this can help you to avoid accidentally attacking endpoints or hosts that you don't have permission to test. For more information, see Proxy settings: Proxy history logging and Proxy settings: Request and responses interception rules

Configure Burp Intruder and Burp Repeater to automatically follow redirections to in-scope URLs. For more information, see Intruder settings: Redirections and Repeater settings: Redirects

Professional

Configure a live task so that Burp Scanner automatically audits in-scope requests as you browse. For more information, see Live tasks

URL-matching rules

Burp Suite uses URL-matching rules to determine whether a given URL is in scope. You have the following options for configuring these rules:

Normal scope control

Advanced scope control

Normal scope control

Normal scope control enables you to quickly specify static prefixes for URLs that are in or out of scope. You can explicitly specify the protocol for each prefix. If you don't include the protocol, the rule applies to both HTTP and HTTPS.

The following are some examples of valid URL prefixes:

http://example.com/path

https://example.com/admin

example.com

example.com/myapp/

http://example.com:8080/login

Note

Wildcard expressions are not supported in URL prefixes for normal scope control. You can include all subdomains of a given host by selecting the Include subdomains checkbox. However, note that this is likely to significantly increase the scan duration.

Advanced scope control

Advanced scope control uses URL-matching rules rather than static prefixes. For a URL to match the rule, it must match all the specified features:

Protocol - The protocol that the rule must match: HTTP, HTTPS, or any.

Host or IP range - A regular expression to match the hostname, or an IP range. You can use various standard formats, for example 10.1.1.1/24 or 10.1.1-20.1-127. To match URLs that contain any host, leave this field blank.

Port - A regular expression to match one or more port numbers. Leave the field blank to match URLs that contain any port.

File - The file or path portion of the URL for the rule to match. Query strings are ignored. You can enter a regular expression to match the required range of URL files. To match URLs that contain any path or file, leave the file field blank.

To enable advanced scope control, select the Use advanced scope control checkbox. To create a new URL-matching rule, click Add and fill in the relevant fields manually.

Burp can also generate rules for you based on URLs that you provide. You have the following options:

Click Paste URL to use a URL from your clipboard.

Click Load to use a list of URLs or hostnames from a text file.

Right-click a request in one of Burp's tools and select Add to scope or Remove from scope.

You can fine-tune each rule manually if required.

Note

Regex is not supported when loading port or file information from a text file.

Related pages

Setting the initial test scope
