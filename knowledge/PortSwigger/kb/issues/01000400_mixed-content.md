# Mixed content

Source: https://portswigger.net/kb/issues/01000400_mixed-content
Fetched: 2026-06-28T09:17:18.112131+00:00

Support Center

Issue Definitions

Mixed content

Mixed content

Twitter

WhatsApp

Facebook

Reddit

LinkedIn

Email

Description: Mixed content

The application loads pages over HTTPS that load other resources over unencrypted connections. An attacker suitably positioned to view a legitimate user's network traffic could record and monitor their interactions with these resources, which may indirectly disclose information about the user's activity on the application itself. Furthermore, an attacker able to modify traffic could alter these resources and potentially influence the application's appearance and behavior. Due to these concerns, users' web browsers may automatically display warnings and disable affected components of the page. As a result, this vulnerability currently has more of an impact on usability than security.

To exploit this vulnerability, an attacker must be suitably positioned to eavesdrop on the victim's network traffic. This scenario typically occurs when a client communicates with the server over an insecure connection such as public Wi-Fi, or a corporate or home network that is shared with a compromised computer. Common defenses such as switched networks are not sufficient to prevent this. An attacker situated in the user's ISP or the application's hosting infrastructure could also perform this attack. Note that an advanced adversary could potentially target any connection made over the Internet's core infrastructure.

Remediation: Mixed content

Ensure that all external resources the page references are loaded using HTTPS.

References

Mixed Content

Vulnerability classifications

CWE-16: Configuration

CWE-319: Cleartext Transmission of Sensitive Information

CAPEC-117: Interception

Typical severity

Information

Type index (hex)

0x01000400

Type index (decimal)

16778240

Twitter

WhatsApp

Facebook

Reddit

LinkedIn

Email

Burp Scanner

This issue - and many more like it - can be found using our

web vulnerability scanner

Read more

Get Burp

Scan your web application from just $499.00

Find out more
