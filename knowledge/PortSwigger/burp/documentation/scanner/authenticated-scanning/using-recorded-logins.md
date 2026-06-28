# Recording login sequences

Source: https://portswigger.net/burp/documentation/scanner/authenticated-scanning/using-recorded-logins
Fetched: 2026-06-28T09:16:10.639010+00:00

Support Center

Documentation

Scanner

Authenticated scanning

Recording login sequences

DASTProfessional

Recording login sequences

Last updated:

June 18, 2026

Read time:

4 Minutes

Recorded login sequences enable Burp Scanner to audit content that only authenticated users can usually see, even on sites that use complex login mechanisms such as Single Sign-On. This section explains how to record a login sequence and then add it to a new or existing site.

You can also use AI to generate login sequences autonomously in both Burp Suite Professional and Burp Suite DAST. This saves time and reduces the chance of human error.

For more information on how to do this in Burp Suite Professional, see Generating recorded login sequences using AI.

For more information on how to do this in Burp Suite DAST, see Using Burp AI to record login sequences.

Note

We recommend using a recorded login sequence, even for sites that use basic username and password authentication. Recorded logins support the status check, which helps the scanner stay logged in and can make scans faster and deeper. In Burp Suite DAST, recorded logins also enable the pre-scan check to confirm that authentication is working before scanning begins. You cannot use both authentication methods on a single application in either Burp Suite Professional or Burp Suite DAST.

Preparing the Login Recorder for Burp Suite extension

Before you can record a login sequence, you may need to install and configure the Login Recorder for Burp Suite Chrome extension.

This step is required to record logins in Burp Suite DAST. It is optional in Burp Suite Professional, as Burp's browser comes with the extension pre-installed. However, you may still want to install the extension so that you can record logins in a standard Chrome installation.

To install and configure the extension:

Open Chrome and navigate to the Login Recorder for Burp Suite extension page.

Click Add to Chrome.

In the dialog box, click Add extension to install the extension.

Click the extension icon on the Chrome toolbar to open the extension menu.

Click Manage extensions to display the Extensions page.

Select Allow in incognito.

Using the extension without incognito mode

You can use the extension without incognito mode in a standard Chrome installation, for example if you have organization restrictions that prohibit the use of incognito mode. However, we strongly recommend using incognito mode whenever possible to avoid issues with stateful behavior. Recording without incognito mode may result in a recorded login that appears to work, but stops working after your session ends.

To install the extension without incognito mode, follow the above steps, but click Continue without incognito at Step 6.

If you have already installed the extension, you can set the extension to not use incognito mode:

Open the browser.

Click the extension icon on the Chrome toolbar and select Manage extensions.

On the Login Recorder for Burp Suite extension tile, click Details to display the Extensions page.

Deselect Allow in incognito.

Recording a login sequence

Read the Best practice for recording login sequences page before attempting to record a login sequence. This page contains advice to help you to avoid some common errors made when recording complex authentication sequences.

Note

DAST If your login uses WebAuthn, you must capture the passkey before recording the login sequence. For more information, see WebAuthn passkeys in recorded logins.

To record a login sequence:

If you are using Burp Suite DAST, or want to record logins for Burp Suite Professional in a standard Chrome installation, install the Login Recorder for Burp Suite Chrome extension. We recommend that you set the extension to run in incognito mode. For more information, see Preparing the Login Recorder for Burp Suite extension.

Click the extension icon on the Chrome toolbar and select Login Recorder for Burp Suite.

At the prompt, click Start recording. A new window opens.

In the window, browse to the target website.

Complete the login sequence that you want to capture.

When you're done, click the extension icon, select Login Recorder for Burp Suite, and click Stop recording.

The extension automatically copies the generated script to your clipboard. You can re-copy the script by selecting the extension icon and selecting Copy to clipboard.

Note

If your login includes a TOTP step, complete it as normal during recording. When you paste the script into Burp Suite DAST, it automatically detects a potential TOTP step and prompts you to configure it. For more information, see Configuring TOTP MFA.

You can repeat this process for each set of credentials that you want to use for scans of this site. For example, you might record one login sequence in which you log in as a normal user and another sequence in which you log in as an administrator.

Note

Burp Scanner uses Burp's browser to perform recorded login sequences when scanning, even if you have not selected Use Burp's browser for crawl and audit in your scan configuration.

Adding recorded login sequences

The process for adding a recorded login is different for Burp Suite DAST and Burp Suite Professional:

To add a recorded login sequence to a new web app in Burp Suite DAST, see Adding manually-recorded login sequences to new sites.

To add a recorded login sequence to an existing web app in Burp Suite DAST, see Adding manually-recorded login sequences to existing sites.

To add a recorded login sequence to Burp Suite Professional, see Adding recorded login sequences in Burp Suite Professional.

You do not need to manually add AI-generated login sequences to either Burp Suite DAST or Burp Suite Professional. These are automatically imported once the sequence is generated.
