# WebAuthn passkeys in recorded logins

Source: https://portswigger.net/burp/documentation/dast/user-guide/scanning-web-apps/configure-authentication/webauthn
Fetched: 2026-06-28T09:15:41.041498+00:00

DAST

WebAuthn passkeys in recorded logins

Last updated:

June 18, 2026

Read time:

2 Minutes

Cloud

Self-hosted

You can configure a recorded login to authenticate using WebAuthn. This includes passkeys, biometrics such as fingerprint or facial recognition, device PINs such as Windows Hello, and hardware security keys such as YubiKey.

Support is limited to applications that implement the WebAuthn standard. Non-standard implementations or flows tied to specific hardware may not be supported.

If your login uses a passkey, you must capture it using the Login Recorder for Burp Suite extension before recording your login sequence. Existing passkeys in your application or identity provider cannot be used unless they were captured and exported using the extension.

To capture a passkey, do one of the following:

Capture a new passkey using the Login Recorder for Burp Suite extension.

Import a passkey that was previously captured and exported from the extension.

Note

Do not delete any passkeys used in recorded logins from your application or identity provider. Burp uses them to authenticate during scans, simulating the WebAuthn authentication process automatically.

Capturing a new passkey

Use this option if you don't already have a passkey captured using the Login Recorder for Burp Suite extension.

Open the Login Recorder for Burp Suite extension.

Enable the My login uses a passkey toggle.

Click Add passkey.

Click Capture new passkey. This enables passkey capture in your browser.

Go to your application or identity provider and create a new passkey. The extension captures it automatically.

Return to the extension and click Stop capturing.

You can now record your login sequence using this passkey. For more information, see Recording login sequences.

Note

Passkeys don't persist between sessions in the extension. Export any passkeys you want to reuse in future recorded login sequences before closing the browser.

Importing a passkey

Use this option if you've previously captured and exported a passkey using the Login Recorder for Burp Suite extension.

Open the Login Recorder for Burp Suite extension.

Enable the My login uses a passkey toggle.

Click Add passkey.

Click Import passkey.

Upload the passkey file.

You can now record your login sequence using this passkey. For more information, see Recording login sequences.

Related pages

Using recorded logins.

Managing steps in a recorded login.

Best practice for recording login sequences.
