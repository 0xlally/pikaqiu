# Burp extensions added to Burp Suite Enterprise Edition

Source: https://portswigger.net/blog/burp-extensions-added-to-burp-suite-enterprise-edition
Fetched: 2026-06-28T09:15:08.734351+00:00

Burp extensions added to Burp Suite Enterprise Edition

Emma Stocks |

Thursday, 26 August 2021 at 13:56 UTC

Burp Suite

Enterprise

BAppStore

Burp Extensions (and your own custom extensions) will now be supported by Burp Suite Enterprise Edition, brand new for the 2021.8 release. If you've had much experience with Burp Suite Professional, it's likely that you're already familiar with our BApp Store. If you've only ever used Burp Suite Enterprise Edition though, you might not have come across it yet.

What are BApp extensions?

The PortSwigger BApp Store works much like any online app store - it contains multiple applications which act as an add-on or extension to the tool or software you already have. In the case of the BApp Store, the files are software extensions that are designed to work seamlessly with the various editions of Burp Suite to extend their capabilties.

BApp extensions are mostly written by the Burp Suite user community, with some contributed by James Kettle and the fantastic team at PortSwigger Research - the whole BApp Store library is curated by PortSwigger's team of developers. Each extension has its own unique functionality - they're usually designed to do things like improve a workflow, accelerate a process, provide additional data, or add custom scan checks. Not all BApp extensions are compatible with Burp Suite Enterprise Edition, and the ones that are will usually enhance scanning functionality in some way.

How can we use extensions in Burp Suite Enterprise Edition?

To add a BApp extension to Burp Suite Enterprise Edition, you will need to visit the BApp Store and download the file for the extension you wish to install. Due to the fact that many organizations choose to air-gap their deployment of Burp Suite Enterprise Edition, we have chosen not to integrate the BApp Store into the software in this initial release.

Once you have downloaded the file for the BApp extension you wish to install, follow the installation instructions within Burp Suite Enterprise Edition to upload the extension. Please note that you will need to assign your chosen extension to a site from the site tree. Once you've assigned extensions to a site, all future scans of that site will make use of the extension unless you remove it from the site.

We've made sure that permissions for installing and using BApp extensions are carefully controlled, to allow you to keep your systems as secure as possible when adding extensibility to Burp Suite Enterprise Edition. You can assign permission for extension usability with the built-in role-based access control (RBAC) feature. As with any role-based access permissions, this can be modified at any time.

To access this new functionality, you will need to be running the latest versions of both Burp Suite Enterprise Edition and Burp Scanner. These can both be updated from the main dashboard of your Burp Suite Enterprise Edition interface.

How will the extensions help to improve our workflows?

General themes for Burp Suite Enterprise Edition extensions tend to include:

Modifications to requests - for example, adding a custom header.

Picking up on new issues.

Picking up on issues that are unique to your specific setup.

Accessing different views on existing issues.

Improvements to functionality running alongside a scan.

Extended data and metrics/outputs.

Additionally, Burp Suite Enterprise Edition's new extension functionality will also enable you to create your own custom extensions. Whether you want to integrate with a specific type of environment, deep-dive into an especially nuanced area of one of your sites, or pinpoint an issue that is unique to your setup, you can now build your own extension to cover it.

Especially suited to those enterprises working toward DevSecOps, custom extensions will support uniquely tailored scan checks. Such scan checks can be useful where an application has specific requirements - including:

Specific internal coding standards.

Specific URL naming conventions.

Navigation of specific areas of a code base.

HTTPS-specific file extensions.

This enables customers to use Burp Suite Enterprise Edition to achieve compliance with your own enterprise security standards.

Custom extensions for Burp Suite Enterprise Edition are currently only supported if they are written in Java, so please bear this in mind when writing your extension's functionality. We've got a guide for writing Burp extensions, which includes language-specific instructions, as well as a selection of sample extensions to get you started.

You can customize every aspect of your own extension, including adding remediation advice specific to both your issue and your unique setup. This will enable targeted feedback to be given to developers, and should help to improve code security overall.

Compatible extensions for Burp Suite Enterprise Edition

In this initial feature release, 11 BApp extensions will be available for integration with Burp Suite Enterprise Edition. We've also applied role-based access control, so you can control which users in your team are able to use this functionality.

The following Java-based BApps are available for Burp Suite Enterprise Edition:

Cypher Injection Scanner - detects Cypher code injection in applications using Neo4j databases.

San Scanner - an extension for enumerating associated domains and services via the "Subject Alt Names" section of SSL certificates.

PHP Object Injection Check - adds an active scan check to find PHP object injection vulnerabilities.

HTML5 Auditor - checks for usage of HTML5 features that have potential security risks.

WAFDetect - passively detects the presence of a we application firewall (WAF) from HTTP responses.

Image Size Issues - passively detects potential denial of service attacks due to the size of an image being specified in request parameters.

GWT Insertion Points - automatically identifies insertion points for GWT (Google Web Toolkit) requests when sending them to the active Scanner or Burp Intruder.

J2EEScan - improve the test coverage during web application penetration tests on J2EE applications.

HTTPoxy Scanner - adds an active check for the HTTPoxy vulnerability.

ParrotNG - adds a custom Scanner check to identify Flex applications vulnerable to CVE-2011-2461 (APSB11-25).

Backslash Powered Scanner - complements Burp's active scanner by using a novel approach capable of finding and confirming both known and unknown classes of server-side injection vulnerabilities.

Burp Suite Enterprise Edition extensibility

Want to try out the latest addition to Burp Suite Enterprise Edition? Update your installation to the latest version today, or take out a fully-featured trial.

Burp Suite

Enterprise

BAppStore

Emma Stocks

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
