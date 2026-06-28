# Burp Suite documentation - contents

Source: https://portswigger.net/burp/documentation/contents
Fetched: 2026-06-28T09:15:32.792517+00:00

Support Center

Documentation

Contents

DASTProfessionalCommunity Edition

Burp Suite documentation - contents

Last updated:

June 18, 2026

Read time:

42 Minutes

Documentation

Desktop editions

Getting started

System requirements

CPU cores / memory

Free disk space

Operating system and architecture

Embedded browser

Download and install

Intercepting HTTP traffic with Burp Proxy

Intercepting a request

Modifying requests in Burp Proxy

Step 1: Access the vulnerable website in Burp's browser

Step 2: Log in to your shopping account

Step 3: Find something to buy

Step 4: Study the add to cart function

Step 5: Modify the request

Step 6: Exploit the vulnerability

Setting the target scope

Reissuing requests with Burp Repeater

Sending a request to Burp Repeater

Testing different input with Burp Repeater

Running your first scan

Scanning a website

Generating a report

What next?

Continue your Burp Suite journey

Activate license

Manual activation

Mac installer

Unified installer FAQs

Is Community Edition changing?

Will this affect how I use Burp Suite?

How does this affect my license or account?

I'm an extension developer. What do I need to know?

Testing workflow

Tutorials

Setting a test scope

Adding URLs to the scope

Excluding URLs from the scope

Mapping the website

Mapping the visible surface

Before you start

Steps

Discovering hidden content

Automated discovery

Before you start

Steps

Discovering hostnames

Steps

Analyzing the attack surface

Scoping the effort to audit a website

Before you start

Steps

Identifying high-risk functionality

Before you start

Steps

Identifying supported HTTP methods

Before you start

Enumerating supported methods for a single endpoint

Enumerating supported methods for multiple endpoints

Checking for hidden inputs

Before you start

Steps

Evaluating inputs

Before you start

Steps

Manually evaluating individual inputs

Scanning inputs

Fuzzing inputs

Analyzing opaque data

Decoding data

Investigate opaque data with the Inspector

Investigate opaque data with Burp Decoder

Identifying which parts of a token impact the response

Steps

Testing for vulnerabilities

Testing authentication mechanisms

Enumerating usernames

Steps

Guessing usernames for known users

Steps

Brute-forcing passwords

Before you start

Running a dictionary attack

Running an exhaustive brute-force attack

Credential stuffing

Before you start

Steps

Brute-forcing logins

Before you start

Steps

Testing session management mechanisms

Analyzing session token generation

Before you start

Steps

Determining the session timeout

Steps

Generating a CSRF proof-of-concept

Steps

Working with JWTs

Before you start

Viewing JWTs

Editing JWTs

Adding a JWT signing key

Maintaining an authenticated session

Identifying an invalid login expression

Configuring a session handling rule

Checking the session handling rule

Testing access controls

Testing for privilege escalation

Before you start

Testing a specific endpoint

Testing across the entire site

Testing horizontal access controls

Before you start

Testing a specific endpoint

Testing across the entire site

Testing for IDORs

Steps

Testing for parameter-based access control

Before you start

Steps

Using match and replace rules

Step 1: Open the lab

Step 2: Attempt to access the admin panel

Step 3: Add a custom match and replace rule

Step 4: Try to access the admin panel again

Summary and next steps

Testing input validation

Bypassing client-side controls

Steps

SQL injection

Testing for SQL injection vulnerabilities

Steps

Scanning for SQL injection vulnerabilities

Manually fuzzing for SQL injection vulnerabilities

Cross-site scripting

Identifying reflected input

Steps

Scanning for reflected inputs

Identifying reflected input manually

Next steps

Testing for DOM XSS with DOM Invader

Before you start

Steps

Related pages

Testing for web message DOM XSS with DOM Invader

Before you start

Steps

Related pages

Testing for reflected XSS manually

Before you start

Steps

Related pages

Testing for stored XSS

Steps

Bypassing XSS filters

Before you start

Steps

Testing for blind XSS

Steps

Related pages

Testing for prototype pollution with DOM Invader

Before you start

Steps

OS command injection

Testing for command injection vulnerabilities

Steps

Scanning for command injection vulnerabilities

Manually testing for command injection vulnerabilities

Testing for asynchronous OS command injection vulnerabilities

Steps

Exploiting OS command injection vulnerabilities to exfiltrate data

Before you start

Steps

XXE injection

Testing for XXE injection vulnerabilities

Steps

Scanning for XXE vulnerabilities

Manually testing for XXE vulnerabilities

Testing for blind XXE injection vulnerabilities

Steps

Scanning for blind XXE injection vulnerabilities

Manually testing for blind XXE injection vulnerabilities

Testing for directory traversal vulnerabilities

Steps

Scanning for directory traversal vulnerabilities

Fuzzing for directory traversal vulnerabilities

Testing for clickjacking

Steps

Testing for SSRF vulnerabilities

Testing for SSRF

Steps

Testing for blind SSRF

Steps

Testing for WebSocket vulnerabilities

Manipulating WebSocket messages

Steps

Manipulating WebSocket handshakes

Steps

Working with GraphQL in Burp Suite

Viewing and modifying GraphQL requests

Accessing GraphQL API schemas using introspection

Complementing manual testing with Burp Scanner

Scanning specific requests

Scanning user-defined insertion points

Scanning a single insertion point

Scanning multiple insertion points

Scanning non-standard data structures

Store HTTP traffic for review

Tools

Dashboard

Task list

Launching new tasks

Pausing and resuming running tasks

Disabling traffic capturing for live tasks

Bottom dock

Burp's browser

Manual testing with Burp's browser

Scanning websites with Burp's browser

Health check for Burp's browser

Burp Proxy

Proxy intercept

Getting started

Controls

Intercepted messages table

Adding annotations

Message display

Protocol

HTTP history

Managing the HTTP history

Viewing a request

Filter settings

Settings mode

Script mode

Adding annotations

Filtering with scripts

Keyboard shortcuts

Loading scripts from your library

Creating custom scripts

Converting filter settings to scripts

Creating your script

Example script

Adding custom columns

Keyboard shortcuts

Loading scripts from your library

Creating custom scripts

WebSockets history

Managing the WebSockets history

Viewing a request

Filter settings

Settings mode

Script mode

Adding annotations

Filtering with scripts

Keyboard shortcuts

Loading scripts from your library

Creating custom scripts

Converting filter settings to scripts

Creating your script

Example script

Adding custom columns

Keyboard shortcuts

Loading scripts from your library

Creating custom scripts

Match and replace

Adding match and replace rules

Creating rules

Settings mode

Using regex syntax

Matching multi-line regions

Using regex groups in back-references and replacement strings

Script mode

Creating rules with scripts

Keyboard shortcuts

Loading scripts from your library

Creating custom scripts

Testing rules

Managing CA certificates

Exporting and importing the CA certificate

Creating a custom CA certificate

Invisible proxying

Repeater

Working with HTTP messages

HTTP Repeater tab

Adding notes for HTTP Repeater tabs

AI features in Repeater

Burp AI in Repeater

Running a Burp AI task in Repeater

Managing context

Adding highlighted areas

Adding notes

Removing items

Reviewing task results

Task progress

Logger

Ending a task

Trust and transparency in Burp AI

Generating AI-powered explanations

Generating an AI-powered explanation

Managing explanations

Custom actions

Creating custom actions

Testing custom actions

How Burp selects test data

Loading custom actions

Running custom actions

Running AI-powered custom actions

Managing custom actions

Sending grouped HTTP requests

Sending requests in sequence

Sending over a single connection

Sending over separate connections

Send in sequence prerequisites

Sending requests in parallel

Send in parallel prerequisites

Working with WebSocket messages

WebSocket Repeater tab

Managing tabs

Tab groups

Managing tab groups

Creating a new tab group

Editing existing groups

Closing tab groups

Configuring tab-specific settings

Intruder

Getting started

Tutorial

Step 1: Access the lab

Step 2: Try to log in

Step 3: Set the payload position

Step 4: Select an attack type

Step 5: Add the payloads

Step 6: Start the attack

Step 7: Look for any irregular responses

Step 8: Study the response

What next?

Learn more about Burp Intruder

Configure attack

Positions

Attack types

Sniper attack

Battering ram attack

Pitchfork attack

Cluster bomb attack

Payload types

Payload configuration

Simple list

Runtime file

Custom iterator

Character substitution

Case modification

Recursive grep

Illegal Unicode

Character blocks

Numbers

Dates

Brute forcer

Null payloads

Character frobber

Bit flipper

Username generator

ECB block shuffler

Extension-generated

Copy other payload

Collaborator payloads

Payload lists

Using predefined payload lists

Placeholders

Processing placeholders

Processing

Configuring processing rules

Types of processing rules

Configuring payload encoding

Resource pools

Creating resource pools

Resource pool settings

Moving tasks between resource pools

Settings

Save attack

Request headers

Error handling

Attack results

Auto-pause attack

Grep - match

Grep - extract

Grep - payloads

Redirections

HTTP/1 connection reuse

HTTP version

Managing tabs

Results

Editing attacks

Saving results

Closing attacks

Viewing results

Viewing a request

Analyzing results

Filtering results

Capture filter

Capture filter settings

Managing the capture filter settings

View filter

View filter settings

Managing the view filter settings

Workflow

Add payload position

Clear payload positions

Scan

Send to...

Show response in browser

Record an issue

Request in browser

Generate CSRF PoC

Add to site map

Request item again

Define extract grep from response

Copy as curl command

Add comment

Highlight

Copy links

Save item

Uses

Enumerating identifiers

Step 1: Find a request

Step 2: Set a payload position

Step 3: Set a payload type

Step 4: Analyze the results

Use cases

Fuzzing

Step 1: Set the payload positions

Step 2: Set the payload type

Step 3: Set the match grep

Step 4: Analyze the results

Harvesting data

Step 1: Find a request

Step 2: Set a payload position

Step 3: Set a payload type

Step 4: Set an extract grep

Step 5: Analyze the results

Use cases

Target

Site map

Accessing the site map

URL view

URL view icons

Contents pane

Requests and responses

Issues pane

Editing the Issues pane

Getting started

Tutorial

Step 1: Access the lab

Step 2: Go to the site map

Step 3: Update the site map

Step 4: Filter the displayed information

Step 5: Set the target scope using the site map

Workflow tools

Add to scope / Remove from scope

Send to

Scan

Show response in browser

Record an issue

Request in browser

Engagement tools

Compare site maps

Add notes / Highlight

Expand / collapse branch / requested items

Delete items

Copy URLs

Copy as curl command

Copy links

Save items

Show new site map window

Filtering the site map

Settings mode

Script mode

Site map annotations

Filtering the site map with scripts

Keyboard shortcuts

Loading scripts from your library

Creating custom scripts

Converting filter settings to scripts

Creating your script

Example script

Comparing site maps

Site map sources

Request matching

Response comparison

Comparison results

Viewing comparison results

Interpreting comparison results

Site map layout

Contents and issues layout

Request and response layout

Adding a new site map window

Scope

URL-matching rules

Normal scope control

Advanced scope control

Crawl paths

Accessing the Crawl paths view tab

Viewing crawl paths

Example crawl path

Viewing HTTP requests

Viewing issues

Viewing outlinks

Issue definitions

Manual Application mapping

Reviewing unrequested items

Analyzing the attack surface

Inspector

Configuring the Inspector layout

Request attributes

Viewing HTTP message data in the Inspector

Automatic decoding

HTTP/2 headers and pseudo-headers

Selecting a substring

Getting started with the Inspector

Tutorial

Step 1: Access the lab

Step 2: Log in to a user account

Step 3: Use the Inspector to examine the request

Step 4: Use the Inspector to edit the cookie

Step 5: Using the selection widget

Learn more about the Inspector

Modifying requests

Adding new items to a request

Removing items from a request

Reordering items in a request

Editing the name or value of an item

Injecting newlines

Injecting other non-printing characters

Copying items from the Inspector

Message editor

Message analysis toolbar

Raw tab

Pretty tab

Hex tab

Render tab

GraphQL tab

Additional tabs

Extension-specific tabs

Actions menu

Other ways of using the message editor

HTTP/2 messages in the message editor

HTTP/0.9 responses in the message editor

Context-specific actions

Record an issue

Sharing messages in collections

Text editor

Syntax analysis

Pretty printing

Hide headers

Line-wrapping

Non-printing characters

Text editor hotkeys

Quick search

Collaborator

Generating payloads

Viewing results

Exporting results

Getting started

Step 1: Access the lab

Step 2: Browse the target site

Step 3: Send an interesting request to Repeater

Step 4: Inject a Collaborator payload into the request

Step 5: Poll for interactions

Summary

What next?

Logger

Getting started with Logger

Step 1: Access the lab

Step 2: View requests on the Logger tab

Step 3: Audit a request with Burp Scanner

Step 4: Examine the requests made by Burp Scanner

Step 5: Filter the log

Step 6: Disable and clear the Logger history

Learn more about Logger

Working with Logger entries

Managing log entries

Adding custom columns

Viewing requests and responses

Filtering log entries

Annotating log entries

Logger workflow tools

Adding custom columns

Keyboard shortcuts

Loading scripts from your library

Creating custom scripts

Example script

Filtering Logger

Capture filter

Settings mode

Capture limit

Capture by request type

Capture by MIME type

Capture by status code

Capture by tool

Capture by search term

Session handling

Limit request/response size

Script mode

Capture filter with scripts

Keyboard shortcuts

Loading scripts from your library

Creating custom scripts

Converting filter settings to scripts

Creating your script

Example script

View filter

Settings mode

Filter by request type

Filter by MIME type

Filter by status code

Filter by tool

Filter by search term

Filter by file extension

Filter by annotation

Script mode

View filter with scripts

Keyboard shortcuts

Loading scripts from your library

Creating custom scripts

Converting filter settings to scripts

Creating your script

Example script

Task Logger

Sequencer

Getting started

Token sample

Configuring a live capture of tokens

Selecting a token location

Manually loading tokens

Live capture

Results

Summary

Overall result

Effective entropy

Reliability

Sample

Analysis result tabs

Individual tests

Character set

Bit conversion

Analysis settings tab

Tests

How the tests work

Character-level tests

Character count analysis

Character transition analysis

Bit-level analysis

FIPS test results

FIPS monobit test

FIPS poker test

FIPS runs test

FIPS long runs test

Spectral tests

Correlation test

Compression test

DOM Invader

Key features

Enabling DOM Invader

Testing for DOM XSS

Injecting a canary

Injecting a canary into multiple sources

Identifying controllable sinks

Determining the XSS context

Studying the client-side code

Testing for DOM XSS using web messages

Enabling web message interception

Identifying interesting web messages

Automated web message analysis

Message details

Origin accessed

Data accessed

Source accessed

Replaying web messages

Generating a proof of concept

Testing for client-side prototype pollution

Enabling prototype pollution

Detecting sources for prototype pollution

Manually confirming sources for prototype pollution

Scanning for prototype pollution gadgets

Generating a proof-of-concept exploit

Testing for DOM clobbering

Enabling DOM clobbering

Settings

Main

Enable DOM Invader

Postmessage interception

Customizing sources and sinks

Attack types

Prototype pollution

DOM clobbering

Web message settings

Postmessage origin spoofing

Canary injection into intercepted messages

Filter messages with duplicate values

Generate automated messages

Detect cross-domain leaks

Prototype pollution settings

Scan for gadgets

Auto-scale amount of properties per frame

Scan nested properties

Query string injection

Hash injection

JSON injection

Verify onload

Remove CSP header

Remove X-Frame-Options header

Scan each technique in separate frame

Disabling prototype pollution techniques

Misc

Message filtering by stack trace

Auto-fire events

Redirection prevention

Add breakpoint before redirect

Inject canary into all sources

Configuring callbacks

Remove Permissions-Policy header

Canary

Copying the canary

Changing the canary

Clickbandit

Setting up Burp Clickbandit

Running an attack

Reviewing an attack

Comparer

Carrying out comparisons

Controls

Results

Decoder

Carrying out transformations

Operations

Engagement tools

Target analyzer

Content discovery

Control tab

Config tab

Target

Filenames

File extensions

Discovery engine

Site map tab

Generate CSRF PoC

CSRF PoC options

Manual testing simulator

Infiltrator

How Burp Infiltrator works

Installing Burp Infiltrator

Non-interactive installation

Configuration options

Organizer

Sending messages to Organizer

Collections

Browsing messages in Organizer

Inspecting a message in Organizer

Exporting results

Annotating items

Statuses in Organizer

Highlighting in Organizer

Notes in Organizer

Filtering items

Collections

Creating new collections

Moving messages into collections

Copying messages into collections

Managing collections

Sharing collections

Importing collections

Importing collections manually

Command palette

Command list

Search

Text search

Find comments and scripts

Find references

Context menu

Menu options

Filter settings

Filter settings

Managing the filter settings

Extending Burp

Bambdas

Custom scan checks

Extensions

Extensions

Viewing requests sent by Burp extensions using Logger

Step 1: Send requests using an extension

Step 2: Go to the Logger tab

Step 3: Filter the log

Step 4: View individual requests

Summary

Installing extensions

BApp Store

Finding extensions

Evaluating extensions

Installing extensions

Manual install

Manually installing a custom extension

Manually installing a BApp Store extension

Managing extensions

Using AI extensions

Using AI credits

Checking AI credit use

Enabling AI for extensions

Data and privacy

Troubleshooting

Installing extensions

Step 1: Check your internet connection

Step 2: Configure an upstream proxy

Step 3: Identify and resolve an intercepting proxy

You need to update Burp

You need to configure Jython or JRuby

You need to upgrade to Burp Suite Professional

Step 1: Update Burp

Step 2: Visit the extension's repository

Step 3: Use AI to review the extension's code

Step 4: Report an issue or suggest a fix to the extension's author

Option 2: Suggest a fix

Performance issues

Step 1: Disable unused extensions

Step 2: View the performance impact estimate for particular extensions

Step 3: Manually test extensions

Creating

Exploring your idea

Choosing the right extensibility option

Choosing a language

Creating AI-powered extensions

Vibe coding extensions with AI

Handling kettled HTTP/2 requests in extensions

Custom editor best practice

Development environment setup

Using the starter project

Prerequisites

Step 1: Download the template

Step 2: Open the project

[Optional] Step 3: Rename the project

[Optional] Step 4: Confirm correct setup

[Optional] Step 5: Enable LLM support

Next steps

Understanding the starter project

Manual setup

Prerequisites

Step 1: Create a new project

Step 2: Add the Montoya API dependency

Gradle configuration

Maven configuration

Step 3: Create your extension class

Step 4: Confirm correct setup

[Optional] Step 5: Enable LLM support

Claude Code support

Other LLM support

Next steps

Writing first extension

Before you begin

Step 1: Implement the extension interface

Step 2: Set the extension name

Step 3: Add a context menu item

Step 4: Add a custom tab

Complete code

Next steps

Tutorials

Before you begin

Adding a settings panel

Step 1: Create a panel

Step 2: Define your settings

Step 3: Register the settings panel

Step 4: Access user-configured setting values

Step 5: Use the setting values

[Optional] Help users find your settings panel

Complete code

Adding a hotkey

Step 1: Register the hotkey

Step 2: Create the handler

Step 3: Implement your action

Step 4: Register the hotkey

Complete code

Setting up remote debugging

Prerequisites

Step 1: Configure a remote debugging session

Step 2: Start Burp with remote debugging enabled

Step 3: Attach your debugger to Burp

Troubleshooting

Using a remote debugger

Prerequisites

Step 1: Set breakpoints

Setting conditional breakpoints

Setting logging breakpoints

Step 2: Trigger your extension in Burp

Troubleshooting

Step 3: Inspect stack frames and variables

Review the call stack

Inspect variable values

Step through the code

View errors in the terminal

Step 4: Modify your extension and repeat

Step 5: Finish the debug session

Sharing your extension

Loading in Burp

Step 1: Build the JAR file

Gradle build command

Maven build command

Including third-party dependencies

Step 2: Load the JAR file in Burp

Reloading your extension

Reload automatically when file rebuilt

Reload manually

Sharing your extension

BApp Store acceptance criteria

Submitting extensions to the BApp Store

Step 1 - Check the acceptance criteria

Step 2 - Submit your extension

Step 3 - We review your extension

Maintaining extensions on the BApp Store

Using AI to support extension maintenance

Creating AI extensions

AI credits

Examples

Best practices for writing AI extensions

Declare AI support and check availability

Mitigate prompt injection attacks

Optimize AI requests for efficiency and security

Use effective prompts

Use lower temperatures for better accuracy

Handle exceptions gracefully

Use an executor service where necessary to avoid blocking threads

Integrating with third-party LLM providers

Developing AI features in extensions

On this page

Checking AI availability

Configuring the extension to enable AI

Verifying AI availability

Sending prompts and handling responses

Single-shot prompts

Building multi-turn conversations

Handling exceptions

Setting the temperature

Extender API examples (Legacy)

Bambdas

Feature specific instructions

Filtering tables

Adding custom columns

Adding custom scan checks

Adding custom actions

Adding match and replace rules

Managing scripts

Importing scripts

Creating scripts

Exporting scripts

Managing scripts

Importing Bambdas

Importing the full GitHub repository

Updating your scripts

How Burp overwrites scripts

Creating scripts

Creating scripts in the Bambda library

Creating scripts from specific Burp tools

Filtering tables

Adding custom columns

Adding custom scan checks

Adding custom actions

Adding match and replace rules

Writing custom actions

Worked example

Step 1: Get the response body

Step 2: Check the response body for the CSRF token

Step 3: Extract and process the token

Step 4: Log the result

Step 5: Handle the situation where no token is found

Writing guide

On this page

API access

Step 1: Accessing request and response data

Retrieving the full request or response

Extracting specific parts of the message

Extracting user-selected content

Extracting the HTTP service

Handling empty or missing content

Step 2: Processing data

Using AI to analyze messages

Modifying editor content

Replacing selected content in the editor

Step 3: Logging and using the data

Logging to output

Sending data to other Burp tools

Logging data to a file

Example use cases

Decoding data

Encoding data

Sending modified requests

Sending repeated requests to test for race condition vulnerabilities

Fetching external data

Running shell commands

Developing AI features

Sending prompts and handling responses

Setting the temperature

Handling exceptions

AI best practices

Mitigate prompt injection attacks

Optimize AI requests for efficiency and security

Use effective prompts

Use lower temperatures for better accuracy

Submitting scripts to GitHub

Step 1: Add documentation to your script

Step 2: Format and refine your script

Step 3: Export your script from Burp

Step 4: Validate and submit your script

Troubleshooting

Compilation errors

Runtime errors

Debugging scripts

Custom scan checks

Managing custom scan checks

Importing custom scan checks

Creating custom scan checks

Exporting custom scan checks

Managing custom scan checks

Importing custom scan checks

Importing full GitHub repositories

Updating your custom scan checks

How Burp overwrites script-based checks

How Burp overwrites BCheck-based checks

Creating custom scan checks

Creating script-based checks

Creating BCheck-based checks

Writing guide

Choosing the right check type

Active and passive checks

When checks run during a scan

Using Collaborator in checks

Structure of a custom scan check

Validating that a response exists

Performing checks

Modifying requests (Active checks)

Inspecting traffic (Active and passive checks)

Reporting results

Breakdown of an audit issue

Setting the URL

Reporting multiple issues

Returning an empty result

Collaborator-enabled checks

Passive scan check example

Step 1: Make sure there's a response

Step 2: Check for the CSP header

Step 3: Build the issue variables

Step 4: Return an issue if no CSP header is present

Step 5: Return an empty result when the header is present

Active scan check example

Step 1: Make sure there's a response

Step 2: Create random origins

Step 3: Loop through each origin

Step 4: Send the modified requests

Step 5: Inspect the response headers

Step 6: Return an issue if the origin is reflected

Step 7: Return no issue when the header is present

Testing custom scan checks

Testing a custom check in the editor

Managing test cases

Running a test scan

Running scans

Scanning web applications

Running a full crawl and audit

Step 1: Configure scan type

Step 2: Configure AI scan enhancements (optional)

Configuring AI credit behavior

Step 3: Configure scan details

Step 4: Select a scan configuration

Step 5: Configure application logins (optional)

Step 6: Select a resource pool (optional)

Scanning specific HTTP messages

Configuring an audit of specific HTTP messages

Configuring scans

Setting up scan configurations

Saving scan configurations

Saving complete scan configurations

Saving crawl-only or audit-only configurations

Loading scan configurations

Importing scan configurations

How Burp applies scan configurations

Setting the scan scope in Burp Suite Professional

URLs to scan

Fragment handling

Protocol settings

Advanced scan parameters

Items to scan

Configuring application logins

Adding usernames and passwords

Adding login credentials

Editing existing login credentials

Testing login functions

Adding recorded login sequences in Burp Suite Professional

Generating recorded login sequences using AI

Adding an AI-powered recorded login

Privacy and security in AI-powered recorded logins

Adding manually recorded login sequences

Editing existing recorded logins

Managing application logins using the configuration library

Managing resource pools for scans

Creating new resource pools

Reassigning resource pools

Scanning APIs

Step 1: Configure scan type

Step 2: Upload API definition

Step 3: Review and configure the API details

Viewing and configuring authentication

Step 4: Select a scan configuration

Step 5: Select a resource pool

Configuring authentication

Detected authentication methods

Adding authentication methods

Basic authentication

Bearer token

API key / Custom token

Fixed API key / Custom token authentication method

Dynamic API Key / Custom token authentication method

Editing authentication credentials / methods

How Burp applies authentication credentials

Conflicts between manually added methods

Conflicts between detected methods and manually added methods

Adding custom scan checks

Managing the custom scan checks table

Adding extension scan checks

Managing the extension scan checks table

Live tasks

Types of live task

Live task scope

Scan configuration and resource pools

Creating live tasks

Task execution settings

Task auto-start

Resource pools

Viewing scan and live task results

Summary

Audit items

Audit phase indicators

Insertion points

Tree view

Nested insertion points

Insertion points information

Insertion point statuses

Issues

Analyzing issue activity

Managing issues

Event log

Audit log

Viewing audit activity

Analyzing audit log activity

Managing audit log items

Live crawl view

Exploring issues with AI

How Explore Issue works

Running an explore task

Reviewing results

Task progress

Logger

Ending an explore task

Trust and transparency in Explore Issue

Reporting scan results

Report settings

Report format

Issue details

HTTP messages

Selecting issue types

Report details

Manually creating issues for reports

To create an issue:

Adding multiple request and response pairs to an issue

To add request / response pairs to a manually created issue:

Burp AI

Getting started with AI in Burp

AI features in Burp

Burp AI in Repeater

Explore Issue

Explainer

Broken access control false positive reduction

AI-powered recorded logins

AI-powered extensions

AI-powered custom actions in Burp Repeater

Security and privacy

AI credits

Buying AI credits

Using AI credits

Extensions

Troubleshooting AI connectivity

Common connectivity problems

Step 1: Check your internet connection

Step 2: Configure an upstream proxy

Step 3: Identify and resolve an intercepting proxy

Prompting best practices with Burp AI

Writing effective prompts

Be specific and goal-oriented

Use context strategically

Stay focused

Guide the format

Include scenario details

Reference known security categories

Write complete prompts

Example prompts for common testing scenarios

Explaining a vulnerability

Reviewing HTTP traffic

Investigating access control

Interpreting unusual responses

Generating test payloads

Summarizing findings

Project files

Opening an existing project file

Pause Automated Tasks

Trust this project file

Creating project files

Opening a project file

Managing project files

Saving a copy of a project

Saving the Burp Collaborator identifier

Importing project files

Recovering data from corrupted project files

Settings

User and project settings

Finding settings

Managing settings

Settings pages

Key settings

Target scope

Platform-level authentication

Session handling rules and macros

Schedule tasks

HTTP message appearance

Tools

Proxy

Proxy listeners

Binding

Request handling

Certificate

TLS Protocols

HTTP

Request and response interception rules

Adding an interception rule

Modifying intercepted messages

WebSocket interception rules

Response modification rules

HTTP and WebSocket match and replace rules

TLS pass through

Adding TLS passthrough targets

Applying TLS passthrough to out-of-scope items

Default Proxy history message display

Proxy history logging

Default Proxy interception state

Miscellaneous

Repeater

Connections

Message modification

Redirects

Follow redirects

Process cookies in redirects

Use selected protocol for cross-domain redirects

Streaming responses timeout

Default tab group

Tab view

Sequencer

Live capture

Token handling

Token analysis

Comparer

Sync Comparer results view

Intruder

Default Intruder side panel layout

Automatic payload placement

New tab configuration

Behavior when closing result windows

Payload list location

Burp's browser

Browser data

Browser running

Project

Collaborator

Scope

Target scope

Out-of-scope request handling

Tasks

Resource pools

New task auto-start

Schedule tasks

Automatic backup

Logging

Sessions

Session handling overview

Session handling rules

Session handling tracer

Cookie jar

Macros

Session handling rule editor

Rule description

Rule actions

Use cookies from the session handling cookie jar

Set a specific cookie or parameter value

Check session is valid

Make requests to validate session

Inspect responses to determine session validity

Define behavior dependent on session validity

Run a macro to obtain a new valid session

Prompt for in-browser session recovery

Run a post-request macro

Invoke a Burp extension

Set a specific header value

Replace matching part of the request

Tools scope

URL scope

Parameter scope

Macros

Record macro

Configure item

Parameter handling

Custom parameter locations in response

Re-analyze macro

Test macro

Network

Connections

Platform authentication

Timeouts

Upstream proxy servers

SOCKS proxy

DNS

Preferred IP version for DNS resolution

Hostname resolution overrides

TLS

TLS negotiation

Client TLS certificates

Server TLS certificates

Custom CA certificates

Java TLS settings

HTTP

Allowed redirect types

Streaming responses

Status 100 response handling

HTTP/1

HTTP/2

UI

Message editor

Message editor request and response views

HTTP message display

Character sets

HTML rendering

HTTP message search

Hide request headers

Hide response headers

Side panel

Default side panel layout

Inspector widgets

Hotkeys

Display

Appearance

Scaling

Title bar appearance

Table appearance

Learn tab display

Suite

REST API

Enabling the REST API

Service URL

API key

Updates

Becoming an early adopter

Performance

Performance feedback

Logging exceptions to a local directory

Maximum memory usage

When to adjust the limit

Temporary files location

Startup behavior

Automated tasks on startup

Untrusted project files

Shutdown behavior

Shutdown confirmation

AI

Extensions

Startup behavior

Load behavior

Java environment

Python environment

Ruby environment

Configuration library

Adding a custom configuration

Importing custom configurations

Exporting custom configurations

Managing custom configurations

Configuration files

Response extraction rules

Customizing Burp's layout

Customizing Burp's top-level tabs

Arranging top-level tabs

Hiding top-level tabs

Restoring the default top-level tab layout

Customizing Burp's tables

Customizing tables with scripts

Mobile testing

Configuring a mobile device

Configuring an iOS device to work with Burp Suite Professional

Step 1: Configure the Burp Proxy listener

Step 2: Configure your device to use the proxy

Step 3: Install a CA certificate on your iOS device

Step 4: Test the configuration

Configuring an Android device to work with Burp Suite Professional

Step 1: Configure a dedicated proxy listener in Burp

Step 2: Configure your device to proxy traffic through Burp

Step 3: Add Burp's CA certificate to your device's trust store

Step 4: Test the configuration

Troubleshooting for mobile devices

I can't access HTTPS URLs on iOS even after installing Burp's CA certificate

HTTP/2

Background concepts

Default protocol

Keeping track of which protocol you're using

Changing the protocol for a request

Kettled requests

What can cause a request to become kettled?

Unkettling a request

Kettled requests and extensions

HTTP/2 settings

Changing the default protocol

Repeater options for HTTP/2

Enforce protocol choice on cross-domain redirections

Enable HTTP/2 connection reuse

Strip Connection header over HTTP/2

Allow HTTP/2 ALPN override

Disabling HTTP/2 for proxy listeners

Upcoming enhancements for HTTP/2 in Burp

Increased support for kettled requests

HTTP/2 basics for Burp users

Binary protocol

Frames

Message length

Header capitalization

Pseudo-headers

Normalization

What normalization is performed?

Why can't I move the Host header?

Sending requests without any normalization

Performing HTTP/2-exclusive attacks

Injecting newlines into headers

Troubleshooting

Troubleshooting

Troubleshooting performance issues

Optimize memory usage

Disabling extensions

Adjusting Burp's memory usage

Using a disk-based project

Check the minimum system requirements

Identify potential bottlenecks: CPU, memory, and network

Optimize CPU usage

Disabling pretty printing

Disabling JavaScript analysis

Configuring your scans for performance

Narrowing the scope of your scans

Scanning a single protocol

Optimize network usage

Reducing concurrent scans

Configuring resource pools

Launch from the command line

Checking your Java version

Launching the Burp Suite JAR

Command line arguments

Setting Java options

Creating a user.vmoptions file

Specifying options

External browser configuration

Check proxy listener is active

Configuring Chrome to work with Burp Suite - Windows

Configuring Chrome to work with Burp Suite - MacOS

Firefox

Safari

Check your browser configuration

Installing Burp's CA certificate

Installing Burp's CA certificate on a mobile device

Why do I need to install Burp's CA certificate?

In-browser interface

Chrome

Removing Burp's CA certificate from Firefox

Chrome

Installing Burp's CA certificate in Chrome - Windows

Removing the CA certificate from Windows

Installing Burp's CA certificate in Chrome - Linux

Removing the Burp Suite CA certificate

Installing Burp's CA certificate in Chrome - MacOS

Removing the Burp Suite CA certificate

Chrome

Removing Burp's CA certificate from Safari

Troubleshooting

Check that Burp is running

Check your proxy listener is active

Try a different port

What next?

Burp Suite DAST

Setting up Burp Suite DAST

Setting up a Cloud instance

Step 1: Assign your primary administrator

Step 2: Launch your instance as the primary administrator

Setting up a self-hosted instance

Planning to deploy Burp Suite DAST

Decide on your subscription

Choose a deployment method

Choose your preferred architecture

Plan your database setup

Review the system requirements

Plan your network and firewall setup

Prepare your organization

Which deployment method is right for me?

Burp Suite DAST system requirements

Concurrent scans

Setup guide: Standard instance

Unattended installation

Architecture overview (Standard)

DAST server

Web server

Database

Services

Scans and scanning machines

Single vs. multi-machine architecture

Single machine architecture

Multi-machine architecture

Requirements

Network and firewall settings

Configuring your network and firewall settings (Standard)

Configuring a single-machine architecture

Configuring a multi-system architecture

System requirements for standard instances

General requirements

Supported operating systems

Single-machine architecture

Machine hardware requirements

Multi-machine architecture

System requirements for your external database (Standard)

Database size requirements

Supported database versions

Setting up the external database (Standard)

Database setup scripts

PostgreSQL

Oracle

MariaDB / MySQL

Microsoft SQL Server

Authentication mode

Additional configuration for Microsoft SQL Server

Database connection URL format

Troubleshooting for MySQL databases

Multiple primary keys defined

Distributing the public key manually

Prerequisites for a standard installation

Port

TLS certificate

Installation location

System user

Scanning machine requirements

Database setup script

Installing Burp Suite DAST (Standard)

Before installation

Step 1: Download the installer

Step 2: Extract and run the installer

Step 3: Choose an install location

Step 4: Select the components to install

Step 5: Specify a logs directory

Step 6: Specify a data directory

Step 7: Select a user to run processes

Step 8: Select database options

Step 9: Specify a web server port

Step 10: Specify a database backups directory

After installation

Configuring Burp Suite DAST (Standard)

Uploading a TLS certificate

Configuring TLS cipher suites

Configuring database details

Configuring admin user details

Activating your license (Standard)

Configuring your web server (Standard)

Enabling TLS

Deploying additional scanning machines

Network and firewall settings

Setting up a new scanning machine

Authorizing a new scanning machine

Setup guide: Kubernetes instance

Kubernetes architecture overview

DAST server

Web server

Database

Scans and scanning resources

Kubernetes scanning resources overview

How does scanning work on Kubernetes?

Configuring scanning resources

Support scope for Kubernetes instances

PortSwigger Kubernetes support scope

Not supported

Kubernetes customer responsibilities

Configuring your environment network and firewall settings (Kubernetes)

Configuring your instance

System requirements for a Kubernetes instance

Container system requirements

Minimum requirements for general container limits

Minimum requirements for a web server container

Minimum requirements for a DAST server container

Minimum requirements for a scan container

System requirements for the external database (Kubernetes)

Supported database versions

Database hardware requirements

Setting up your external database (Kubernetes)

Database setup scripts

PostgreSQL

Oracle

MariaDB / MySQL

Microsoft SQL Server

Authentication mode

Additional configuration for Microsoft SQL Server

Database connection URL format

Troubleshooting for MySQL databases

Multiple primary keys defined

Distributing the public key manually

Deploying Burp Suite DAST to Kubernetes

Setting up a suitable Kubernetes cluster

Using the reference template

Installing the application (Kubernetes)

Downloading the Helm chart

Providing custom values for the Helm chart

Note for Oracle users

Adding a TLS certificate

Configuring TLS cipher suites

Configuring the database details

Using the Helm chart

Installing using a pre-existing values file

Creating the admin user (Kubernetes)

Activating your license (Kubernetes)

Configuring your web server (Kubernetes)

Enabling TLS

Setup guide: CI-driven scans with no dashboard

Running a basic CI-driven scan with no dashboard

Before you start

System requirements

Running a scan

Scan results

Remediation advice

Evidence

Configuring CI-driven scans

CI-driven scan integration examples

Configuring CI-driven scans with no dashboard

Creating a configuration file for a CI-driven scan with no dashboard

Mandatory settings

Common requirements

Web apps

APIs

Proxy settings

Defining the scope

Authentication

Login credentials (web apps only)

Recorded logins (web apps only)

API authentication (APIs only)

API key authentication

HTTP authentication types

Selecting a built-in scan configuration

Configuring connection settings

Specifying report format

Ignoring specific issues

Setting the threshold

Configuring output detail level

Adding a configuration file to a CI-driven scan with no dashboard

Example integrations for CI-driven scans with no dashboard

Integrating a CI-driven scan with no dashboard with Jenkins

Before you start

Jenkins server requirements

Configuring the Jenkins pipeline

Setting the configuration of your scan

Creating the Jenkinsfile

Viewing scan results in Jenkins

Remediation advice

Evidence

Integrating a CI-driven scan with no dashboard with TeamCity

Before you start

TeamCity agent requirements

Creating the settings file

Setting the configuration of your scan

Configuring the TeamCity pipeline

Viewing scan results in TeamCity

Remediation advice

Evidence

Integrating a CI-driven scan with no dashboard with GitHub Actions

Migrating from Linux to Cloud

Prerequisites

Export your data

Import your data

Scan schedule behavior after migration

Migrating from Windows to Cloud

Prerequisites

Export your data

Import your data

Scan schedule behavior after migration

Next steps after setup

Set up your email server

Set up integrations

Set up SSO

Import sites in bulk

Trial setup guide

Install with the default options

Activating your license

Run your first scan

Analyze your scan's results

Burp Suite DAST user guide

Getting started with Burp Suite DAST

Step 1: Set up your users

Step 2: Add the sites you want to scan

Step 3: Set up a scan configuration

Step 4: Schedule your scans

Step 5: View scan results

What else can I do with Burp Suite DAST?

Extensions in Burp Suite DAST

Extension library

Adding extensions to Burp Suite DAST

Prerequisite permissions for adding extensions

Adding BApps to Burp Suite DAST

Adding custom extensions to Burp Suite DAST

Requirements for extensions

Adding a custom extension

Adding BChecks to Burp Suite DAST

Managing extensions in Burp Suite DAST

Viewing extension details

Updating an extension

Deleting an extension

Managing users and permissions

Managing users locally

Using SSO

Role-based access control

Vertical segregation of permissions

Horizontal segregation of permissions

Adding local users

Creating an API user

Enabling single sign-on for Burp Suite DAST

Creating local groups for SAML or LDAP

Configuring LDAP single sign-on for Burp Suite DAST

Testing your configuration

Configuring SAML single sign-on for Burp Suite DAST

Configuring SAML SSO with ADFS

Before you start

Step 1: Add Burp Suite DAST to your trusted applications

Step 2: Obtain key details from ADFS

Step 3: Enter the key details in Burp Suite DAST

Step 4: Test your configuration

Managing groups

Enabling Burp Suite DAST to access your ADFS groups

Create a central claim issuance policy

Create claim rules for each group individually

Adding your groups to Burp Suite DAST

Configuring SAML SSO with Entra ID

Before you start

Step 1: Configure your Entra ID Enterprise Application

Step 2: Import key details from Entra ID

Step 3: Test your configuration

Managing groups

Enabling Burp Suite DAST to access your Entra ID groups

Adding your groups to Burp Suite DAST

Configuring SAML SSO with Okta

Before you start

Step 1: Add Burp Suite DAST to your trusted applications

Step 2: Add a Group Attribute Statement

Step 3: Obtain key details from Okta

Step 4: Enter the key details in Burp Suite DAST

Step 5: Test your configuration

Managing groups

Enabling Burp Suite DAST to access your Okta groups

Adding your groups to Burp Suite DAST

Configuring single logout

Configuring SCIM

Integrating SCIM using Okta

Prerequisites

Get your SCIM URL and API token

Upload a TLS certificate

Configure the connection in Okta

Enable SCIM provisioning

Enter the connection details

Configure the provisioning to app settings

Push your Okta users and groups to Burp Suite DAST

Integrating SCIM using OneLogin

Prerequisites

Get your SCIM URL and API token

Upload a TLS certificate

Configure the connection in OneLogin

Enter the connection details

Configure the parameters

Enable SCIM provisioning

Push your OneLogin users to Burp Suite DAST

Troubleshooting provisioning issues in OneLogin

Integrating SCIM using Entra ID

Prerequisites

Get your SCIM URL and API token

Cloud instances

Self-hosted instances

Upload a TLS certificate

Configure the connection in Entra ID

Enter the connection details

Enable SCIM provisioning

Troubleshooting provisioning issues in Entra ID

Managing SCIM users and groups

Assigning permissions to SCIM users

Assigning permissions to SCIM groups

Removing a SCIM user

Managing users locally

Viewing users

Creating a new user

Editing users

Suspending a user temporarily

Deleting a user

Managing groups locally

Creating a new group

Editing a group

Restricting access to sites

Deleting a group

Managing roles locally

Creating a new role

Modifying roles

Deleting roles

Restricting access to sites

Resetting your admin password

Resetting your admin password on a Cloud instance

Resetting your admin password on a self-hosted standard instance

Windows

Linux

Resetting your admin password on a self-hosted Kubernetes instance

Scanning web apps

Optional settings for your new web app site

Detailed scope configuration

Protocol settings

Scan settings

Importing sites in bulk

Preparing the import CSV file

Uploading the CSV file

Configuring authentication for web apps

Configuring login details

Configuring platform authentication details

Adding usernames and passwords for a web app

Using recorded logins

Status checker

Confirmation text options

Finding CSS or XPath selectors

Adding recorded logins

Adding manually-recorded login sequences to new sites

Adding manually-recorded login sequences to existing sites

Recording login sequences using AI

Using Burp AI to record login sequences for new sites

Using Burp AI to record login sequences for existing sites

Reviewing a recorded login

Editing recorded logins

Managing steps in a recorded login

Viewing steps

Step types

Selector types

Advanced settings

Browser settings

Shadow parent

Adding a step

Editing a step

Deleting a step

Configuring TOTP MFA

TOTP detection

Configuring TOTP

Uploading a QR code

Configuring TOTP manually

Configuring the status checker

Updating your TOTP configuration

WebAuthn passkeys in recorded logins

Capturing a new passkey

Importing a passkey

Configuring platform authentication

Performing a pre-scan check

Managing recorded logins

Setting the site scope

Using basic scope control

Setting the scope to a domain

Setting the scope to a specific path

What happens when start URLs overlap

Manually editing the scope

Using advanced scope control

Adding in-scope rules

Adding out-of-scope rules

Scanning APIs

Adding API definitions

Choosing how to add APIs

Managing authentication for API sites

Optional settings for your API

Adding APIs to DAST

Discovering APIs from integrations

Integrating with AWS

Prerequisites

Connecting to Amazon API Gateway

Integrating with Azure API Management

Prerequisites

Connecting to Azure API Management

Integrating with Google Apigee

Prerequisites

Connecting to Google Apigee

Coding custom integrations with GraphQL API

When to use a custom integration

Creating a custom integration

Creating sites for added APIs

Creating API sites

Viewing API endpoints

Creating a site for a single API

Creating sites for multiple APIs

Viewing onboarded APIs

Ignoring APIs

Restoring ignored APIs

Updating your API sites

When new endpoints are detected

Including new endpoints in scans

Adding a single API

Adding API definitions by uploading a file

Adding API definitions by providing a URL

Saving and scanning your site

Bulk uploading APIs

Before you start

How to bulk upload APIs

Update behavior

Import type

Select methods

Choose folder

Network

Review upload

Authentication

Scan configuration

After bulk upload

Configuring API authentication

Host credentials vs API authentication

Supported authentication types

Authentication status overview

Adding basic authentication

Adding Bearer token authentication

Adding API key / custom token authentication

Adding OAuth 2.0 client credentials authentication

Editing or deleting authentication methods

Scanning with incomplete authentication

Viewing and configuring API endpoints

Filtering endpoints

Managing your sites

Configuring site settings

Defining the scan configuration for a site

Using preset scan modes

Using custom scan configurations

Assign a custom scan configuration to a site

Create a custom scan configuration

Exporting scan configurations

Importing scan configurations

Defining the scan configuration for a folder

How scan configurations are combined

How preset scan modes are combined

Configuring AI-enhanced scanning

How does AI-enhanced scanning work?

Enabling AI-enhanced scanning

Enabling AI-enhanced scanning for new sites

Enabling AI-enhanced scanning for existing sites

Viewing AI-enhanced scan results

Configuring upstream proxy servers

Adding headers and cookies

Adding custom headers

Adding session cookies

Understanding scope prefix

Scanning with extensions in Burp Suite DAST

Applying extensions to sites

Applying extensions to an existing site

Removing extensions from sites

Applying extensions to folders

Adding tags to sites

Permissions required to manage tags

Creating tags

Adding tags to a single site or folder

Adding tags to multiple sites or folders

Filtering by tags

Untagging a single site or folder

Untagging multiple sites or folders

Editing tags

Deleting tags

Editing existing sites

Managing the site tree

Creating folders and subfolders

Adding individual sites to a folder

Moving sites and folders in bulk

Deleting sites and folders

Setting up scan notifications

Setting up email notifications

Setting up email notifications when creating a new site

Setting up email notifications for existing sites

Setting up Slack notifications

Setting up Slack notifications when creating a new site

Setting up Slack notifications for existing sites

Configuring network and firewall settings for a site

Cloud instances

Self-hosted instances

Managing your scans

Creating scans

Scheduling scans for a folder

Creating a new scan

CI-driven scans

Managing scheduled scans

Viewing scheduled scans

Editing scheduled scans

Deleting scheduled scans

Editing scheduled scan configurations

Performing bulk actions with scans

Pausing and resuming scans

Creating scan freeze windows

Managing scan freeze windows

Viewing paused scans

Manually pausing and resuming scans

Viewing scan details

Monitoring scan progress

Reviewing scan errors

Configuring issue management settings

Configure false positive settings:

Configure accepted risk settings:

Configure edit issue severity settings:

Best practices for scanning

Configurations by use case

Scope considerations

Large web applications

Authentication

Best practices for managing false positives

Configuring site and scan data settings

Downloading logs and debug packs

Downloading the event log

Downloading the scan debug pack

Downloading the verbose debug pack

Working with scan results

Viewing scan results

Viewing the dashboard

Viewing issues

Reviewing discovered URLs

Reviewing statistics about your scan

Reviewing the settings used for your scan

Viewing failed scans

Viewing AI-enhanced scan results

Burp AI outcomes

Viewing details of Burp AI's investigation

Running an AI investigation manually

Reporting on AI-enhanced results

Tracking issues over time

Viewing the dashboard for a site

Viewing the dashboard for a folder

Viewing the severity trend

Viewing issue details

View details for a specific issue

Managing issues in Burp Suite DAST

Marking an issue as false positive

Marking an issue as accepted risk

Editing issue severity

Raising tickets

Raising GitLab issues from within Burp Suite DAST

Raising GitLab issues for multiple issues

Raising Jira tickets manually

Unlink Jira tickets

Raising Trello cards from within Burp Suite DAST

Raising Trello cards for multiple issues

Raising tickets for multiple issues

Linking multiple issues to an existing ticket

Managing linked tickets

Downloading reports

Download a standard report

Download a compliance report

Send scan summary reports automatically

Export issue data

Burp AI

Burp AI features in DAST

AI-enhanced scanning

AI-powered recorded logins

Enabling Burp AI features in your DAST instance

Security and privacy

Managing scanning resources

Using self-hosted scanning machines with a Cloud instance

System requirements for self-hosted scanning machines

General requirements

Supported operating systems

Network and firewall settings for self-hosted scanning machines

Setting up a self-hosted scanning machine for a Cloud instance

Prerequisites

Downloading the installer

Running the installer

Scanning your sites with self-hosted scanning machines

Managing self-hosted scanning machines with a Cloud instance

Updating self-hosted scanning machines

Deleting a self-hosted scanning machine

Managing authentication tokens

Scanning pools for Cloud instances of Burp Suite DAST

Features of scanning pools

Creating a new scanning pool

Reassigning a scanning machine to a different pool

Reassigning a site to a different pool

Managing scanning resources for a self-hosted instance

Standard instances

Kubernetes instances

Deploying additional scanning machines

Setting up a new scanning machine

Authorizing a new scanning machine

Managing Kubernetes scanning resources

Setting concurrent scan limits

Disabling scanning

Amending your license

Viewing active scans

Scanning pools for self-hosted instances of Burp Suite DAST

Features of scanning pools

Creating a new scanning pool

Reassigning a scanning machine to a different pool

Reassigning a site to a different pool

Managing scanning pools

Assigning scan limits

Additional scans

Post-installation configuration

Managing certificates for outbound connections

Configuring your SMTP server

Using an HTTP proxy server to connect to the SMTP server

Connecting to an external email service

Connecting to an internal email service

Verifying your SMTP server connection

Configuring an HTTP proxy server

Allowlisting an application for CORS

Configuring database backups

Migrating to an external database

Preparing for the migration

Prerequisite steps for Oracle databases

Migrating your data

Running the database transfer command manually

Restarting the Burp Suite DAST services

Integrating with CI/CD platforms

CI-driven scans

CI/CD plugins (legacy)

Integrating CI-driven scans

What are CI-driven scans?

Configuring your scan

Viewing your scan results

Getting started with CI-driven scans

Before you start

System requirements

Running a scan

Setting the public key certificate

Scan results

Remediation advice

Evidence

Configuring CI-driven scans

CI-driven scan integration examples

System requirements for CI-driven scans

Network and firewall configuration

Creating a configuration file for a CI-driven scan

Mandatory settings

Common requirements

Web apps

APIs

Proxy settings

Defining the scope

Public key certificate

Authentication

Login credentials (web apps only)

Recorded logins (web apps only)

API authentication (APIs only)

API key authentication

HTTP authentication types

Dynamic authorization

Scan configuration

Selecting a built-in scan configuration

Selecting a custom scan configuration

Using custom extensions, BChecks, and BApps with CI-driven scans

Configuring connection settings

Viewing scan results in the dashboard

Specifying report format

Ignoring specific issues

Setting the threshold

Configuring output detail level

Adding a configuration file to a CI-driven scan

Example integrations for CI-driven scans

Integrating a CI-driven scan with Azure DevOps

Before you start

Azure DevOps agent requirements

Configuring the Azure DevOps pipeline

(Optional) Creating a starter pipeline YAML file

Running the Azure DevOps pipeline

Viewing scan results in Azure DevOps

Remediation advice and evidence

Integrating a CI-driven scan with GitHub Actions

Integrating a CI-driven scan with GitLab

Before you start

GitLab agent requirements

Configuring the GitLab pipeline

(Optional) Creating a starter pipeline YAML file

Running the GitLab pipeline

Viewing scan results in GitLab

Remediation advice and evidence

Integrating a CI-driven scan with Jenkins

Before you start

Jenkins server requirements

Configuring the Jenkins pipeline

Setting the configuration of your scan

Creating the Jenkinsfile

Viewing scan results in Jenkins

Remediation advice

Evidence

Integrating a CI-driven scan with TeamCity

Before you start

TeamCity agent requirements

Creating the settings file

Setting the configuration of your scan

Configuring the TeamCity pipeline

Viewing scan results in TeamCity

Remediation advice

Evidence

Using plugins for CI/CD platform integration

Overview of CI/CD platform integration

Integration types

Detailed instructions

Integration types for CI/CD platforms

Site-driven scan

Burp scan

Creating an API user for the CI/CD integration

Create a role and group for CI/CD users

Create the CI/CD API user

Integrating Burp Suite DAST with Jenkins

Create an API user

Download and install the plugin

Configure the integration

Configuring a site-driven scan in Jenkins

Prerequisites

Whitelist your Jenkins URL

Create the site-driven scan build step in Jenkins

Test your integration

Configuring a Burp scan in Jenkins

Prerequisites

Create the Burp scan build step in Jenkins

Test your integration

Integrating Burp Suite DAST with TeamCity

Create an API user

Download and install the plugin

Configure the integration

Configuring a site-driven scan in TeamCity

Prerequisites

Whitelist your TeamCity URL

Create the site-driven scan build step in TeamCity

Test your integration

Configuring a Burp scan in TeamCity

Prerequisites

Create the Burp scan build step in TeamCity

Test your integration

Integrating with other CI/CD platforms

Configuring a site-driven scan using the generic CI/CD driver

Prerequisites

Add the build steps to your pipeline

Test your integration

Configuring a Burp scan using the generic CI/CD driver

Prerequisites

Add the build steps to your pipeline

Test your integration

Parameter reference for the generic CI/CD driver

Optional settings for the CI/CD integration

Configuring optional settings using the platform plugins

Configuring optional settings using the generic CI/CD driver

Overriding the default scan configurations from your CI/CD system

Ignoring issues

Integrating Burp Suite DAST with issue tracking platforms

Integrating Burp Suite DAST with GitLab

Prerequisites

(Recommended) Create a new GitLab user for the integration

Generate a GitLab impersonation token

Connect Burp Suite DAST to GitLab

Enable GitLab issues to be raised manually

Enable GitLab issues to be raised automatically

Raising GitLab issues from within Burp Suite DAST

Integrating Burp Suite DAST with Jira

Supported versions of Jira

Supported certificate types

Create a new Jira user (Recommended)

Generate a Jira API token (Jira Cloud only)

Connect Burp Suite DAST to Jira

Enable users to manually raise Jira tickets

Adding custom ticket fields

Raising Jira tickets automatically

Adding custom ticket fields

Raising tickets for previously found issues

Duplicating rules for automatic tickets

Conditional field mapping

Setting up conditional mapping

Managing Jira ticket duplication

Integrating Burp Suite DAST with Trello

Prerequisite

(Recommended) Create a new Trello user for the integration

Connect Burp Suite DAST to Trello

Enable manual Trello card creation

Enable automatic Trello card creation

Raising Trello cards from within Burp Suite DAST

Integrating Burp Suite DAST with Slack

Prerequisites

Create a Slack app

Add the app to your Slack channels

Connect your Slack app to Burp Suite DAST

Manage which Slack channels are available

Integrating Burp Suite DAST with Splunk

Prerequisites

Configuring a connection to Splunk

Creating a new event type in Splunk

Disconnecting from Splunk

Managing services

Managing Burp Suite DAST services for standard instances

List running services

Stop running services

Start services

Restarting services for Kubernetes instances

Managing updates

Configuring automatic updates

Manually checking for updates

Manually installing updates

Downtime during updates

Updating a Cloud instance

Updating Burp Suite DAST on Kubernetes

Preparing to update

Running the update command

Troubleshooting in Burp Suite DAST

Troubleshooting Cloud instances

Event log

Help center

Support logs

Troubleshooting a self-hosted instance

Troubleshooting a Kubernetes instance

Help center

Support pack

Event log

Scan debug pack

Enabling verbose logging

Downloading logs manually

Troubleshooting a standard instance

Help center

Support pack

Diagnostics

Debug

Documentation

Event log

Scan debug pack

Enabling verbose logging

Downloading logs manually

API overview

Using the APIs

Creating API users

REST API

GraphQL API

GraphQL API overview

Getting started with the GraphQL API

Creating an API user

Structuring the GraphQL call

Example request

Using Insomnia

Performing common tasks with the GraphQL API

Query and mutation names

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

Burp Suite DAST - Reference

Technical infrastructure

Troubleshooting in Burp Suite DAST

API reference

User interface

Home page

Dashboard

Issues

Sites page

Site filters

Site actions

Scans page

Scans

Scheduled scans

Schedule scan configurations

Custom scan configuration settings

Connections

Platform authentication

Upstream proxy servers

Request Throttling

Embedded Browser

Burp Collaborator Server

Site and scan data settings

Automatic site creation for API-generated scans

How does Burp Suite DAST decide which sites to match?

Scan deltas

Issue details

Advisory tab

Request and response tabs

Dynamic analysis

Reports

Standard reports

Included severities

False positives

Compliance reports

Compliance report contents

Uncategorized issues

Viewing scan details

Automatic scan summary reports

Team page

Users

Groups

Roles

Settings menu

User activity log

Enabling user activity logging

Downloading the user activity log

Site-level view

Dashboard

Scans

Scheduled scans

Issues

Details

Site details

Site scope

Scan settings

Folder-level view

Folder-level dashboard

Scans

Scheduled scans

Issues

Details

Browser-powered scanning for Burp Suite DAST

How to enable browser-powered scanning for Burp Suite DAST

Enabling browser-powered scanning on Linux machines

All other Linux distributions

Performing bulk actions in the site tree

Permissions for bulk actions

Scanning machines

Scanning pools

CI-driven scans

Network and firewall rule reference

On this page

Cloud instances running scans on PortSwigger's infrastructure

Cloud instances with self-hosted scans

Cloud instances with CI-driven scans

Self-hosted instances with self-hosted scans

Self-hosted instances with CI-driven scans

Multi-factor authentication settings

Enabling MFA

Logging in with MFA

Backup codes

Managing backup codes

Using backup codes

Unattended installation of Burp Suite DAST

Performing an unattended installation with Linux

Performing an unattended installation with Windows

Varfile field guide

Scanner

How do scans work?

BCheck definitions

Managing BChecks in Burp Suite Professional

Managing BChecks in Burp Suite DAST

BCheck definition reference

Metadata

Control flow

Conditionals

Actions

Issue naming

Issue consolidation

Reserved variables

Functions

Combining functions

Misc

Strings

Character escaping

Regex

Comments

Special characters

BCheck structure

Worked examples

In this section

Example host check

Step 1: Add metadata

Step 2: Configure potential paths

Step 3: Configure the request

Step 4: Report issues

Example path check

Step 1: Add metadata

Step 2: Configure file extensions

Step 3: Configure the request

Step 4: Report issues

Example passive check

Step 1: Add metadata

Step 2: Add a string for the check to match

Step 3: Report the issue

Test this BCheck

Example insertion point check

Step 1: Add metadata

Step 2: Define the calculation

Step 3: Send the request

Step 4: Report issues

Example Collaborator-based check

Step 1: Add metadata

Step 2: Configure the request

Step 3: Analyze the results

Test this BCheck

Example Log4Shell check

Step 1: Add metadata

Step 2: Declare variables

Step 3: Send the request

Step 4: Send a follow-up request

Step 5: Report issues

Example server-side prototype pollution check

Step 1: Add metadata

Step 2: Declare variables

Step 3: Attempt to inject SSPP

Step 4: Force an error to check for SSPP

Step 5: Evaluate results and send follow-up request

Step 6: Do a second check for SSPP

Step 7: Report issues

Test this BCheck

Submitting BChecks to the community

Step 1 - Check the submission guidelines

Step 2 - Make a pull request

Step 3 - We review your BCheck

Crawling

Core approach

Session handling

Detecting changes in application state

Authenticated scanning

Application login credentials

Crawling volatile content

Crawling with Burp's browser

Viewing crawl paths

Auditing

Audit phases

Passive audit phase

Consolidation of frequently-occurring passive issues

Active audit phase

JavaScript analysis phase

Audit prioritization

Attack surface exposure

Interest level

Insertion points

Encoding data within insertion points

Nested insertion points

Modifying parameter locations

Handling of frequently occurring insertion points

Automatic session handling

Handling application errors

Authenticated scanning

Login credentials

How does Burp Scanner use login credentials?

Login settings

Identifying login and registration forms

Why is Burp Scanner not filling in my login forms?

Recorded login sequences

Using recorded login sequences

Best practice for recording login sequences

Limitations of recorded login sequences

Tips for recording successful login sequences

Status checker best practices

Troubleshooting recorded login sequences for Burp Suite DAST

Recording login sequences

Preparing the Login Recorder for Burp Suite extension

Using the extension without incognito mode

Recording a login sequence

Adding recorded login sequences

Troubleshooting recorded login sequences

Scan configurations

Preset scan modes

Using presets in Burp Suite Professional

Setting preset scan modes for folders

Custom scan configurations

Scan configuration structure

Using custom configurations in Burp Suite Professional

Using custom configurations in Burp Suite DAST

Built-in configurations

Audit checks - all except JavaScript analysis

Audit checks - all except time-based detection methods

Audit checks - BChecks only

Audit checks - critical issues only

Audit checks - extensions only

Audit checks - light active

Audit checks - medium active

Audit checks - passive

Audit coverage - maximum

Audit coverage - thorough

Crawl and Audit - Balanced

Crawl and Audit - CICD Optimized

Crawl and Audit - Deep

Crawl and Audit - Fast

Crawl and Audit - Lightweight

Crawl limit - 10 minutes

Crawl limit - 30 minutes

Crawl limit - 60 minutes

Crawl strategy - faster

Crawl strategy - fastest

Crawl strategy - more complete

Crawl strategy - most complete

Minimize false negatives

Minimize false positives

Never stop audit due to application errors

Never stop crawl due to application errors

Crawl settings

Crawl behavior

Crawl strategy

Crawl limits

Crawl network timeouts

Handling repeated timeouts during crawl

Login behavior

Authenticated crawl only

Testing login functions

API crawling

Browser behavior

Discovery logic

Audit settings

Audit behavior

Audit strategy

Audit speed

Audit accuracy

Skip checks unlikely to be effective

Automatically maintain session

Follow redirections where necessary

Allow crawl and audit phases to run in parallel

Total scan time

Issue noise reduction

Audit network timeouts

Handling repeated timeouts during audit

Scan checks

JavaScript analysis

Insertion points strategy

Set insertion point types

Ignore specific insertion points

Handling frequent insertion points

Nested insertion points

Insertion point limits

Payload relocation rules

Browser-powered scanning

Use cases for browser-powered scanning

Requirements for API scanning

Starting an API scan

Incidental API scanning

API definition requirements

OpenAPI definition requirements

OpenAPI endpoints

SOAP WSDL requirements

Postman Collection requirements

Postman requests

GraphQL definition requirements

Scanning single-page apps

Configuring scans of SPAs

Crawl strategy

Routing fragments

Non-standard clickable elements

Burp Scanner error reference

Burp Scanner errors in Burp Suite Professional

Burp Scanner errors in Burp Suite DAST

Vulnerabilities list

Burp AI

Burp AI by product

Security and privacy

Burp AI trust and compliance FAQ

Data and privacy

Can AI providers use my data to train their models?

Do AI providers store or retain my data?

Does Burp AI send sensitive data?

What data does PortSwigger store?

Does PortSwigger use my data to improve Burp AI?

How does Burp communicate with AI providers?

Compliance

Is Burp AI covered by PortSwigger's Data Processing Agreement?

Is Burp AI ISO 27001 compliant?

Where is data processed?

What security controls protect your AI infrastructure?

What happens if there's a security incident involving an AI provider?

What happens if an AI provider goes down?

User controls

Can I disable Burp AI entirely?

Does Burp AI run automatically?

Can I stop Burp AI mid-task?

Can I control which targets Burp AI analyzes?

How does Burp AI stay focused on security testing tasks?

Can I choose which AI provider or model Burp uses?

Burp AI data handling

Data sent to AI providers

Explain this

Explore Issue / AI-enhanced scanning

Burp AI in Repeater

False Positive Analysis

Broken Access Control

Recorded Logins

Sensitive data handling

Models used by Burp AI

Geographic locations

Burp AI data storage and retention

Data we collect

Retention periods

Access control and security

How your data may be used

Geographic location

Burp Collaborator

Uses

External service interaction

Out-of-band resource load

Blind SQL injection

Blind cross-site scripting

Server

Private or public server

Data security

Data storage

Data retrieval

Collaborator-based email addresses

Deploying a private server

General setup

Setting up the domain and DNS records

Setting up the ports and firewall

Setting up your server resources

Setting up the configuration file

Launching the Collaborator server

Health check and troubleshooting

Basic setup

Configuring your private server

Configure TLS certificates

Add a polling interface

Use CNAME settings

Truncate interaction messages

Collect usage metrics

Log interaction information

Add custom HTTP content

Add custom DNS records

Example configuration file

Configuration file fields

Alternative configuration fields:

Troubleshooting

Collaborator health check

Server domain resolution

Contents

Results
