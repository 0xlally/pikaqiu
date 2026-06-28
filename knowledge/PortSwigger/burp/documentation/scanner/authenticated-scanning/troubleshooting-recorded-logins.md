# Troubleshooting recorded login sequences

Source: https://portswigger.net/burp/documentation/scanner/authenticated-scanning/troubleshooting-recorded-logins
Fetched: 2026-06-28T09:16:10.280844+00:00

Support Center

Documentation

Scanner

Authenticated scanning

Troubleshooting recorded login sequences

DASTProfessional

Troubleshooting recorded login sequences

Last updated:

June 18, 2026

Read time:

3 Minutes

Burp Scanner is sometimes unable to replay a recorded login sequence during the scan. Although this won't cause the scan to fail completely, failing to replay the sequence prevents Burp Scanner from performing an authenticated crawl.

There are several steps you can take to troubleshoot these issues:

Check the Limitations of recorded login sequences page to make sure that the application's login mechanism is compatible with the recorded logins feature.

Check for error messages in the scan's event log. These might tell you whether the issue is the login sequence or whether there is a general issue with the browser. Note that some log entries may only represent temporary failures that were later resolved. For example, if the target site imposes rate limits, you might see many entries saying that Burp Scanner was unable to log in. However, it may have logged in successfully later in the scan.

For more information on accessing the event log in Burp Suite DAST, see Downloading logs and debug packs.

For more information on accessing the event log in Burp Suite Professional, see Event log.

From the Help menu of Burp's browser, run a health check to make sure there are no issues with the browser. Recorded logins are only compatible with browser-powered scans. Burp Scanner cannot use your recorded login sequence if there is an issue preventing browser-powered scanning.

For more information, see Burp's browser.

Use the Replay function to test the recorded login sequence. Make sure that the sequence finishes on the page you would expect it to after logging in. If it does not, you may be able to determine the final action that Burp was able to perform as expected. Try re-recording the login sequence and run another test. If this new recording also fails at the same stage, it may be that the next action in the sequence is not supported by Burp Scanner. For more information on replaying login sequences in Burp Suite DAST, see Reviewing a recorded login.

Double-check that the login sequence finishes on a page that is in scope for the scan. Although the crawler can follow out-of-scope links during the login process, the login sequence must end on an in-scope page.

If your recorded login includes a TOTP step and the scanner is generating invalid passcodes, verify that the TOTP secret, algorithm, period, and digits match the MFA settings of your target app. You may need to ask your admin for these settings.

If your recorded login includes a WebAuthn step and authentication is failing, check the following:

Make sure you disabled any password manager browser extensions before capturing your passkey and recording the login sequence.

If you're using an enterprise identity provider, check that synced passkey support is enabled in your settings.

DAST If you're using the status checker, verify your configuration:

Check that the URL is accessible and returns the expected content when you're logged in.

Confirm that the confirmation text appears only when authenticated and is not present for unauthenticated users.

Test the status URL manually by logging in and out to ensure the confirmation text appears and disappears as expected.

Check the event log for status checker-related errors that might indicate authentication failures during the scan.
