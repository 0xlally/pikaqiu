# Best practice for recording login sequences

Source: https://portswigger.net/burp/documentation/scanner/authenticated-scanning/recorded-login-best-practice
Fetched: 2026-06-28T09:16:10.077759+00:00

Support Center

Documentation

Scanner

Authenticated scanning

Best practice for recording login sequences

DASTProfessional

Best practice for recording login sequences

Last updated:

June 18, 2026

Read time:

5 Minutes

Burp Suite's recorded login sequence feature enables you to specify login details that Burp Scanner can use when performing authenticated scanning on applications with complex login mechanisms.

We recommend using a recorded login sequence, even for sites that use basic username and password authentication. Recorded logins support the status check, which helps the scanner stay logged in and can make scans faster and deeper. In Burp Suite DAST, recorded logins also enable the pre-scan check to confirm that authentication is working before scanning begins.

While the Login Recorder for Burp Suite Chrome extension is easy to use in itself, successfully recording a login sequence for a sophisticated authentication mechanism can be a complex process.

We have compiled some advice that should help you record login sequences successfully.

Limitations of recorded login sequences

Although recorded login sequences are intended to handle a wide variety of login mechanisms, they do have some limitations:

Recorded logins are only compatible with browser-powered scans. If Burp Scanner cannot initialize its browser then the authenticated scan cannot start.

Burp Scanner cannot self-register users or deliberately trigger login failures by submitting invalid credentials in conjunction with a recorded login sequence. As a result, Burp Scanner ignores any Testing login functions crawl settings from your scan configuration when using recorded logins.

Your authentication system may flag repeated logins made during the scan as suspicious. This in turn could trigger additional authentication steps or anti-robot measures that the crawler is unable to handle. In this case, we recommend running the scan on a test instance with these checks disabled.

Recorded logins are compatible with TOTP MFA and WebAuthn, but not with other forms of two-factor authentication, character-select passwords, or CAPTCHA.

Some enterprise identity providers do not support WebAuthn by default, and may require you to enable synced passkey support in your settings before passkey capture will work.

Note

Recorded logins do not support CAPTCHA because CAPTCHA systems are specifically designed to deny automated systems such as our recorded login tool. Adding support would likely result in CAPTCHA providers patching the methods we would use to bypass the CAPTCHA mechanism, potentially creating a cycle of us finding CAPTCHA vulnerabilities and providers patching them out.

Tips for recording successful login sequences

Read the limitations of recorded login sequences to make sure that the authentication process for your target application is compatible with Burp Suite's recorded logins.

These tips will help you to create recorded login sequences that work first time:

Wait for pages and elements to finish loading completely before performing the next action.

Avoid any unnecessary actions such as additional mouse clicks. Burp Scanner repeats all the actions you record.

Use mouse clicks (rather than keyboard shortcuts) to interact with all elements on the page. This tip applies even for fields that are automatically selected.

After the login process is complete, end the sequence without clicking on any other links or logging out. The recorded login sequence is designed to perform the login process only. Any additional navigation is automatically handled by Burp Scanner as part of its crawl phase.

Make sure that the login sequence finishes on a page that is in scope for scans of this site. Although the crawler can follow out-of-scope links during the login process, the login sequence must end on a page that is in scope.

Recorded login sequences are intended to handle web application authentication only. If the destination server requires platform authentication, such as Microsoft NTLM, then you should enter these credentials separately. You can set platform authentication credentials as part of a custom scan configuration.

If your site uses WebAuthn, disable any password manager browser extensions before attempting to capture passkeys and record login sequences. These extensions may intercept the passkey flow and prevent it from being captured correctly.

DAST Configure the status checker to monitor authentication status during scans. Choose a URL that reliably shows when you're logged in and select text from the page that only appears for authenticated users.

Status checker best practices

DAST

When configuring the status checker alongside your recorded login sequences, follow these guidelines:

Choose a reliable URL - Select a URL that consistently shows authentication status, such as an account dashboard or profile page. Avoid pages that might be cached or show the same content for both authenticated and unauthenticated users.

Select specific confirmation text - Choose text that only appears when you're logged in, such as "My Account", a username, or "Welcome back". Avoid generic text that might appear for all users.

Test your configuration - Verify that the confirmation text is only displayed when you're logged in. This helps the status checker to accurately detect authentication failures.

Use in-scope URLs when possible - While the status checker can check out-of-scope URLs, using an in-scope URL helps make sure the status check doesn't interfere with the scan's crawling and auditing phases.

Troubleshooting recorded login sequences for Burp Suite DAST

If Burp Scanner is unable to replay a recorded login sequence during a scan then it cannot perform an authenticated crawl. However, the scan will still run.

If your login sequence does not break any of the limitations for recorded logins, and you have followed all the best practice tips listed above, then you should download the event log for the scan. The log error messages could tell you whether the issue was with the login sequence itself or whether there was a general issue with the browser.

Some log entries may represent temporary failures that were later resolved. For example, if the target site imposes rate limits, you might see entries saying that the crawler was unable to log in. However, it may have logged in successfully later in the scan.

Note

You can use Burp AI to record login sequences in both Burp Suite Professional and Burp Suite DAST. Burp AI is designed to follow these best practices automatically. If you are struggling to record an effective sequence manually, consider using Burp AI to record it.

Related pages

Recorded login sequences.

Recording login sequences.

Troubleshooting recorded login sequences.
