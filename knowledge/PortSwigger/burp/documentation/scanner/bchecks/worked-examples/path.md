# Example path check

Source: https://portswigger.net/burp/documentation/scanner/bchecks/worked-examples/path
Fetched: 2026-06-28T09:16:10.886372+00:00

Support Center

Documentation

Scanner

BCheck definitions

Worked examples

Example path check

DASTProfessional

Example path check

Last updated:

June 18, 2026

Read time:

3 Minutes

This check enables Burp Scanner to see whether the target application contains old backup files. It is an example of a per-path check (that is, a check that runs once for each path scanned).

The example scan check works by attempting to locate files with potential backup file extensions.

metadata:

language: v2-beta

name: "Path-level"

description: "Tests for exposed backup files"

author: "Carlos Montoya"

run for each:

# you could add more values to this list to make the check repeat

extension =

".bak",

".back",

".backup",

".old"

given path then

if not ({base.response.status_code} is "404") then

send request called check:

replacing path: {regex_replace ({base.response.url.path}, "(.)/?$", `$1{extension}`)}

if {check.response.status_code} is {base.response.status_code} then

send request called garbage:

replacing path: {regex_replace ({base.response.url.path}, "(.)/?$", `$1.{random_str(10)}`)}

if {garbage} differs from {check} then

report issue and continue:

severity: info

confidence: firm

detail: `Backup file found at {check.request.url}`

remediation: "Ensure your backup files are not exposed."

end if

end if

end if

Step 1: Add metadata

metadata:

language: v2-beta

name: "Path-level"

description: "Tests for exposed backup files"

author: "Carlos Montoya"

The definition starts with a metadata block. For more information on available metadata properties, see the

reference documentation.

Step 2: Configure file extensions

run for each:

# you could add more values to this list to make the check repeat

extension =

".bak",

".back",

".backup",

".old"

This step configures which file extensions that Burp Scanner should look for when trying to locate old backup files.

The example code declares a variable called extension, which contains a list of potential file extensions. Burp Scanner will iterate through this list, performing one full check for each entry before moving on to the next one.

Step 3: Configure the request

given path then

if not ({base.response.status_code} is "404") then

send request called check:

replacing path: {regex_replace ({base.response.url.path}, "(.)/?$", `$1{extension}`)}

if {check.response.status_code} is {base.response.status_code} then

send request called garbage:

replacing path: {regex_replace ({base.response.url.path}, "(.)/?$", `$1.{random_str(10)}`)}

Before the request is sent, for each unique path requested, Burp Scanner checks that the status code of the base response isn't 404, which indicates that the web page can't be found.

If the status code isn't 404, Burp Scanner sends a request that uses the regex_replace function to replace the trailing slash on the end of the URL with one of the extensions named in the

extension variable.

Burp also sends an additional request that uses the regex_replace function to replace the trailing slash on the end of the URL with a random string.

Note that both requests are named using the called keyword. The request names are used in the next step to make a comparison between the responses.

Step 4: Report issues

if {garbage} differs from {check} then

report issue and continue:

severity: info

confidence: firm

detail: `Backup file found at {check.request.url}`

remediation: "Ensure your backup files are not exposed."

The next step is to report issues where appropriate.To reduce false positives, Burp Scanner uses an

if statement to look to see if the garbage response differs from thecheck response.

Burp Scanner then reports an info issue.

Related pages

BCheck definition reference.
