# Enterprise Edition 2023.1

Source: https://portswigger.net/burp/releases/enterprise-edition-2023-1
Fetched: 2026-06-28T09:16:18.348614+00:00

This release introduces support for popup windows when recording logins. We've also added checks that enable you to make sure your infrastructure meets the minimum system requirements. In addition, there are major improvements to Burp Scanner.

Authenticated crawling of applications with popup-based login mechanisms

Burp Scanner can now replay recorded login sequences that open new windows or tabs. This enables you to run authenticated scans on websites with login mechanisms that require you to interact with popups, such as Microsoft and Amazon's SSO services.

System requirement checks

We now check that your infrastructure meets our minimum system requirements, to make sure you have the best experience with Burp Scanner. If any of your machines don't meet the requirements, you'll see an error message and remedial advice.

Major improvements to Burp Scanner

This release significantly improves Burp Scanner's resilience and provides increased support for a wider range of applications, especially single-page apps.

Most importantly, we've fundamentally changed the way Burp Scanner navigates using its built-in browser. As a result, you may now be able to successfully scan a number of sites that were previously incompatible with automated vulnerability scans. In particular, you should see much better results on sites that rely heavily on navigation initiated by client-side JavaScript.

We've also dramatically improved our browser process management, which results in much lower memory usage during scans.

Other improvements

We've added HTTP/2 and Burp Collaborator options to the scan configurations.

Bug fixes

We fixed some bugs, including:

You can now install Burp Suite Enterprise Edition on macOS Ventura.

You can download a report if the scan fails at the crawl or audit phase.

If you create a folder with site restrictions, users no longer need to log out and log in to access it.

Note for Windows Server 2012 and Windows 7/8/8.1 users

Due to a recent Chrome upgrade, Burp Scanner is no longer compatible with the Windows Server 2012 and Windows 7/8/8.1 operating systems. For more information, see the related Chrome announcement.

If you are affected, please refer to our documentation for a list of supported operating systems and upgrade your machines accordingly.
