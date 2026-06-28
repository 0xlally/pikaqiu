# Unencrypted communications

Source: https://portswigger.net/kb/issues/01000200_unencrypted-communications
Fetched: 2026-06-28T09:17:18.090285+00:00

Support Center

Issue Definitions

Unencrypted communications

Unencrypted communications

Twitter

WhatsApp

Facebook

Reddit

LinkedIn

Email

Description: Unencrypted communications

The application allows users to connect to it over unencrypted connections. An attacker suitably positioned to view a legitimate user's network traffic could record and monitor their interactions with the application and obtain any information the user supplies. Furthermore, an attacker able to modify traffic could use the application as a platform for attacks against its users and third-party websites. Unencrypted connections have been exploited by ISPs and governments to track users, and to inject adverts and malicious JavaScript. Due to these concerns, web browser vendors are planning to visually flag unencrypted connections as hazardous.

To exploit this vulnerability, an attacker must be suitably positioned to eavesdrop on the victim's network traffic. This scenario typically occurs when a client communicates with the server over an insecure connection such as public Wi-Fi, or a corporate or home network that is shared with a compromised computer. Common defenses such as switched networks are not sufficient to prevent this. An attacker situated in the user's ISP or the application's hosting infrastructure could also perform this attack. Note that an advanced adversary could potentially target any connection made over the Internet's core infrastructure.

Please note that using a mixture of encrypted and unencrypted communications is an ineffective defense against active attackers, because they can easily remove references to encrypted resources when these references are transmitted over an unencrypted connection.

Remediation: Unencrypted communications

Applications should use transport-level encryption (SSL/TLS) to protect all communications passing between the client and the server. The Strict-Transport-Security HTTP header should be used to ensure that clients refuse to access the server over an insecure connection.

References

Marking HTTP as non-secure

Configuring Server-Side SSL/TLS

HTTP Strict Transport Security

Vulnerability classifications

CWE-326: Inadequate Encryption Strength

CAPEC-94: Man in the Middle Attack

CAPEC-157: Sniffing Attacks

Typical severity

Low

Type index (hex)

0x01000200

Type index (decimal)

16777728

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
