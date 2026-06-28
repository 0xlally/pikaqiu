# Adding recorded login sequences in Burp Suite Professional

Source: https://portswigger.net/burp/documentation/desktop/running-scans/configuring-app-logins/adding-recorded-logins
Fetched: 2026-06-28T09:15:52.369346+00:00

Support Center

Documentation

Desktop editions

Running scans

Configuring application logins

Adding recorded login sequences in Burp Suite Professional

Professional

Adding recorded login sequences in Burp Suite Professional

Last updated:

June 18, 2026

Read time:

3 Minutes

To configure application logins for a scan, you can import a recorded login sequence rather than supplying basic user credentials. A recorded login sequence is a set of instructions that tell Burp Scanner how to log in to the target application. You can record login sequences manually, or use Burp's AI-powered capabilities to streamline the process.

Recorded login sequences enable Burp to handle complex authentication mechanisms, including:

Single sign-on.

Multi-step logins in which the username and password are not entered in the same form.

Login forms that contain, for example, extra fields or checkboxes.

You can manage recorded login sequences from the Application login tab of the scan launcher. From here, you can:

Add new logins to the scan.

Edit existing logins.

Replay existing logins.

Import logins from the configuration library.

Generating recorded login sequences using AI

Burp can autonomously record login sequences using AI. It uses the credentials you provide to log in to your target site, and records a working login sequence with no need for you to create steps manually.

Recording logins using AI helps you to:

Save time on scan setup. You can quickly generate recorded login sequences with no need for manual intervention.

Reduce errors and failed scans. Recording steps manually can introduce human error, such as missed interactions or unrecognized input methods.

Scale your testing. AI makes it much quicker to generate login sequences for users with different privilege levels, helping you to test access controls and role-based vulnerabilities efficiently.

Adding an AI-powered recorded login

To create an AI-powered recorded login:

From the scan launcher's Application login tab, select Use recorded login sequences.

Click New to display the New Recorded Login dialog.

Select AI recorded login.

Click Continue.

Enter the following details for the login:

Label - Choose a name for your recorded login.

URL - Enter the full URL where you want to log in, including the protocol. For example http://ginandjuice.shop.

Username and Password - Enter the user credentials.

Click Create recorded login. Burp begins the login attempt.

Watch Burp attempt to log in. Burp makes up to three attempts, recording the first successful login.

Click OK to save the recorded login.

Burp adds the login to the recorded login sequence table. AI-powered recorded logins have an AI icon next to them.

Note

AI-powered recorded logins don't support login sequences that require new windows or tabs to be created or that use the shadow DOM. If Burp is unable to log in, consider adding a login sequence manually.

Privacy and security in AI-powered recorded logins

All of Burp's AI features prioritize security, transparency, and user control. Burp only uses the login credentials you provide to generate its login sequence, and not for any other purpose. It does not send the credentials you provide to the AI - these are only used locally by Burp.

You can review and modify AI-powered login sequences for accuracy and safety before running scans. For more information on this, see Editing existing recorded logins.

Adding manually recorded login sequences

You can record login sequences manually using the Login Recorder for Burp Suite Chrome extension, then add these for your scan.

Related pages

For information on how to record a login sequence, see Recording login sequences.

To add a manually recorded login sequence to your scan:

From the scan launcher's Application login tab, select Use recorded login sequences.

Click New to display the New Recorded Login dialog.

Select Manual recorded login.

Click Continue.

Enter a descriptive Label for the login.

Paste the data from your clipboard into the Paste Script field.

Click OK.

Burp adds the sequence to the list of application logins.

Editing existing recorded logins

To edit an existing recorded login, select it and click Edit to display the Edit Recorded Login dialog. This dialog shows the events comprising the login sequence in a table.

From here you can:

Insert a new login event.

Edit an existing event.

Delete an event.

Alternatively, click See as JSON to view the raw JSON for the recorded login sequence. You can edit this JSON directly. To return to the events table from this view, click View as Events.

Note

For more information on how recorded login events work, see Recorded login sequences.

To delete an existing recorded login, select it and click Delete.
