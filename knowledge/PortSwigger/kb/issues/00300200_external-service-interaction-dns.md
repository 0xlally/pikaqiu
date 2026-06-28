# External service interaction (DNS)

Source: https://portswigger.net/kb/issues/00300200_external-service-interaction-dns
Fetched: 2026-06-28T09:17:10.677527+00:00

Support Center

Issue Definitions

External service interaction (DNS)

External service interaction (DNS)

Twitter

WhatsApp

Facebook

Reddit

LinkedIn

Email

Description: External service interaction (DNS)

The ability to induce an application to interact with an arbitrary external service, such as a web or mail server, does not constitute a vulnerability in its own right. This might even be the intended behavior of the application. However, in some cases, it can indicate a vulnerability with serious consequences.

If you can trigger DNS-based interactions, it is normally possible to trigger interactions using other service types. Burp Scanner reports these as separate issues. You may find that a payload, such as a URL, only triggers a DNS-based interaction, even though you were expecting interactions with a different service as well. This could be due to egress filters on the network layer that prevent the application from connecting to these other services. However, some systems perform DNS lookups without any intention of connecting to the remote host. This behavior is typically harmless.

The ability to send requests to other systems can allow the vulnerable server to be used as an attack proxy. By submitting suitable payloads, an attacker can cause the application server to attack other systems that it can interact with. This may include public third-party systems, internal systems within the same organization, or services available on the local loopback adapter of the application server itself. Depending on the network architecture, this may expose highly vulnerable internal services that are not otherwise accessible to external attackers.

Remediation: External service interaction (DNS)

You should review the purpose and intended use of the relevant application functionality, and determine whether the ability to trigger arbitrary external service interactions is intended behavior. If so, you should be aware of the types of attacks that can be performed via this behavior and take appropriate measures. These measures might include blocking network access from the application server to other internal systems, and hardening the application server itself to remove any services available on the local loopback adapter.

If the ability to trigger arbitrary external service interactions is not intended behavior, then you should implement a whitelist of permitted services and hosts, and block any interactions that do not appear on this whitelist.

Out-of-Band Application Security Testing (OAST) is highly effective at uncovering high-risk features, to the point where finding the root cause of an interaction can be quite challenging. To find the source of an external service interaction, try to identify whether it is triggered by specific application functionality, or occurs indiscriminately on all requests. If it occurs on all endpoints, a front-end CDN or application firewall may be responsible, or a back-end analytics system parsing server logs. In some cases, interactions may originate from third-party systems; for example, a HTTP request may trigger a poisoned email which passes through a link-scanner on its way to the recipient.

References

Burp Collaborator

Out-of-band application security testing (OAST)

PortSwigger Research: Cracking the Lens

Vulnerability classifications

CWE-918: Server-Side Request Forgery (SSRF)

CWE-406: Insufficient Control of Network Message Volume (Network Amplification)

Typical severity

Information

Type index (hex)

0x00300200

Type index (decimal)

3146240

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
