# Burp Suite Enterprise Edition Power Tools: Unleashing the power to the command line, Python, and more

Source: https://portswigger.net/blog/burp-suite-enterprise-edition-power-tools-unleashing-the-power-to-the-command-line-python-and-more
Fetched: 2026-06-28T09:15:09.420436+00:00

Burp Suite Enterprise Edition Power Tools: Unleashing the power to the command line, Python, and more

Ollie Whitehouse |

Tuesday, 21 March 2023 at 14:30 UTC

Burp Suite

Enterprise Edition

tl;dr

We have released BSEEPT - Burp Suite Enterprise Edition Power Tools which:

Is a command line tool to drive all aspects of the BSEE GraphQL API.

Is a Python client library to allow you to easily utilise the BSEE GraphQL API in your own code be it command line tooling, lambdas, or integration layers.

Returns BSEE's JSON allowing you to parse on the command line with jq and similar.

Backstory

In January I joined PortSwigger in a more involved capacity as Non-Executive Director++ (the ++ being I can still code whilst sitting in the boardroom). In my first month I spent time coming up to speed on the products, their features, roadmaps, and most importantly their APIs for extensibility and similar.

These first months saw me produce two extension prototypes using the Montoya API. These used the Google Safe Browsing API to identify known malicious sites in sitemaps and a YAML-powered regular expression engine to identify sensitive information presence / leakage. I then had the fortune of working with Hannah and Alex on the TOTP Authenticate extension to support multi-factor authentication in Burp Suite Enterprise Edition.

I then turned my attention to the Burp Suite Enterprise Edition GraphQL API. It struck me that we had this amazing GraphQL API, which we both use in the product, but also expose to customers. But for DevOps teams and others in the security function to really utilize this required a bit of investment.

So an objective was born ... write the power tools that teams who work with Burp Suite Enterprise Edition would find valuable.

Que A-Team building music, over 80 commits, lots of learning (I learnt to use a Mac at the same time) and out popped BSEEPT.

BSEEPT allows you to use every aspect of the GraphQL API from the command line or in your own Python code.

Quick Demo

I have written an extensive readme on the GitHub project but I will give an example of how one might use it.

In this example we will run through several steps:

Query the run scans.

Then pass through jq to just extract the issue titles.

Then pass through jq to build a CSV of issue titles, site, and path they were found in.

All without writing any new code - just using command line tools!

So we first get the scan details:

bseept % python3 bseept.py --getscans | jq

{

"data": {

"scans": [

{

"id": "123",

"status": "succeeded",

"site_id": "1",

"schedule_item": {

"id": "1",

"site": {

"id": "1",

"name": "Gin & Juice"

},

"schedule": {

"initial_run_time": "2022-09-02T13:51:14.550Z",

"rrule": "FREQ=DAILY;INTERVAL=2"

},

"has_run_more_than_once": true,

"scheduled_run_time": "2023-03-15T13:51:14.000Z"

},

"scheduled_start_time": "2023-03-13T13:51:14.000Z",

"start_time": "2023-03-13T13:51:54.525Z",

"end_time": "2023-03-13T14:37:50.525Z",

"duration_in_seconds": 2756,

"scan_failure_code": null,

"scan_metrics": {

"crawl_request_count": 774,

"unique_location_count": 54,

"audit_request_count": 57437,

"crawl_and_audit_progress_percentage": 100,

"scan_phase": null,

"audit_start_time": null,

"current_url": "https://ginandjuice.shop:443/robots.txt"

},

"scan_failure_message": null,

"scan_delta": {

"new_issue_count": 0,

"repeated_issue_count": 40,

"regressed_issue_count": 0,

"resolved_issue_count": 0

},

"issue_counts": {

"total": 40,

"high": {

"total": 11,

"firm": 4,

"tentative": 0,

"certain": 7

},

"medium": {

"total": 0,

"firm": 0,

"tentative": 0,

"certain": 0

},

"low": {

"total": 10,

"firm": 5,

"tentative": 3,

"certain": 2

},

"info": {

"total": 19,

"firm": 1,

"tentative": 1,

"certain": 17

}

},

"scanner_version": "2023.2.3",

"scanner_build_number": 19390

},

...

Second, extract the issues for the successful scan with the scan ID of 123:

bseept % python3 bseept.py --getscanissues 123 | jq

{

"data": {

"scan": {

"issues": [

{

"issue_type": {

"name": "External service interaction (HTTP)",

"description_html": "<p>External service interaction arises when it is possible to induce an application to interact with an arbitrary external service, such as a web or mail server. The ability to trigger arbitrary external service interactions does not constitute a vulnerability in its own right, and in some cases might even be the intended behavior of the application.\nHowever, in many cases, it can indicate a vulnerability with serious consequences.</p>\n<p>The ability to send requests to other systems can allow the vulnerable server to be used as an attack proxy.\n By submitting suitable payloads, an attacker can cause the application server to attack other systems that it can interact with. \n This may include public third-party systems, internal systems within the same organization, or services available on the local loopback adapter of the application server itself. \n Depending on the network architecture, this may expose highly vulnerable internal services that are not otherwise accessible to external attackers. </p>",

"remediation_html": "<p>You should review the purpose and intended use of the relevant application functionality, \n and determine whether the ability to trigger arbitrary external service interactions is intended behavior. \n If so, you should be aware of the types of attacks that can be performed via this behavior and take appropriate measures. \n These measures might include blocking network access from the application server to other internal systems, and hardening the application server itself to remove any services available on the local loopback adapter.</p>\n<p>If the ability to trigger arbitrary external service interactions is not intended behavior, then you should implement a whitelist of permitted services and hosts, and block any interactions that do not appear on this whitelist.</p>\n\n<p>Out-of-Band Application Security Testing (OAST) is highly effective at uncovering high-risk features, to the point where finding the root cause of an interaction can be quite challenging. To find the source of an external service interaction, try to identify whether it is triggered by specific application functionality, or occurs indiscriminately on all requests. If it occurs on all endpoints, a front-end CDN or application firewall may be responsible, or a back-end analytics system parsing server logs. In some cases, interactions may originate from third-party systems; for example, a HTTP request may trigger a poisoned email which passes through a link-scanner on its way to the recipient.</p>",

"vulnerability_classifications_html": "<ul>\n<li><a href=\"https://cwe.mitre.org/data/definitions/918.html\">CWE-918: Server-Side Request Forgery (SSRF)</a></li>\n<li><a href=\"https://cwe.mitre.org/data/definitions/406.html\">CWE-406: Insufficient Control of Network Message Volume (Network Amplification)</a></li>\n</ul>",

"references_html": "<ul>\n <li><a href=\"https://portswigger.net/blog/introducing-burp-collaborator\">Burp Collaborator</a></li>\n <li><a href=\"https://portswigger.net/burp/application-security-testing/oast\">Out-of-band application security testing (OAST)</a></li>\n <li><a href=\"https://portswigger.net/research/cracking-the-lens-targeting-https-hidden-attack-surface\">PortSwigger Research: Cracking the Lens</a></li>\n</ul>"

},

"confidence": "certain",

"display_confidence": null,

"serial_number": "5601616512020228096",

"severity": "high",

"description_html": "It is possible to induce the application to perform server-side HTTP and HTTPS requests to arbitrary domains.

The payload <b>http://s0t5stlr0i5p270b2o0hxzl1ksqlee24qzdq1f.oastify.com/</b> was submitted in the <b>Referer</b> HTTP header.

The application performed an HTTP request to the specified domain.",

"remediation_html": null,

"path": "/catalog",

"origin": "https://ginandjuice.shop",

"novelty": "repeated",

"tickets": null,

"generated_by_extension": null

},

Third, we use jq to parse the JSON and print the issue titles from scan 123:

bseept % python3 bseept.py --getscanissues 123 | jq ".[].scan.issues[].issue_type.name"

"External service interaction (HTTP)"

"External service interaction (HTTP)"

"External service interaction (HTTP)"

"HTTP response header injection"

"External service interaction (HTTP)"

"Cross-site scripting (reflected)"

"Cross-site scripting (reflected)"

"SQL injection"

"XML external entity injection"

"Cross-site scripting (reflected)"

"Client-side template injection"

"Strict transport security not enforced"

"Password field with autocomplete enabled"

"Iterable input"

"Iterable input"

"Iterable input"

"Iterable input"

"Iterable input"

"Open redirection (DOM-based)"

"Open redirection (DOM-based)"

"Vulnerable JavaScript dependency"

"Cookie without HttpOnly flag set"

"Cookie without HttpOnly flag set"

"Input returned in response (reflected)"

"Cacheable HTTPS response"

"TLS certificate"

"TLS cookie without secure flag set"

"External service interaction (DNS)"

"External service interaction (DNS)"

"Input returned in response (reflected)"

"External service interaction (DNS)"

"Input returned in response (reflected)"

"Cross-site scripting (reflected)"

"Input returned in response (reflected)"

"External service interaction (DNS)"

"Input returned in response (reflected)"

"Input returned in response (reflected)"

"Input returned in response (reflected)"

"Client-side prototype pollution"

"Request URL override"

Fourth, we build a CSV-like output of issue names, their origin site and path:

bseept % python3 bseept.py --getscanissues 123 | jq '.[].scan.issues[] | "\(.issue_type.name),\(.origin),\(.path)"'

"External service interaction (HTTP),https://ginandjuice.shop,/catalog"

"External service interaction (HTTP),https://ginandjuice.shop,/catalog/filter"

"External service interaction (HTTP),https://ginandjuice.shop,/catalog/product"

"HTTP response header injection,https://ginandjuice.shop,/catalog/product-search-results/5"

"External service interaction (HTTP),https://ginandjuice.shop,/catalog/product/stock"

"Cross-site scripting (reflected),https://ginandjuice.shop,/catalog/search/3"

"Cross-site scripting (reflected),https://ginandjuice.shop,/catalog/search/4"

"SQL injection,https://ginandjuice.shop,/catalog/filter"

"XML external entity injection,https://ginandjuice.shop,/catalog/product/stock"

"Cross-site scripting (reflected),https://ginandjuice.shop,/catalog/search/2"

"Client-side template injection,https://ginandjuice.shop,/catalog/search/4"

"Strict transport security not enforced,https://ginandjuice.shop,/"

"Password field with autocomplete enabled,https://ginandjuice.shop,/login"

"Iterable input,https://ginandjuice.shop,/post"

"Iterable input,https://ginandjuice.shop,/post"

"Iterable input,https://ginandjuice.shop,/post"

"Iterable input,https://ginandjuice.shop,/post"

"Iterable input,https://ginandjuice.shop,/post"

"Open redirection (DOM-based),https://ginandjuice.shop,/catalog/product"

"Open redirection (DOM-based),https://ginandjuice.shop,/catalog/product"

"Vulnerable JavaScript dependency,https://ginandjuice.shop,/resources/js/angular_1-7-7.js"

"Cookie without HttpOnly flag set,https://ginandjuice.shop,/"

"Cookie without HttpOnly flag set,https://ginandjuice.shop,/"

"Input returned in response (reflected),https://ginandjuice.shop,/"

"Cacheable HTTPS response,https://ginandjuice.shop,/"

"TLS certificate,https://ginandjuice.shop,/"

"TLS cookie without secure flag set,https://ginandjuice.shop,/"

"External service interaction (DNS),https://ginandjuice.shop,/catalog"

"External service interaction (DNS),https://ginandjuice.shop,/catalog/filter"

"Input returned in response (reflected),https://ginandjuice.shop,/catalog/filter"

"External service interaction (DNS),https://ginandjuice.shop,/catalog/product"

"Input returned in response (reflected),https://ginandjuice.shop,/catalog/product-search-results/1"

"Cross-site scripting (reflected),https://ginandjuice.shop,/catalog/product-search-results/1"

"Input returned in response (reflected),https://ginandjuice.shop,/catalog/product-search-results/5"

"External service interaction (DNS),https://ginandjuice.shop,/catalog/product/stock"

"Input returned in response (reflected),https://ginandjuice.shop,/catalog/search/2"

"Input returned in response (reflected),https://ginandjuice.shop,/catalog/search/3"

"Input returned in response (reflected),https://ginandjuice.shop,/catalog/search/4"

"Client-side prototype pollution,https://ginandjuice.shop,/"

"Request URL override,https://ginandjuice.shop,/"

That's it. As mentioned there is an extensive help document with examples of both the command line and code.

Issues and feedback

Please raise any bugs / feature requests as issues so they can be resolved.

Email with any questions / feedback to ollie.whitehouse at portswigger [.] net.

Getting it

Scoot on over to the BSEEPT - BSEEPT - Burp Suite Enterprise Edition Power Tools GitHub project.

Burp Suite

Enterprise Edition

Ollie Whitehouse

@ollieatnowhere

Latest Posts

Burp Extensibility 2026: Awards, Talks, and Highlights

19 June 2026

Burp Extensibility 2026: Awards, Talks, and Highlights

The beast needs a cage: What's next for AppSec post-Mythos

12 May 2026

The beast needs a cage: What's next for AppSec post-Mythos

3 ways custom scan checks turn practitioner knowledge into scalable automation

01 May 2026

3 ways custom scan checks turn practitioner knowledge into scalable automation

Senior pentesters have a deeply refined intuition about what is vulnerable in an environment. The problem? That expertise is often siloed with an individual and trapped in their notes or Python scripts.
