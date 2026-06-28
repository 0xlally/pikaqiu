# Example host check

Source: https://portswigger.net/burp/documentation/scanner/bchecks/worked-examples/host
Fetched: 2026-06-28T09:16:10.515606+00:00

Support Center

Documentation

Scanner

BCheck definitions

Worked examples

Example host check

DASTProfessional

Example host check

Last updated:

June 18, 2026

Read time:

2 Minutes

This check enables Burp Scanner to see whether the target application exposes a Git directory. It is an example of a per-host check (that is, a check that runs once for each host scanned).

The example scan check works by attempting to locate the host's git-config file. If the file is returned, Burp Scanner reports an issue.

metadata:

language: v2-beta

name: "Host-level"

description: "Checks for an exposed git directory"

author: "Carlos Montoya"

run for each:

potential_path =

"/.git/config",

"/.git/config~"

given host then

send request called check:

method: "GET"

path: {potential_path}

if "[core]" in {check.response.body} then

report issue:

severity: info

confidence: certain

detail: `Git directory found at {potential_path}.`

remediation: "Ensure your git directories are not exposed."

end if

Step 1: Add metadata

metadata:

language: v2-beta

name: "Host-level"

description: "Checks for an exposed git directory"

author: "Carlos Montoya"

The definition starts with a metadata block. For more information on available metadata properties, see the reference documentation.

Step 2: Configure potential paths

run for each:

potential_path =

"/.git/config",

"/.git/config~"

The next step is to configure the paths that Burp Scanner should send requests to when trying to locate the git-config file.

The example code declares a variable called potential_path, which contains a list of potential locations for the file. Burp Scanner will iterate through this list, performing one full check for each entry before moving on to the next one.

Step 3: Configure the request

given host then

send request called check:

method: "GET"

path: {potential_path}

The next step is to configure the request that Burp Scanner will send. In this case, Burp Scanner sends a GET request to one of the locations named in the potential_path variable.

Note that this request is named using the called keyword. The request name is used in the next step to identify the correct response body.

Step 4: Report issues

if "[core]" in {check.response.body} then

report issue:

severity: info

confidence: certain

detail: `Git directory found at {potential_path}.`

remediation: "Ensure your git directories are not exposed."

The next step is to report issues where appropriate. Burp Scanner uses an if statement to look for the string [core] in the body of both responses received. This string can be found in all git-config files.

If Burp Scanner finds the [core] string on a response, it reports an informational issue with certain confidence.

If there are more entries in the potential_path list that have not been checked, Burp Scanner re-runs the check for the next entry in the list.

Related pages

BCheck definition reference.
