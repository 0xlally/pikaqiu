# BCheck definition reference

Source: https://portswigger.net/burp/documentation/scanner/bchecks/bcheck-definition-reference
Fetched: 2026-06-28T09:16:10.500664+00:00

Support Center

Documentation

Scanner

BCheck definitions

BCheck definition reference

DASTProfessional

BCheck definition reference

Last updated:

June 18, 2026

Read time:

13 Minutes

This page details the keywords available when writing a BCheck. Mandatory properties are marked with an asterisk (*).

On this page

Metadata

Control flow

Conditionals

Actions

Reserved variables

Functions

Misc

BCheck structure

Metadata

Contains information about the check itself. The metadata object is mandatory for all BChecks and must be placed at the very start of the definition.

metadata

metadata:

language: v2-beta

name: "Simple SQLi"

description: "Tests insertion points for basic SQLi"

author: "Peter Wiener"

tags: "sql", "active", "sql-injection"

Property

Description

Type

language*

The version of the BCheck definition language used.

enum [v2-beta]

name*

The BCheck's name. This is displayed in the Burp Suite UI when the check reports an issue.

String

description

A description of the BCheck.

String

author

The author's name.

String

tags

Identifying tags.

List of strings

Control flow

These keywords control the flow of execution for the definition.

run for each

Declares an array variable that can be iterated over. When the variable is called the check runs once for each item in the array. The variable declared has outer scope.

The run for each keyword is optional. If used, you must place it before the given...then statement in your definition.

run for each:

variable_name = "variable value 1", "variable value 2", etc.

Example

The example declares a variable called url_array listing three URLs. This could be useful if you are writing a check that needs to run the same test against multiple URLs (for example, adding each in turn as the Origin header in a CORS misconfiguration check).

run for each:

url_array =

null,

"http://example.com",

`https://{random_str(5)}{base.response.url}`

define

Declares variables with inner scope. The define keyword is optional. If used, you must place it before the given...then statement in your definition.

define:

variable_name = "variable_content"

Example

The example calls the generate_collaborator_address() function to generate a new Burp Collaborator address, and stores it in a variable called collaborator_address.

define:

collaborator_address = {generate_collaborator_address()}

given...then

Defines when the check runs, based on the content being audited.

given [response|request|host|path] | [ [any|query|header|body|cookie]* + insertion point] then

Each BCheck must have a single given / then statement containing:

EITHER one of the following:

given response then - The check runs once for each response audited.

given request then - The check runs once for each request audited.

given host then - The check runs once for each host audited.

given path then - The check runs once for each unique path audited.

OR one of the following insertion point keywords:

given any insertion point then - The check runs once for each insertion point (of any type) audited. Burp Scanner also uses this default option if you do not specify an insertion point type (i.e. you use given insertion point).

given query insertion point then - The check runs once for each query audited.

given header insertion point then - The check runs once for each header audited.

given body insertion point then - The check runs once for each body content audited.

given cookie insertion point then - The check runs once for each cookie audited.

You can use the or keyword to combine insertion points. For example:

given query or body insertion point then - The check runs once for each query or body content audited.

given header or cookie insertion point then - The check runs once for each header or cookie audited.

Conditionals

These keywords control actions that happen as a result of a set condition. You can only use conditional keywords inside a given...then statement.

if... then

Executes an action if a set condition is met. Requires the following:

A condition.

An action.

An end if keyword.

if [condition] then

[action]

end if

Example

If the latest response contains an Apache Struts version number then report an issue:

if {latest.response} matches "Apache Struts [\d\s\.]+" then

report issue:

severity: info

confidence: certain

detail: "Disclosed Apache Server"

remediation: "Do not reveal error messages"

end if

else if... then

Used within an if statement. Executes an action if the preceding condition is false and the else if condition is true. You can use multiple else if statements within a BCheck.

if [condition 1] then

[action 1]

else if [condition 2] then

[action 2]

end if

Example

If the check results in the Collaborator receiving DNS interactions then report an issue with firm confidence. Otherwise, check whether the Collaborator has received any SMTP interactions. If it has, report an issue with tentative confidence.

if dns interactions then

report issue:

severity: high

confidence: firm

else if smtp interactions then

report issue:

severity: high

confidence: tentative

end if

else then

Used within an if statement. Executes an action if the statement's condition and the condition of any preceding else / if statements are not met.

if [condition] then

[action]

else then

[action 2]

end if

Example

If the latest response is not identical to the base response but does have the same HTTP status code, report an issue with firm confidence. Otherwise, report an issue with tentative confidence.

if {latest.response} differs from {base.response} and {latest.response.status_code} is {base.response.status_code} then

report issue:

severity: high

confidence: firm

else then

report issue:

severity: high

confidence: tentative

end if

end if

Denotes the end of an if statement.

if [condition] then

[action]

end if

Conditions

You can use the following conditions in if statements:

{X} matches "[regex]" - True if X matches the regex provided.

{X} differs from {Y} - True if response X differs from response Y.

{X} in {Y} - True if Y contains X (for example, Y could be a response and X could be a header to search for within that response).

{X} is {Y} - True if the provided parameters are identical.

any interactions - True if Burp Collaborator has received any interactions.

dns interactions - True if Burp Collaborator has received any DNS interactions.

http interactions - True if Burp Collaborator has received any HTTP interactions.

smtp interactions - True if Burp Collaborator has received any SMTP interactions.

You can also combine and modify conditions:

{condition} and {condition} - True if both conditions are true.

{condition} or {condition} - True if one or both of the conditions is true.

not({condition}) - True if the condition is not true.

Brackets

You can use brackets in conditions to refine the flow of logic on your checks.

For example, A or B and C creates a condition that evaluates to true if one of the following conditions is met:

A is true.

Both B and C are true.

However, (A or B) and C creates a condition that evaluates to true if both of the following conditions is met:

Either A or B is true.

C is true.

Actions

These keywords prompt Burp Scanner to perform a particular action.

Note

Some of these keywords can only be used in conjunction with certain insertion points. For more information on defining which insertion points the check logic is used on, see given...then.

send request

Sends a request including the specified information. Can be used with all scan check modes except given response.

Note

All request properties default to replacing if an action keyword is not provided. For example:

headers:

"name_of_header1": "value of header1",

"name_of_header2": "value of header2"

is the same as

replacing headers:

"name_of_header1": "value of header1",

"name_of_header2": "value of header2"

send request [called request_name]:

[appending|replacing] headers:

"name_of_header1": "value of header1",

"name_of_header2": "value of header2"

removing headers:

"name_of_header1",

"name_of_header2"

[appending|replacing] queries:

"name_of_query_1=http://portswigger.net",

"name_of_query_2=https://portswigger.net"

removing queries:

"name_of_query_1",

"name_of_query_2"

[appending|replacing] path: "/test"

removing path

[appending|replacing] method: "GET"

removing method

[appending|replacing] body: "contents of body"

removing body

Keyword

Description

Example

called

(string)

Names the request so that it can be referred to later in the check

"Example request"

appending headers:

(1-n name:value pairs)

Adds the specified header(s) to the request. If a header with the same name already exists in the request then a second header with the new value is added. You can list multiple header / value pairs

"Origin": "http://example.com"

replacing headers:

(1-n name:value pairs)

Replaces the value of the specified header(s) with a new value. If there are no headers with the specified name then a new header is appended. You can list multiple header / value pairs

"Origin": "http://example.com"

removing headers:

(1-n header names)

Removes the specified header(s) from the request. You can list multiple header names

"Origin"

appending queries:

(1-n query names and values)

Adds the specified query parameter(s) to the request URL. If a query with the same name already exists in the request then a second header with the new value is added. You can list multiple parameters

"title=example_query"

replacing queries:

(1-n query names and values)

Replaces the value of the specified query parameter(s) with a new value. If there are no queries with the specified name then a new query is appended. You can list multiple parameters

"title=example_query"

removing queries:

(1-n query names)

Removes the value of the specified query parameter(s) from the request. You can list multiple parameters

"title"

appending query_string:

(string)

Appends the specified query string to the existing query. Alternatively, if there is no existing query, adds the query string to the request

"title=value&example_title=example_value"

replacing query_string:

(string)

Replaces the entire query string with a specified value

"example_title=example_query"

removing query_string:

Removes the query string from the request

appending path:

(string)

Adds the specified path parameter(s) to the request URL

"/admin"

replacing path:

(string)

Replaces the path parameters in the URL with the specified values. Any query parameters are preserved

"/admin"

removing path

Removes all path parameters from the request.

appending method:

(string)

Adds the specified HTTP method to the request

"GET"

replacing method:

(string)

Replaces the request method with the specified value

"GET"

removing method

Removes the request method

appending body:

(string)

Appends the specified body content to the request

"body content"

replacing body:

(string)

Replaces the request body with the specified content

"body content"

removing body

Removes the request body

send request (raw)

Sends a request including the specified information as a raw HTTP request. Can be used with all scan check modes except given response.

Example

send request [called request_name]:

"GET /catalog/product?productId=2 HTTP/2

Host: ginandjuice.shop

Cookie: session=qwertyuiop

Content-Length: 2"

send payload

Sends a new request with the specified payload appended or replaced. Can be used with given insertion point only.

send payload [called payload_name]:

appending: "payload"

replacing: "payload"

Property

Description

Type

appending:

Appends the specified payload to the request's payload set.

string / variable

replacing:

Replaces the request's existing payload set with the specified payload.

string / variable

report issue

Causes Burp Scanner to report an issue. This terminates the BCheck, even if there are parts of the check that have not yet run.

For example, consider the following BCheck:

given host:

send request:

method: `GET`

headers: `Host`: `{collaborator_address}`

if dns interactions then

report issue:

severity: info

confidence: certain

end if

if http interactions then

report issue:

severity: high

confidence: certain

end if

This check looks for first DNS and then HTTP interactions resulting from its Burp Collaborator payload. However, if the check finds a DNS interaction then it performs its first report issue action and does not subsequently report any HTTP interactions, even if there are HTTP interactions present.

report issue and continue

Causes Burp Scanner to report an issue, then continue to run the BCheck. For example, consider the following BCheck:

given host:

send request:

method: `GET`

headers: `Host`: `{collaborator_address}`

if dns interactions then

report issue and continue:

severity: info

confidence: certain

end if

if http interactions then

report issue:

severity: high

confidence: certain

end if

This check looks for first DNS and then HTTP interactions resulting from its Burp Collaborator payload. If the check finds a DNS interaction then it performs its first report issue action. It then continues to run the check, and reports any subsequent HTTP interactions.

Reporting issues

You can report issues in BChecks using either the report issue or report issue and continue keywords. Both of these keyword blocks have the same properties.

name:

severity:

confidence

remediation:

detail:

Note

You must use all of the below properties in the order specified. If you attempt to change the order (for example, by using a name property after a severity property), then your BCheck will fail validation.

Property

Description

Type

name

The name of the issue.

String

severity*

The severity of the issue

[info|low|medium|high]

confidence*

The level of confidence that the issue is present

[certain|firm|tentative]

remediation

Remediation advice

String

detail

Further information on the issue

String

Issue naming

All issues reported by BChecks have an issue type of Declarative Scan Check Generated. The name of the issue is calculated as follows:

If the relevant report issue or report issue and continue block has a name keyword, then this value is displayed in Burp as the issue name.

If the relevant report issue or report issue and continue block does not have a name keyword, then the issue name is taken from the BCheck's name metadata property.

Adding a name keyword to the report issue block enables you to override the name used to report the issue in specific cases, which is useful when reporting different issue types from the same BCheck. For example, you might have a single BCheck that can report several different variations of similar bugs.

Issue consolidation

Consolidation is a process by which Burp aggregates duplicate issues to reduce noise in the UI.

Burp applies its normal consolidation rules to issues returned by BChecks if both of the following conditions are true:

Both issues are reported by the same BCheck.

Both issues have the same name, regardless of whether this name is derived from metadata or the parameter in the report issue block.

Reserved variables

These keywords refer to specific request or response properties.

Note

Make sure that you do not use these reserved property names when naming your own variables, as this will result in an error when the BCheck runs.

request / response

These keywords refer to specific request or response properties. You can refer to either:

base - The request sent and response received by Burp Scanner for the specified scan mode during crawling.

latest - The most recent request / response pair for this scan mode.

{request_name} - A specific request / response pair, named using the called keyword.

base|latest|{request_name} {

response {

status_code

headers

body

http_version

}

request {

method

url {

protocol

host

port

path

file

query

}

http_version

headers

body

}

}

Response

Property

Description

response

Returns the entire content of the response.

response.status_code

Returns the response's HTTP status code.

response.headers

Returns a list of the response's headers.

response.body

Returns the body content of the response.

response.http_version

Returns the HTTP version used in the response.

Request

Property

Description

request

Returns the entire content of the request.

request.method

Returns the HTTP method used in the request.

Example: GET

request.url

Returns the URL that the request was sent to.

Example: https://ginandjuice.shop:443/catalog/product?productId=1

request.url.protocol

Returns the request URL's protocol.

Example: https

request.url.host

Returns the host that the request was sent to.

Example: ginandjuice.shop

request.url.port

Returns the port that the request was sent over.

Example: 443

request.url.path

Returns the request URL path.

Example: /catalog/product

request.url.file

Returns the URL file (the portion of the URL after the initial slash).

Example: /catalog/product?productId=1

request.url.query

Returns the query string used in the request URL.

Example: productId=1

request.http_version

Returns the HTTP version used in the request.

Example: HTTP/2

request.headers

Returns a list of request headers.

request.body

Returns the body content of the request.

user_agent

Returns Burp's user agent.

insertion_point_base_value

Returns the base value of the specified insertion point.

Note

The insertion_point_base_value variable must be used with an insertion point control

flow keyword.

Functions

These keywords perform a specific task when called.

Note that all BCheck functions are denoted with curly braces {}.

random_str

{random_str(int)}

Returns a random string of the specified length. The length must be between 0 and 9,999,999. Entering 0 returns an empty string.

Example

{random_str(13)} // "qpald95nbjkig"

regex_replace

regex_replace (String source, String regex, String replacement)

Takes the source string and replaces any content matching the specified regex pattern with the replacement string.

Example

regex_replace ({var}, "[a-z]*@", "abc@")

In this example, assume that the value of {var} is "xyz@portswigger.net". The regex pattern matches the first part of the email address and replaces it with the replacement string to create a final output of abc@portswigger.net.

to_lower

{to_lower(string)}

Converts the specified string to lowercase.

Example

{to_lower("Carlos MONTOYA")} // carlos montoya

to_upper

{to_upper(string)}

Converts the specified string to uppercase.

Example

{to_lower("Peter weiner")} // PETER WEINER

base64_encode

{base64_encode(string)}

Encodes the specified string with base64.

Example

hello world // aGVsbG8gd29ybGQ=

base64_decode

{base64_decode(string)}

Decodes the specified string from base64.

Example

hello world // aGVsbG8gd29ybGQ=

generate_collaborator_address

{generate_collaborator_address}

Generates a new Burp Collaborator address for use within a request. You can generate multiple addresses within the same BCheck by calling {generate_collaborator_address} multiple times.

SHA1

sha1(String)

Hashes the provided input using the SHA1 hash function.

Example

sha1("Hello") // aaf4c61ddcc5e8a2dabede0f3b482cd9aea9434d

SHA256

sha256(String)

Hashes the provided input using the SHA256 hash function.

Example

sha256("Hello") // 2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824

MD5

md5(String)

Hashes the provided input using the MD5 hash function.

Example

MD5("Hello") // 5d41402abc4b2a76b9719d911017c592

Combining functions

These functions can be nested if required. For example, the following function converts a variable to lowercase and then encodes it as base64 in one action:

{base64_encode(to_lower(my_variable))}

Note

Make sure that you do not use these function names when naming variables, as this will result in an error when the BCheck runs.

Misc

Strings

Both interpolatable and literal strings are accepted:

Use double quotes ("") to denote literal strings - "delete carlos"

Use backticks (``) to denote interpolatable strings - `https://{random_str(5)}.com`

When processing multiline strings, Burp Scanner replaces line endings with \r\n and trims trailing and leading whitespaces on each line (except for spaces right after the opening quote and before the closing quote).

For example:

"__GET / HTTP/1.1__

___Host: portswigger.net_"

becomes

"__GET / HTTP/1.1

Host: portswigger.net__"

To explicitly specify trailing/leading whitespaces in interpolatable strings, use the \s character instead.

Character escaping

Use the \ character within strings to escape characters.

For example, \{var} is escaped, but {var} prints the value of var.

Regex

BChecks support Java-style regex.

"2[0-9][0-9]"

Comments

Use # to denote comment lines.

#Hello

Special characters

These characters can be used as part of an interpolatable string. For example, '\s' is interpreted as a space, but the literal string "\s" is interpreted as two separate characters.

\n - new line

\r - carriage return

\s - space

\t - tab

\b - backspace

\f - form feed

BCheck structure

There are some structure rules you need to follow in order to create valid BChecks:

Each definition must start with a metadata object.

Each definition must have exactly one given... then statement.

Conditional statements can only appear in a given... then statement.

Any define or run for each statement used must be placed after the metadata block but before the given... then statement.

Variables declared using run for each have outer scope while those declared using define have inner scope. This means that you can't use a variable declared via define in a subsequent run for each statement.
