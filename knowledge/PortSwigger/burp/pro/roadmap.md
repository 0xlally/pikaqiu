# Product roadmap

Source: https://portswigger.net/burp/pro/roadmap
Fetched: 2026-06-28T09:16:13.253004+00:00

Burp Suite Professional

Product roadmap

TRY FOR FREE

BUY -

Coming in the next 12 months

BChecks - testing tool

New feature

A new BChecks testing tool will make testing BChecks just as easy as it is to write them. Send suitable requests to the tool, and use them as test cases to confirm that your BCheck is working.

User interface - customization

New feature

Alter and customize the layout of your Burp workspace. Tailor Burp Suite's top level tools to the particularities of your workflow.

Service worker networking

Feature enhancement

Burp Scanner's crawler will properly support service workers and WebSockets messages - eliminating situations where attack surface could be missed due to incomplete support in this area.

API scanning improvements

Feature enhancement

Burp Scanner's API scanning feature will gain the ability to support a number of popular API features that it doesn't currently. This will enable greatly improved scan coverage of web APIs.

Code your own view filters

New feature

Customize Burp Suite using your own code, directly from the UI. Quickly and easily create view filters that do exactly what you need them to. No more being limited by checkboxes.

Start scan from API definition

New feature

Include an API definition as part of the Burp Scanner launch process. The scanner will use this API definition to seed its scan - enhancing its ability to scan APIs and microservices.

Improved Burp Scanner interface

Feature enhancement

Improved visualization of scan activity. Better understand the coverage that your scan configuration has achieved, and how any discovered issues fit into the target's nav structure.

Burp Scanner auto configuration

Feature enhancement

Burp Scanner will gain the ability to configure itself based on the type of application you are scanning. This will improve scan coverage and help to avoid missed attack surface - without manual configuration.

Access control scan checks

New feature

Burp Scanner will check for a number of security vulnerabilities relating to access control.

Notes everywhere

Feature enhancement

Write free-form multi-line notes, to capture everything you know about an HTTP message. This will be a big improvement over Burp's existing comment feature.

Browser performance enhancements

Feature enhancement

Burp Scanner uses a pool of embedded browsers to navigate web sites effectively while scanning. But this can be heavy on resources. We will redesign this system - leading to more efficient scans.

Enhanced tables

Feature enhancement

We're going to change the way tables work in Burp, so they're more consistent, and give you more control. Show and hide different columns, move them around, and gain new capabilities for search and export.

Test the modern web

Find out how Burp Suite Professional can help you cut through the growing complexity of the modern web - to test faster.

Read more

BChecks

Released

Extend Burp Scanner quickly and easily - using BChecks written in a simple text-based language. Now you can use Burp Scanner to scan for anything you want to look for.

Burp Organizer

Released

A new tool within Burp Suite that makes it easier to manage your pentesting workflow. Store messages to investigate later, or save messages you've already identified as interesting / want to add to a report.

GraphQL scan checks

Released

Burp Scanner can check for security vulnerabilities in APIs that use the GraphQL language. This broadens the range of APIs you are able to test automatically.

ARM64 support

Released

Use Burp on an ARM64 machine running Linux. Particularly useful if you're a tester running Kali Linux on an ARM64 virtual machine.

Collaborator client

Released

Collaborator client now has its own top-level tab, uses a tabbed interface, and saves its interactions in project files, among other improvements.

JWT scan checks

Released

Burp Scanner now checks for a number of security vulnerabilities relating to JSON Web Tokens (JWT).

New API

Released

Burp's Montoya API is a completely new extensibility framework, which will lead to much richer capabilities in the future.

Audit of asynchronous traffic

Released

Burp Scanner now automatically audits in-scope API requests that are issued from client-side JavaScript using XHR and Fetch.

Enhanced Burp Intruder

Released

More options for brute forcing and fuzzing. New payload types and placement options, richer results analysis, and incremental saving.

DOM testing tools

Released

Add-ons to Burp Suite Professional's embedded browser have enhanced manual testing for DOM-based vulnerabilities.

Integrated SCA capabilities

Released

Perform software composition analysis (SCA) of client-visible code. Report JavaScript libraries in use that contain known vulnerabilities.

API scanning

Released

Enumerate API endpoints to scan APIs in target applications. API scanning utilizes OpenAPI (Swagger) definitions.

Automatic updates

Released

Update without lifting a finger. Burp Suite Professional can now update itself automatically - without user intervention.

New web cache poisoning scan checks

Released

Find cutting-edge vulnerabilities with Burp Scanner. Scan checks based on James Kettle's latest web cache poisoning research.

Browser-powered scanning by default

Released

Best-in-class coverage and scanning performance for challenging targets like AJAX-heavy single page app, with browser-driven (Chromium) scanning. Enabled by default.

Read all release notes

Additional Montoya API functionality

Released

Work with WebSockets and Burp project files when building Burp extensions (BApps). While we will continue to develop the Montoya API, it is already more powerful than Burp's old API ever was.

React form handling

Released

Burp Scanner can handle forms when scanning single page applications (SPAs) built on React. This improves performance when scanning input elements that lack an enclosing form tag.

Revamped browser powered scanning

Released

We have fundamentally changed the way that Burp Scanner navigates using its built-in browser. This improves scanning of applications that make heavy use of client-side JavaScript for navigation, and lays a strong foundation for further development of the scanner.

User and project options

Released

User and project options are now accessed via a single Settings dialog. We have also added a search function.

Performance improvements

Released

Improved memory and processing efficiency for various Burp features. Users also now get feedback on any resource-hungry BApps.

Message inspector improvements

Released

Various improvements to the usability of the HTTP message inspector, based on user feedback.

HTTP/2-specific vulnerability reporting

Released

Burp Scanner can now report new classes of HTTP/2-specific vulnerabilities.

Server-side template injection

Released

Burp Scanner can now detect injection into a wider range of templating engines, and will employ OAST techniques to detect blind SSTI.

Improved SPA scanning

Released

Burp Scanner now handles navigational actions that cause DOM updates without a synchronous request to the server, allowing better handling of single-page applications.

Native HTTP logging

Released

Based on the user popularity of certain BApps (Logger++ and Flow), Burp Suite Professional has gained native, resource-efficient logging functionality.

HTTP/2 support

Released

Use HTTP/2 for both inbound and outbound communication over TLS (beta feature). Also gives control of TLS protocols within Burp Proxy.

Inspector view

Released

Manipulate browser traffic more easily. Improved access to headers, parameters, and more - plus automatic encoding and decoding.

Render pages within Burp tools

Released

See exactly what you're looking at - without changing tab. Tools like Burp Repeater and Burp Intruder now allow you to render responses.

Collaborator payloads in Intruder attacks

Released

Dynamically generate Collaborator payloads in Intruder attacks - enabling you to automate out-of-band (OAST) attacks more easily.

Improved scanning of JavaScript frameworks

Released

Multiple improvements to Burp Scanner's performance when scanning web applications built using popular JavaScript frameworks. This is an area we will periodically revisit.

Improved scan speed

Released

Further optimized performance in default settings - to enable faster scans without compromising coverage.

Support for popups in recorded login sequences

Released

Addition of support for popup page elements when using Burp Scanner's recorded login (authenticated scanning) feature.

Improved user experience

Released

A number of changes to Burp Suite Professional's UI, based on user feedback - including grouped tabs, and four new preset modes for Burp Scanner.

HTTP/2-based enhancements

Released

The HTTP message inspector has gained new capabilities, enabling manual exploitation of HTTP/2-specific vulnerabilities using Burp Repeater. The Burp Extender API has also been enhanced to enable HTTP/2-specific attacks.

Payloads within data formats

Released

We have improved the placement and encoding of scan payloads within JSON and XML data structures.

Improved navigational coverage

Released

Burp Scanner now detects and interacts with more DOM elements that can cause JavaScript-triggered navigation, in addition to conventional links and forms.

Early adopters releases

Released

All Burp Suite Professional users now gain access to an optional early adopters' release track - giving early access to new and experimental features.

Recorded login sequences

Released

Better scrutinize login-related functionality by recording complex login sequences in a browser. Ideal for JavaScript-heavy logins, or single sign-on.

Embedded browser for manual testing

Released

Proxy HTTPS traffic with no configuration necessary. Burp Suite's embedded Chromium browser can now take care of everything.

Browser-powered scanning enhancements

Released

Significant improvements to Burp Scanner - enabling enhanced performance and coverage of modern navigational patterns.

Pretty printing in the HTTP message editor

Released

Make code easier to work with. Burp Suite will prettify JSON, XML, HTML, CSS, and JavaScript within the HTTP message editor.

The tool is self sufficient, with many features out of the box and allows for extensibility. No need for servers or databases. It's a well calibrated "gun". It lets us either validate findings from

external security reports or penetration test our software while in development.

Source: TechValidate survey of PortSwigger customers

See more customer stories

Software Engineer

Large Enterprise Financial Services Company

Product Overview

Find out more

Features

Find out more

Try for free

Request a trial

Resellers

Find out more

Get started for free

The most widely used application security toolkit
