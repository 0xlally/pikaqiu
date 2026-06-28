# Performing common tasks with the GraphQL API

Source: https://portswigger.net/burp/documentation/dast/user-guide/api-documentation/graphql-api/graphql-common-tasks
Fetched: 2026-06-28T09:15:34.632445+00:00

DAST

Performing common tasks with the GraphQL API

Last updated:

June 18, 2026

Read time:

14 Minutes

This page details some common tasks that you can perform using Burp Suite DAST's GraphQL API.

This document is intended to complement the API reference, which contains full reference information on the GraphQL API and a brief introduction to GraphQL itself.

On this page:

Retrieving a list of scans

Retrieving the most recent scan for a site

Retrieving basic details for a specific scan

Retrieving a list of scan configurations

Retrieving basic site tree details

Retrieving scan issue information

Retrieving all issues for a scan

Retrieving detailed information about a specific issue

Generating a scan remediation report

Creating a site

Scheduling a new scan

Moving a site to a new folder

Query and mutation names

You must specify a name for any queries and mutations you use in the API. Query and mutation names should be specified directly after the query or mutation keyword. For example:

query <QueryNameHere> {

<query type> {

<query content>

}

}

Note that, while all queries and mutations must have a name, that name can be anything you choose. As such, the query and mutation names given in these examples are entirely arbitrary.

Retrieving a list of scans

This scans query returns the id and status of all scans in the database. In this simplified example, the API has returned three successful scans.

Request

query GetScan {

scans {

id

status

}

}

Example response

{

"data": {

"scans": [

{

"id": "21029",

"status": "succeeded"

},

{

"id": "21028",

"status": "succeeded"

},

{

"id": "21027",

"status": "succeeded"

}

]

}

}

The scan object contains many additional fields that could potentially be added to the request. You can also remove either of these fields from the request if required.

For a list of additional fields that the scans query can return, see the Scan Object page of the API reference.

Retrieving the most recent scan for a site

This scans query takes a site_id and returns details of the most recent scan that has been run for that site. Specifically, it generates a list of scans sorted in descending order of start date, and then limits the number of entries in that list to one.

As well as timing and status information, the query returns a new_issue_count field detailing the number of issues found by this scan that were not found by the previous scan.

In this example we can see that the most recent scan for site_id 28 was successful and found no new issues.

Request

query getScans {

scans(site_id: 28, limit: 1, sort_column: start, sort_order: desc) {

id,

status,

start_time,

end_time,

scan_delta {

new_issue_count

},

}

}

Example response

{

"data": {

"scans": [

{

"id": "21110",

"status": "succeeded",

"start_time": "2021-11-08T14:35:12.190Z",

"end_time": "2021-11-08T15:04:09.013Z",

"scan_delta": {

"new_issue_count": 0

}

}

]

}

}

The scan object contains many additional fields that could potentially be added to the request. You can also remove most of these fields from the request if required.

For a list of additional fields that the scans query can return, see the Scan Object page of the API reference.

Retrieving basic details for a specific scan

This scan query takes the id of a particular scan and returns the number of issues at each level of severity found during that scan, as well as the scan's status and site name.

In this example we can see that scan 21029 found five high-severity issues, one low-severity issue, and six information-only issues.

Request

query GetScan {

scan (id: 21029) {

status

site_name

issue_counts {

high {

total

}

medium {

total

}

low {

total

}

info {

total

}

}

}

}

Example response

{

"data": {

"scan": {

"status": "succeeded",

"site_name": "vulnerable-website",

"issue_counts": {

"high": {

"total": 5

},

"medium": {

"total": 0

},

"low": {

"total": 1

},

"info": {

"total": 6

}

}

}

}

}

The scan object contains many additional fields that could potentially be added to the request. You could also remove most of the fields specified in the example from the request if required.

For a list of valid scan fields, see the Scan Object page of the API reference.

Retrieving a list of scan configurations

In Burp Suite DAST, a scan configuration defines various settings that determine how a scan is performed, such as the maximum crawl depth of the crawl, what types of issues to report, and the maximum time that a scan will run.

This scan_configurations query lists the id and name of all scan configurations that you have set up in Burp. In this simplified example, the API has retrieved details of three scan configurations.

Request

query GetScanConfigurations {

scan_configurations {

id

name

}

}

Example response

{

"data": {

"scan_configurations": [

{

"id": "31556c28-38c9-415d-9a00-d3df51470a22",

"name": "Audit checks - all except JavaScript analysis"

},

{

"id": "d8018e42-0467-4b44-80a8-a159ec691ddf",

"name": "Audit checks - all except time-based detection methods"

},

{

"id": "542322ab-1984-45a2-810e-6d3410e1e01a",

"name": "Audit checks - light active"

}

]

}

}

For a list of additional fields that the scan_configurations query can return (including the scan_configuration_fragment_json field, which returns the configuration itself in JSON format), see the Scan Configuration Object page of the API reference.

Retrieving basic site tree details

In Burp Suite DAST, the site tree is the hierarchical structure containing all sites and folders that are currently configured.

Each site and folder in the tree has a unique id and a parent_id. The tree structure is defined using these two fields. For example, if a folder has an id of 1 then any folders or sites located directly within that folder would have a parent_id of 1.

This site_tree query returns the id, parent_id, and name of all sites and folders in the tree. In this example, the API has returned four folders: 0 (root), 1, 2, and 3. 1 and 2 are top-level folders (i.e. direct children of root), and 3 is located within 2. There are also four sites, one located at the root level, two located within folder 1, and one located within folder 3.

Request

query SitesAndFolderInfo {

site_tree {

sites {

id

parent_id

name

}

folders {

id

parent_id

name

}

}

}

Example response

{

"data": {

"site_tree": {

"sites": [

{

"id": "81",

"parent_id": "0",

"name": "Global"

},

{

"id": "82",

"parent_id": "1",

"name": "Northern US"

},

{

"id": "38",

"parent_id": "1",

"name": "Southern US"

},

{

"id": "39",

"parent_id": "3",

"name": "UK"

}

],

"folders": [

{

"id": "0",

"parent_id": null,

"name": "All Sites"

},

{

"id": "1",

"parent_id": "0",

"name": "US Sites"

},

{

"id": "2",

"parent_id": "0",

"name": "Europe Sites"

},

{

"id": "3",

"parent_id": "2",

"name": "UK Sites"

}

]

}

}

}

For a list of additional site fields that the site_tree query can return, see the Site Tree Object page of the API reference.

Retrieving scan issue information

This query gives an overview of the issue types found in a particular scan. Specifically, it returns three pieces of information:

The type_index of each high-severity issue type found during the scan. Note that, if required, you can amend or remove the severities field to change the severity of the issues returned.

A count of the total number of issues found during the scan

Further details on all issue instances that have a specific type_index, including a description and a serial number for each individual instance of the issue.

This example shows a request for information on scan 21029, with further details of all issue instances that have a type_index of 3146256 (External Service Interaction - HTTP). In this case, we can see that there were three different types of high-severity issue reported. Of the 12 total issue instances returned, one was an instance of an External Service Interaction - HTTP issue.

Looking up type indexes

A type_index is an identifier for a particular type of issue (as opposed to a specific instance of an issue). You can look up issue type values on the Issue Definitions page of the PortSwigger Support Center.

Please note that while we provide type indexes in both hexadecimal and decimal formats for reference purposes, the API only accepts decimal type_index values.

Request

query ScanInfo {

scan(id: 21029) {

issue_type_groups(severities: high) {

issue_type {

type_index

}

severity

}

issue_counts {

total

}

issues(start: 0, count: 44, type_index: "3146256") {

description_html

path

remediation_html

serial_number

}

}

}

Example response

{

"data": {

"scan": {

"issue_type_groups": [

{

"issue_type": {

"type_index": "3146240"

},

"severity": "high"

},

{

"issue_type": {

"type_index": "3146256"

},

"severity": "high"

},

{

"issue_type": {

"type_index": "1051648"

},

"severity": "high"

}

],

"issue_counts": {

"total": 12

},

"issues": [

{

"description_html": "It is possible to induce the application to perform server-side HTTP requests to arbitrary domains.<br><br>The payload <b>http://929xszo277xq82vclxu5rykbr2xvlmca2ytlj98.burpcollaborator.net/?foo</b> was submitted in the <b>q</b> field.<br><br>The application performed an HTTP request to the specified domain.<br><br>Burp Infiltrator detected that input is being passed to a potentially unsafe API.",

"path": "/http-collaborator",

"remediation_html": null,

"serial_number": "6150599811840047104"

}

]

}

}

}

The scan object contains many additional fields that could potentially be added to the request. You could also remove most of the example fields from the request if required. For a list of valid scan fields, see the Scan Object page of the API reference.

Retrieving all issues for a scan

This scan query returns the serial_number and the name of the relevant issue_type for all issue instances found by a particular scan.

In this example, we can see that scan 21029 found 12 individual issues, of which all had a different issue_type.

Request

query GetScan {

scan(id: 21029) {

issues(start: 0, count: 1000) {

issue_type {

name

}

serial_number

}

}

}

Example response

{

"data": {

"scan": {

"issues": [

{

"issue_type": {

"name": "External service interaction (DNS)"

},

"serial_number": "432120106538718976"

},

{

"issue_type": {

"name": "External service interaction (HTTP)"

},

"serial_number": "6150595811840047104"

},

{

"issue_type": {

"name": "JavaScript injection (DOM-based)"

},

"serial_number": "4716073395305441280"

},

{

"issue_type": {

"name": "PHP code injection"

},

"serial_number": "540804386956503040"

},

{

"issue_type": {

"name": "SQL injection"

},

"serial_number": "17259916985675520"

},

{

"issue_type": {

"name": "Unencrypted communications"

},

"serial_number": "3974375729790973952"

},

{

"issue_type": {

"name": "HTML does not specify charset"

},

"serial_number": "4889966492298873856"

},

{

"issue_type": {

"name": "Credit card numbers disclosed"

},

"serial_number": "2403021217137964032"

},

{

"issue_type": {

"name": "Email addresses disclosed"

},

"serial_number": "5872016766220388352"

},

{

"issue_type": {

"name": "Input returned in response (stored)"

},

"serial_number": "4102206774889574400"

},

{

"issue_type": {

"name": "File path traversal"

},

"serial_number": "2466965706342529024"

},

{

"issue_type": {

"name": "Suspicious input transformation (stored)"

},

"serial_number": "3364917051419260928"

}

]

}

}

}

The issue object contains many additional fields that could potentially be added to the request. For a list of valid issue fields, see the Issue Object page of the API reference.

Retrieving detailed information about a specific issue

This query returns detailed information on a specified issue instance.

This example shows a request for information on an issue instance with the serial_number 6150599811840047104, as found by scan 21029. The response shows that this is an instance of an External Service Interaction - HTTP issue, and gives extensive information on the circumstances in which the issue was discovered.

Request

query Issue {

issue(scan_id: 21029, serial_number: 6150599811840047104) {

issue_type {

type_index

name

description_html

remediation_html

vulnerability_classifications_html

references_html

}

confidence

display_confidence

serial_number

description_html

remediation_html

severity

path

origin

novelty

evidence {

... on Request {

request_index

request_count

request_segments {

... on DataSegment {

data_html

}

... on HighlightSegment {

highlight_html

}

... on SnipSegment {

snip_length

}

}

}

... on Response {

response_index

response_count

response_segments {

... on DataSegment {

data_html

}

... on HighlightSegment {

highlight_html

}

... on SnipSegment {

snip_length

}

}

}

... on HttpInteraction {

title

description_html

request {

... on DataSegment {

data_html

}

... on HighlightSegment {

highlight_html

}

... on SnipSegment {

snip_length

}

}

response {

... on DataSegment {

data_html

}

... on HighlightSegment {

highlight_html

}

... on SnipSegment {

snip_length

}

}

}

... on DescriptiveEvidence {

title

description_html

}

}

}

}

Example response

{

"data":{

"issue":{

"issue_type":{

"type_index":"3146256",

"name":"External service interaction (HTTP)",

"description_html":"<p>External service interaction arises when it is possible to induce an application to interact with an arbitrary external service, such as a web or mail server. The ability to trigger arbitrary external service interactions does not constitute a vulnerability in its own right, and in some cases might even be the intended behavior of the application.\nHowever, in many cases, it can indicate a vulnerability with serious consequences.</p>\n<p>The ability to send requests to other systems can allow the vulnerable server to be used as an attack proxy.\n By submitting suitable payloads, an attacker can cause the application server to attack other systems that it can interact with. \n This may include public third-party systems, internal systems within the same organization, or services available on the local loopback adapter of the application server itself. \n Depending on the network architecture, this may expose highly vulnerable internal services that are not otherwise accessible to external attackers. </p>",

"remediation_html":"<p>You should review the purpose and intended use of the relevant application functionality, \n and determine whether the ability to trigger arbitrary external service interactions is intended behavior. \n If so, you should be aware of the types of attacks that can be performed via this behavior and take appropriate measures. \n These measures might include blocking network access from the application server to other internal systems, and hardening the application server itself to remove any services available on the local loopback adapter.</p>\n<p>If the ability to trigger arbitrary external service interactions is not intended behavior, then you should implement a whitelist of permitted services and hosts, and block any interactions that do not appear on this whitelist.</p>\n\n<p>Out-of-Band Application Security Testing (OAST) is highly effective at uncovering high-risk features, to the point where finding the root cause of an interaction can be quite challenging. To find the source of an external service interaction, try to identify whether it is triggered by specific application functionality, or occurs indiscriminately on all requests. If it occurs on all endpoints, a front-end CDN or application firewall may be responsible, or a back-end analytics system parsing server logs. In some cases, interactions may originate from third-party systems; for example, a HTTP request may trigger a poisoned email which passes through a link-scanner on its way to the recipient.</p>",

"vulnerability_classifications_html":"<ul>\n<li><a href=\"https://cwe.mitre.org/data/definitions/918.html\">CWE-918: Server-Side Request Forgery (SSRF)</a></li>\n<li><a href=\"https://cwe.mitre.org/data/definitions/406.html\">CWE-406: Insufficient Control of Network Message Volume (Network Amplification)</a></li>\n</ul>",

"references_html":"<ul>\n <li><a href=\"https://portswigger.net/blog/introducing-burp-collaborator\">Burp Collaborator</a></li>\n <li><a href=\"https://portswigger.net/burp/application-security-testing/oast\">Out-of-band application security testing (OAST)</a></li>\n <li><a href=\"https://portswigger.net/research/cracking-the-lens-targeting-https-hidden-attack-surface\">PortSwigger Research: Cracking the Lens</a></li>\n</ul>"

},

"confidence":"certain",

"display_confidence":null,

"serial_number":"6150599811840047104",

"description_html":"It is possible to induce the application to perform server-side HTTP requests to arbitrary domains.<br><br>The payload <b>http://929xszo277xq82vclxu5rykbr2xvlmca2ytlj98.burpcollaborator.net/?foo</b> was submitted in the <b>q</b> field.<br><br>The application performed an HTTP request to the specified domain.<br><br>Burp Infiltrator detected that input is being passed to a potentially unsafe API.",

"remediation_html":null,

"severity":"high",

"path":"/http-collaborator",

"origin":"http://vulnerable-website.com",

"novelty":"regression",

"evidence":[

{

"request_index":0,

"request_count":2,

"request_segments":[

{

"data_html":"GET /http-collaborator?q="

},

{

"highlight_html":"http%3a%2f%2f929xszo277xq82vclxu5rykbr2xvlmca2ytlj98.burpcollaborator.net%2f%3ffoo"

},

{

"data_html":" HTTP/1.1\r\nHost: vulnerable-website.com\r\nAccept-Encoding: gzip, deflate\r\nAccept: */*\r\nAccept-Language: en-US,en-GB;q=0.9,en;q=0.8\r\nUser-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36\r\nConnection: close\r\nCache-Control: max-age=0\r\nReferer: http://vulnerable-website.com/http-collaborator\r\n\r\n"

}

]

},

{

"response_index":0,

"response_count":2,

"response_segments":[

{

"data_html":"HTTP/1.1 200 OK\r\nDate: Wed, 03 Nov 2021 13:48:49 GMT\r\nContent-Type: text/html; charset=UTF-8\r\nContent-Length: 94\r\nConnection: close\r\nX-frame-options: DENY\r\n\r\n<html><h1>HTTP Collaborator Evidence</h1><body><a href='?q=foo'>collaborator</a></body></html>"

}

]

},

{

"request_index":1,

"request_count":2,

"request_segments":[

{

"data_html":"GET /http-collaborator?q="

},

{

"highlight_html":"http%3a%2f%2fvkjjal6optfcqody3jcr9k2x9ofh38uwkkb71vq.burpcollaborator.net%2f%3ffoo"

},

{

"data_html":" HTTP/1.1\r\nHost: vulnerable-website.com\r\nAccept-Encoding: gzip, deflate\r\nAccept: */*\r\nAccept-Language: en-US,en-GB;q=0.9,en;q=0.8\r\nUser-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36\r\nConnection: close\r\nCache-Control: max-age=0\r\nReferer: http://vulnerable-website.com/http-collaborator\r\n\r\n"

}

]

},

{

"response_index":1,

"response_count":2,

"response_segments":[

{

"data_html":"HTTP/1.1 200 OK\r\nDate: Wed, 03 Nov 2021 13:48:50 GMT\r\nContent-Type: text/html; charset=UTF-8\r\nContent-Length: 94\r\nConnection: close\r\nX-frame-options: DENY\r\n\r\n<html><h1>HTTP Collaborator Evidence</h1><body><a href='?q=foo'>collaborator</a></body></html>"

}

]

},

{

"title":"Collaborator HTTP interaction",

"description_html":"<div>\n<p>\nThe Collaborator server received an HTTP request.<br><br> The request was received from IP address 52.211.196.189 at 2021-Nov-03 13:48:49 UTC.\n</p>\n</div>",

"request":[

{

"data_html":"GET /?foo HTTP/1.1\r\nUser-Agent: Java/1.8.0_212\r\nHost: "

},

{

"highlight_html":"929xszo277xq82vclxu5rykbr2xvlmca2ytlj98.burpcollaborator.net"

},

{

"data_html":"\r\nAccept: text/html, image/gif, image/jpeg, *; q=.2, */*; q=.2\r\nConnection: keep-alive\r\n\r\n"

}

],

"response":[

{

"data_html":"HTTP/1.1 200 OK\r\nServer: Burp Collaborator https://burpcollaborator.net/\r\nX-Collaborator-Version: 4\r\nContent-Type: text/html\r\nContent-Length: 62\r\n\r\n<html><body>giuovbxib34f2id10pll5zzjlgjjgigjfigz</body></html>"

}

]

},

{

"title":"Unsafe API call",

"description_html":"<div class=\"unsafe-api-call-description\">\n<p>Burp Infiltrator detected that input is being passed to the following API:</p>\n<pre class=\"code\">java.net.URLConnection java.net.URL.openConnection() throws java.io.IOException</pre>\n\n<p>\nThe following value was passed to the object's constructor:\n</p>\n\n<pre class=\"code\">http://vkjjal6optfcqody3jcr9k2x9ofh38uwkkb71vq.burpcollaborator.net/?foo</pre>\n\n<p>The call stack when the API was invoked was:</p>\n<pre class=\"code\">net.portswigger.VulnerableServer$HttpCollaborator.getResponse(VulnerableServer.java:428)\nnet.portswigger.VulnerableServer$AbstractHttpHandler.handle(VulnerableServer.java:175)\ncom.sun.net.httpserver.Filter$Chain.doFilter(Filter.java:79)\nsun.net.httpserver.AuthFilter.doFilter(AuthFilter.java:83)\ncom.sun.net.httpserver.Filter$Chain.doFilter(Filter.java:82)\nsun.net.httpserver.ServerImpl$Exchange$LinkHandler.handle(ServerImpl.java:675)\ncom.sun.net.httpserver.Filter$Chain.doFilter(Filter.java:79)\nsun.net.httpserver.ServerImpl$Exchange.run(ServerImpl.java:647)\njava.util.concurrent.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1149)\njava.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:624)\njava.lang.Thread.run(Thread.java:748)\n</pre>\n</div>"

}

]

}

}

}

You can remove most of the fields in this example to filter the information returned if required. For information on the structure of the issue object, see the Issue Object page of the API reference.

Generating a scan remediation report

This scan_report query returns a Scan Remediation report for a specified scan. The Scan Remediation report is a web page containing a breakdown of the issues that were returned by the scan, including background, remediation advice, and the location at which the issue was found.

This example shows a request to get the scan report for scan 21029, with any false positives returned by that scan omitted. Note that this example omits the HTML content of the report itself for space reasons.

Request

query GetScanReport {

scan_report(scan_id: 21029, include_false_positives: false) {

report_html

}

}

Example response

{

"data": {

"scan_report": {

"report_html": "<html></html>"

}

}

}

The scan_report query has several additional fields that you can use to filter the information included in the scan. For a full list of these fields, see the Queries page of the API reference.

Unescaping the report HTML

The HTML returned by the scan_report query is JSON-escaped. The escaped characters are necessary in order to transfer the report safely.

As such, you will need to perform some processing on the HTML in order to view it as a web page. To do so:

Extract the HTML content from the API response by copying everything between the two <html> tags and pasting it into a text file.

JSON-unescape the HTML. There are various tools online that you can use for this purpose.

Save the unescaped HTML into a .html file.

Open the .html file in a web browser to view the report.

Creating a site

The create_site mutation creates a new site within Burp Suite DAST's site tree. This example shows a successful request to create a new site. The API response contains confirmation of the site details that were provided in the request.

Note

You need to set a valid parent_id for the location of your new site. If you set parent_id: to 0, the site is created in the root folder.

Request

mutation CreateSite {

create_site(input: {name: "MyVulnerableWebsite", parent_id: 0, application_logins: {login_credentials: [], recorded_logins: []} , scope_v2: {start_urls: "https://vulnerable-website.com/", protocol_options: USE_SPECIFIED_PROTOCOLS}}) {

site {

id

parent_id

scope_v2 {

start_urls

protocol_options

}

application_logins {

login_credentials {

id

label

username

}

recorded_logins {

id

label

}

}

email_recipients {

email

}

}

}

}

Example response

{

"data": {

"create_site": {

"site": {

"id": "89",

"parent_id": "0",

"scope_v2": {

"start_urls": [

"https://vulnerable-website.com/"

],

"protocol_options": "USE_SPECIFIED_PROTOCOLS"

},

"application_logins": {

"login_credentials": [],

"recorded_logins": []

},

"email_recipients": []

}

}

}

}

The fields that can be used when creating a new site are defined by the CreateSiteInput object. For more information on available fields when creating a new site, see the Create Site Input Object page of the API reference.

Note

In this example we have added two addresses as email recipients. These addresses will automatically receive a scan report whenever a scan finishes for the site.

Your SMTP server must be configured in order for Burp Suite DAST to send email notifications. For more information on how to set up your SMTP server, see Configuring your SMTP server.

Scheduling a new scan

This create_schedule_item mutation enables you to schedule scans in bulk for sites and folders.

The example shows a request to schedule scans for site_ids 1 and 2, and folder_ids 7 and 8.

Request

mutation CreateScheduleItem {

create_schedule_item(input: {site_ids: ["1", "2"], folder_ids: ["7", "8"]}) {

schedule_item {

id

schedule {

rrule

initial_run_time

}

scheduled_run_time

}

}

}

Example response

{

"data":{

"create_schedule_item":{

"schedule_item":{

"id":"21042",

"schedule":{

"rrule":null,

"initial_run_time":"2021-11-04T11:07:25.664Z"

},

"scheduled_run_time":null

}

}

}

}

If required, you can specify scheduling and configuration information within the create_schedule_item mutation. For information on the fields accepted by create_schedule_item, see the Create Schedule Item Mutation page of the API reference.

Moving a site to a new folder

The move_site mutation moves a given site to a different location within the site tree hierarchy. Specifically, it enables you to specify a new parent_id for the specified site.

This example shows a request to move a site with an id of 89 to the root folder (i.e. the folder with an id of 0).

Request

mutation MoveSitetoSpecFolder {

move_site(input: {site_id: 89, parent_id: 0}) {

site {

id

name

parent_id

scope_v2 {

start_urls

}

scan_configurations {

id

}

}

}

Example response

{

"data":{

"move_site":{

"site":{

"id":"89",

"name":"MyVulnerableWebsite",

"parent_id":"0",

"scope_v2":{

"start_urls":[

"https://vulnerable-website.com/"

]

},

"scan_configurations":[

]

}

}

}

}

The move_site mutation can return various other site fields if required. For a list of these fields, see the Site Object page of the API reference.
