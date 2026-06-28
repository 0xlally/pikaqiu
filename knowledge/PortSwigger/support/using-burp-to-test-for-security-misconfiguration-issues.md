# Using Burp to Test for Security Misconfiguration Issues

Source: https://portswigger.net/support/using-burp-to-test-for-security-misconfiguration-issues
Fetched: 2026-06-28T09:17:36.907794+00:00

This page may be out of date

We haven't updated it for a while because we're busy working on new, improved content to help you get the

most out of Burp Suite. In the meantime, please note that the information on this page may no longer be

accurate.

Visit our Support Center

Using Burp to Test for Security Misconfiguration Issues

Application misconfiguration attacks exploit configuration weaknesses found in web applications.

Security misconfiguration can happen at any level of an application stack, including the platform, web server, application server, database, and framework.

Many applications come with unnecessary and unsafe features, such as debug and QA features, enabled by default. These features may provide a means for a hacker to bypass authentication methods and gain access to sensitive information, perhaps with elevated privileges.

Likewise, default installations may include well-known usernames and passwords, hard-coded backdoor accounts, special access mechanisms, and incorrect permissions set for files accessible through web servers.

In this example we will demonstrate how to use Burp Spider and/or Site map to check for directory listings. This tutorial uses an exercise from the “Mutillidae” training tool.

The version of “Mutillidae” we are using is taken from OWASP’s Broken Web Application Project. Find out how to download, install and use this project.

First, ensure that Burp is correctly configured with your browser.

Ensure Burp Proxy "Intercept is off".

In your browser, visit the page of the web application you are testing.

In this example start by browsing to the Mutillidae home page.

Return to Burp.

Select the "Target" tab and then the "Site map" tab.

Locate and right click on the "Mutillidae" folder to bring up the context menu..

Click "Spider from here".

Although not necessarily a security vulnerability, directory listings are reported by Burp Scanner.

For example, if you have passive scanning enabled when you spider this application, "Directory listing" will be included in the Scanner "Results" tab.

Go to the "Target" tab and then the "Site map" tab.

Here you can view the site map for the web application which has been populated by Burp Spider.

Select an interesting branch from the Site map. In this case we will explore the "Includes" directory.

Return to your browser and access the directories you have chosen to investigate by adding the directory name to the URL.

In this example: /mutillidae/includes/.

Explore the links in each file and directory you are able to find.

Related articles:

What is Burp Proxy?

Scanning websites with Burp Scanner

Burp's target site map

Getting Started with Burp Spider
