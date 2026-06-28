# Using recorded logins

Source: https://portswigger.net/burp/documentation/dast/user-guide/scanning-web-apps/configure-authentication/recorded-logins
Fetched: 2026-06-28T09:15:40.959383+00:00

DAST

Using recorded logins

Last updated:

June 18, 2026

Read time:

9 Minutes

Cloud

Self-hosted

A recorded login sequence is a set of instructions that tell Burp Scanner how to log in to a particular web app. Recorded login sequences enable Burp Scanner to audit content that only authenticated users can usually see, even on web apps that use complex login mechanisms such as Single Sign-On.

This section explains how to add manually-recorded login sequences to a new or existing site. For information on how to record the sequences, see Recording login sequences (Scanner).

Note

We recommend using a recorded login sequence, even for sites that use basic username and password authentication. Recorded logins enable the pre-scan check to confirm that authentication is working, and provide troubleshooting.

Recorded logins also support our status checker, which can make scans faster and deeper.

Status checker

To make sure the scanner can access authenticated content, use the status checker to confirm that the scanner successfully logs in each time it replays your recorded login during the scan. The status checker looks in your specified URL for confirmation that only appears if you're logged in.

The status checker enables the scanner to maintain authentication efficiently, making scans much faster and deeper.

If the status checker detects that authentication has failed during the scan, it shows a message to help you understand and fix the issue. If the status checker fails during a pre-scan check, you can also see a screenshot and the HTTP response.

We recommend configuring the status checker when you add a recorded login.

Confirmation text options

In the Confirmation text field, you can use plain text, XPath expressions, or CSS selectors to identify elements that confirm you're logged in. This is particularly useful if you scan single page applications, because it enables you to target specific page elements.

These are some examples of confirmation text:

Plain text: Welcome back - Looks for this text anywhere on the page.

CSS selector: a[href="/account"] - Looks for a link to an account page.

XPath selector: //button[text()='Log out'] - Looks for a "Log out" button.

Finding CSS or XPath selectors

Using CSS or XPath selectors can make status checks more reliable, especially on dynamic sites. They enable Burp Scanner to target specific elements that only appear when you're logged in, instead of relying on visible text.

You can identify CSS or XPath selectors for your confirmation text by using your browser's developer tools.

To find a CSS selector:

Open your site in your browser.

Right-click the element you want Burp Scanner to look for, and select Inspect.

In the developer tools panel, make sure the correct element is highlighted.

Right-click the highlighted code, and select Copy > Copy selector.

Paste the selector into the Confirmation text field in Burp Suite DAST.

To find an XPath selector:

Open your site in your browser.

Right-click the element you want Burp Scanner to look for, and select Inspect.

In the developer tools panel, make sure the correct element is highlighted.

Right-click the highlighted code, and select Copy > Copy XPath.

Paste the XPath into the Confirmation text field in Burp Suite DAST.

Note

If both selector types are available, use the CSS selector. CSS selectors are generally shorter, easier to read, and work well with most modern web apps.

Adding recorded logins

You can add a recorded login to new or existing sites, with or without configuring the status checker.

Adding manually-recorded login sequences to new sites

To add a manually-recorded login sequence when you add a new web app site:

On the top menu, select Sites > Add a new site to display the Create a new site page.

In the Scan settings section, select Authentication > Application logins.

Select Recorded login sequences.

Click Add a recorded login sequence.

Select Manual recorded login.

Paste the login script into the Paste script field.

Burp Suite DAST generates a Label from your script. Edit the label if required.

Configure the status checker to monitor authentication during the scan. This is recommended for all scans, and required for TOTP MFA:

Click the Status checker tab.

In the URL field, enter a URL where the scanner can check that you're logged in.

In the Confirmation text field, enter text that the scanner can look for to confirm you're logged in.

Click Finish to close the dialog box.

Click Save. The recorded sequence is added to the list of application logins for the site.

Note

Burp Scanner always uses Burp's browser to perform recorded login sequences when scanning, even if you have not selected Use Burp's browser for crawl and audit in your scan configuration.

Adding manually-recorded login sequences to existing sites

To add a manually-recorded login sequence for an existing web app:

On the top menu, select Sites to display the site tree.

Select the web app site you want to set up notifications for.

Select the Details tab and click Edit.

In the Scan settings section, select Authentication > Application logins.

Select Recorded login sequences.

Click Add a recorded login sequence.

Select Manual recorded login.

Paste the login script into the Paste script field.

Burp Suite DAST generates a Label from your script. Edit the label if required.

Configure the status checker to monitor authentication during the scan. This is recommended for all scans, and required for TOTP MFA:

Click the Status checker tab.

In the URL field, enter a URL where the scanner can check that you're logged in.

In the Confirmation text field, enter text that the scanner can look for to confirm you're logged in.

Click Finish to close the dialog box.

Click Save. The recorded sequence is added to the list of application logins for the site.

To add another recorded login, click the plus button and repeat steps 7 to 9.

To delete a recorded login, click the trash icon .

Recording login sequences using AI

Note

Burp AI in Burp Suite DAST is currently in a limited access beta and is not available to all customers.

Burp AI can autonomously record login sequences in Burp Suite DAST. It uses credentials you provide to log in to your target site, and records a working login sequence with no need for you to create steps manually.

Using Burp AI to record logins helps you to:

Save time on scan setup. You can quickly generate recorded login sequences with no need for manual intervention.

Reduce errors and failed scans. Recording steps manually can introduce human error, such as missed interactions or unrecognized input methods.

You must have the Configure Burp AI features permission to use AI-recorded logins.

Note

Burp AI cannot record login sequences for sites that use multi-factor authentication (MFA).

Using Burp AI to record login sequences for new sites

To use Burp AI to record a login sequence when you add a new site:

On the top menu, select Sites > Add a new site to display the Create a new site page.

In the Scan settings section, select Authentication > Application logins.

Select Recorded login sequences.

Click Add a recorded login sequence and make sure that the AI recorded login radio button is selected.

Add a Label for your script. This is used to identify it once it has been created.

Add the URL that the script should run against.

Add the Username and Password that the script should attempt to log in with.

Click Next to display the Status checker page.

Configure the status checker to monitor authentication during the scan (recommended):

In the URL field, enter a URL where the scanner can check that you're logged in.

In the Confirmation text field, enter text that the scanner can look for to confirm you're logged in.

Click Finish to close the dialog box.

Click Save to return to the site page. Burp AI begins generating your login sequence.

Burp Suite DAST displays a notification at the top of the Dashboard tab when the sequence has finished recording.

Using Burp AI to record login sequences for existing sites

To use Burp AI to record a login sequence for an existing site:

On the top menu, select Sites to display the site tree.

Select the site you want to set up a recorded login for.

Select the Details tab and click Edit.

In the Scan settings section, select Authentication > Application logins.

Select Recorded login sequences.

Click Add a recorded login sequence and make sure that the AI recorded login radio button is selected.

Add a Label for your script. This is used to identify it once it has been created.

Add the URL that the script should run against.

Add the Username and Password that the script should attempt to log in with.

Click Next to display the Status checker page.

Configure the status checker to monitor authentication during the scan (recommended):

In the URL field, enter a URL where the scanner can check that you're logged in.

In the Confirmation text field, enter text that the scanner can look for to confirm you're logged in.

Click Finish to close the dialog box.

Click Save to return to the site details page. Burp AI begins generating your login sequence.

Burp Suite DAST displays a notification at the top of the site details page when the sequence has finished recording.

Related pages

Burp AI trust and compliance FAQ - explains how PortSwigger keeps your data safe when using AI features.

Reviewing a recorded login

When you run a pre-scan check, Burp Suite DAST captures images from the steps of your recorded login sequences. You can review the steps and edit any that show an error message, to make sure that they successfully log in to the site.

Note

To view a recorded login sequence, you need permission for the site to View site application login details. For more information, see Role-based access control.

To grant users permission to view recorded logins, an admin user needs to:

Create a new role that has permission to View sites, View site details, and View site application login details.

If the role also needs to enable users to run pre-scan checks, give permission to Edit sites and folders.

Create a new group that contains the new role, the appropriate users, and any site restrictions.

Ask the users to sign out and sign in again, for the changes to take effect.

To review your recorded login sequences:

From the Sites menu, select a web app site.

In the Pre-scan check menu, click Run pre-scan check. Wait for the pre-scan check to complete.

Expand the Pre-scan check menu and go to the Recorded logins tab.

To review a specific recorded login sequence, click Review replay.

Review any steps of the recorded login that show an error message. Click Edit to make changes to your login script.

Note

You will see error messages if there is an error with the script for the recorded login or the status checker.

Recorded login images are only stored for 14 days. After this period, you need to run a new pre-scan check in order to review your login sequence.

If the status checker fails, you can view a screenshot of the page where Burp Scanner looked for your confirmation text:

Click Recorded logins.

Next to Status, click View response.

An image of the page and the HTTP response are displayed. Click Download to save a copy of the HTTP response.

Editing recorded logins

You can edit existing recorded login sequences without having to delete and recreate them. You can either manage individual steps or edit the JSON script directly. This is useful when you need to update authentication credentials, modify the login script, or adjust the status checker settings.

Note

To edit a recorded login sequence, you need permissions for the site to View site application login details and Edit site application logins. For more information, see Role-based access control.

To edit a recorded login sequence:

Select the site's Details tab and click Edit.

In Scan settings > Authentication, click the pencil icon next to the recorded login sequence you want to modify.

Edit your recorded login sequence:

To manage individual steps, go to the Steps tab. For more information, see Managing steps in a recorded login.

To edit the JSON script directly, go to the Script tab and update the JSON-based script. You can also change the label for the recorded login.

Click Next.

Modify the URL and confirmation text used to verify the authentication status during scans.

Click Finish to close the dialog box.

Click Save to apply your changes.

Related pages

Managing steps in a recorded login.

Configuring TOTP MFA.

Adding usernames and passwords for a web app.

Best practice for recording login sequences in Burp Suite DAST.

Running a pre-scan check.
