# Configuring TOTP MFA

Source: https://portswigger.net/burp/documentation/dast/user-guide/scanning-web-apps/configure-authentication/totp-mfa
Fetched: 2026-06-28T09:15:41.113441+00:00

DAST

Configuring TOTP MFA

Last updated:

June 18, 2026

Read time:

3 Minutes

Cloud

Self-hosted

If your web app uses time-based one-time password (TOTP) multi-factor authentication (MFA), you can configure recorded logins to generate valid passcodes during scans. Burp Suite DAST automatically detects potential TOTP steps in recorded login scripts, and prompts you to configure them.

For more information, see Managing steps in a recorded login.

TOTP detection

When you paste a login script into a recorded login, Burp Suite DAST scans the script for steps that look like a TOTP entry. For example, a step that types a six-digit code into a field. If it finds one, TOTP detected appears in the sidebar.

Select TOTP detected in the sidebar to view the detected step and configure TOTP.

Configuring TOTP

You can configure TOTP by uploading a QR code, or by entering the details manually.

Uploading a QR code

The easiest way to configure TOTP is to take a screenshot of the QR code that your target app displays when you set up MFA.

Note

Your target app only shows the QR code once, during MFA setup. We recommend creating a dedicated account for scanning and taking a screenshot of the QR code when you set up MFA for that account. If you don't have the QR code, ask your admin for the TOTP secret so you can configure TOTP manually.

To configure TOTP using a QR code:

Create your recorded login and add the login script.

Click TOTP detected, and then click Configure TOTP.

Click Upload QR code and select your QR code image.

Click Save.

Configuring TOTP manually

If you don't have a QR code, you can enter the TOTP details manually. You may need to ask your admin for these.

To configure TOTP manually:

Create your recorded login and add the login script.

Click TOTP detected, and then click Configure TOTP.

Click Set up TOTP manually.

Enter your TOTP secret.

Configure the remaining fields to match your app's TOTP settings:

Algorithm: The hashing algorithm your app uses. The default is SHA1.

Period (seconds): How often the passcode refreshes. The default is 30 seconds.

Digits: The number of digits in the passcode. The default is 6.

Click Save.

Note

Burp Scanner throttles login attempts to prevent TOTP code reuse before the passcode refreshes.

Configuring the status checker

After you configure TOTP, you need to configure the status checker.

The status checker enables the scanner to greatly reduce the number of times a recorded login sequence runs during a scan.

For more information, see Status checker.

Updating your TOTP configuration

You can update your TOTP configuration at any time by editing the recorded login sequence.

To update your TOTP configuration:

Select the site's Details tab and click Edit.

In Scan settings > Authentication, click the pencil icon next to the recorded login sequence.

In the Steps tab, click More next to the TOTP step and select Edit.

Click Replace QR code to upload a new QR code, or update the manual configuration fields as needed.

Click Save to apply your changes.

Related pages

Using recorded logins.

Managing steps in a recorded login.

Best practice for recording login sequences.
