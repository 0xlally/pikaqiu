# External service interaction (SMTP)

Source: https://portswigger.net/kb/issues/00300220_external-service-interaction-smtp
Fetched: 2026-06-28T09:17:11.211758+00:00

Support Center

Issue Definitions

External service interaction (SMTP)

External service interaction (SMTP)

Twitter

WhatsApp

Facebook

Reddit

LinkedIn

Email

Description: External service interaction (SMTP)

External service interaction arises when it is possible to induce an application to interact with an arbitrary external service, such as a web or mail server. The ability to trigger arbitrary external service interactions does not constitute a vulnerability in its own right, and in some cases might even be the intended behavior of the application. However, in many cases, it can indicate a vulnerability with serious consequences.

The ability to send requests to other systems can allow the vulnerable server to be used as an attack proxy. By submitting suitable payloads, an attacker can cause the application server to attack other systems that it can interact with. This may include public third-party systems, internal systems within the same organization, or services available on the local loopback adapter of the application server itself. Depending on the network architecture, this may expose highly vulnerable internal services that are not otherwise accessible to external attackers.

The facility to generate an email to an arbitrary address is often intended application behavior. But this is not necessarily the case, particulary in cases where the destination address is not explicitly entered on-screen by the user.

Remediation: External service interaction (SMTP)

You should review the purpose and intended use of the relevant application functionality, and determine whether the ability to trigger arbitrary external service interactions is intended behavior. If so, you should be aware of the types of attacks that can be performed via this behavior and take appropriate measures. These measures might include blocking network access from the application server to other internal systems, and hardening the application server itself to remove any services available on the local loopback adapter.

If the ability to trigger arbitrary external service interactions is not intended behavior, then you should implement a whitelist of permitted services and hosts, and block any interactions that do not appear on this whitelist.

References

Burp Collaborator

Out-of-band application security testing (OAST)

Vulnerability classifications

CWE-16: Configuration

CWE-406: Insufficient Control of Network Message Volume (Network Amplification)

Typical severity

Information

Type index (hex)

0x00300220

Type index (decimal)

3146272

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
