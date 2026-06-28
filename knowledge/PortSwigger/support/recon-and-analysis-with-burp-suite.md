# Recon and Analysis with Burp Suite

Source: https://portswigger.net/support/recon-and-analysis-with-burp-suite
Fetched: 2026-06-28T09:17:34.779366+00:00

This page may be out of date

We haven't updated it for a while because we're busy working on new, improved content to help you get the

most out of Burp Suite. In the meantime, please note that the information on this page may no longer be

accurate.

Visit our Support Center

Recon and Analysis with Burp Suite

The Proxy tool lies at the heart of Burp's workflow. It lets you use your browser to navigate the application, while Burp captures all relevant information and lets you easily initiate further actions. This article describes the tasks that are typically required during the recon and analysis phase.

Manually map the application

Using your browser working through Burp Proxy, manually map the application by following links, submitting forms, and stepping through multi-step processes.

This process will populate the Proxy history and Target site map with all of the content requested, and (via passive spidering) will add to the site map any further content that can be inferred from application responses (via links, forms, etc.).

You should then review any unrequested items (shown in gray in the site map), and request these using your browser.

Perform automated mapping where necessary

You can optionally use Burp to automate the mapping process in various ways. You can:

Carry out automatic spidering to request unrequested items in the site map. Be sure to review all the Spider settings before using this tool.

Use the content discovery function to find further content that is not linked from visible content that you can browse to or spider.

You can perform custom discovery using Burp Intruder, to cycle through lists of common files and directories, and identify hits.

Note that before performing any automated actions, it may be necessary to update various aspects of Burp's configuration, such as target scope and session handling.

Analyze the application's attack surface

The process of mapping the application populates the Proxy history and Target site map with all the information that Burp has captured about the application.

Both of these repositories contain features to help you analyze the information they contain, and assess the attack surface that the application exposes.

Further, you can use Burp's Target Analyzer to report the extent of the attack surface and the different types of URLs the application uses.

Note: When the initial application mapping is completed, this is a good time to define your Target scope, by selecting branches within the site map and using the "Add to scope" / "Remove from scope" commands on the context menu. You can then configure suitable display filters on the site map and Proxy history, to hide from view items that you are not currently interested in.

Related articles:

Burp Intruder

Target tool

Burp Spider

Configuring your browser to work with Burp

What is Burp Proxy?
