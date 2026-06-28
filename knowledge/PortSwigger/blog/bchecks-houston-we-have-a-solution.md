# BChecks: Houston, we have a solution!

Source: https://portswigger.net/blog/bchecks-houston-we-have-a-solution
Fetched: 2026-06-28T09:15:07.332514+00:00

BChecks: Houston, we have a solution!

Ollie Whitehouse |

Thursday, 29 June 2023 at 12:46 UTC

Burp Suite

scanning

Scripted scan checks in Burp Suite Professional are now a thing ...

tl;dr

Burp Suite Professional now has a powerful yet simple scripting language that allows you to quickly build on our world class scanning engine (see our Burp Suite Shorts videos) to create checks for anything your imagination envisages. This is much quicker than writing a BApp extension just to add a scan check.

Tada!

So we have just released BChecks into beta, and this is a quick look at the language, how it can be used and what for.

Use cases for BChecks

BChecks can be used for a variety of different solutions (and this list isn't comprehensive):

Checking for a specific vulnerability - e.g. CVE-2023-1337.

Checking for a vulnerability class - e.g. Your novel template injection technique.

Identifying technology stack components - e.g. to tingle those spidey senses.

Identifying traits which are of interest to security researchers of different types - i.e. is this a CobaltStrike server, etc.

... and then all the finds we didn't envisage, but you will.

What can it do?

To give you a flavor of what the language is capable of:

Conditional logic.

Regular expression (regex) matching.

Sending of raw HTTP requests.

Interacting with Burp Collaborator.

Programmatic trigger on discovery of insertion points to deliver your own payloads.

Raise findings (issues) with descriptions etc.

Helper functions for MD5, SHA1, SHA256 and Base64, etc.

... and more.

A quick example

As a bit of nostalgia we will revisit a vulnerability which is 22 years old - the indeed infamous CVE-2001-0537 or otherwise known as Cisco level router authentication bypass. This vulnerability was legendary at the time as it allowed you to bypass authentication and execute commands with the highest level of privilege over HTTP for Cisco IOS 11.3 to 12.2 .

The example BCheck for this issue is below:

metadata:

language: v1-beta

name: "CVE-2001-0537 CISCO Authentication Bypass"

description: "Checks for CVE-2001-0537"

author: "Ollie Whitehouse"

tags: "CVE-2001-0537 CVE"

define:

potential_path =

"/level/16/exec/show%20privilege"

given host then

send request called check:

method: "GET"

path: {potential_path}

# Checks that we get a 200 AND that the output we expect in the result

if {check.response.status_code} is "200" and "Current privilege level is" in {check.response.body} then

report issue:

severity: high

confidence: certain

detail: "Router is vulnerable to the authentication bypass vulnerability CVE-2001-0537"

remediation: "Patch to a non vulnerable version"

end if

Other examples

We have a number of other examples over in the BChecks GitHub repo.

These cover:

Blind SSRF via out-of-band detection.

Exposed git directory.

Leaked AWS tokens.

Log4Shell via out-of-band detection.

Server-side prototype pollution.

Suspicious input transformation.

These cover the various bits of the language's functionality discussed at the top of this post.

Using BChecks in audits

To use BChecks (and only BChecks) in a Burp Suite Professional audit, we can configure a custom scan configuration. The important part being the Issues Reported, as shown in the image below. Set this to BCheck generated issue:

You can create a custom scan configuration that uses only BChecks.

Configuring the scanner in this way will mean that only the BChecks will be executed during the audit phase - expediting the discovery of any vulnerabilities.

BChecks on GitHub

We have created a BChecks GitHub repository. This includes example BChecks from PortSwigger, as well as BChecks developed by the Burp Suite community. You'll also find full documentation on our website.

We look forward to accepting pull requests and celebrating your awesome work.

Burp Suite

scanning

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
