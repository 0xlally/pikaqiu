# Professional / Community 1.7.34

Source: https://portswigger.net/burp/releases/professional-community-1-7-34
Fetched: 2026-06-28T09:16:32.187807+00:00

A number of bugs have been fixed:

A bug that prevented Burp from validating the common name of the Collaborator server certificate when polling over HTTPS. The impact of this bug is that if an attacker performed an active MITM attack within the network that is hosting the Collaborator server, then they would be able to correlate interaction data with polling clients. This would not normally be sufficient to infer specific vulnerabilities. (Note that for an attacker on the same network as the Burp user, the impact is lower, because the attacker can already view all traffic to the application and correlate requests with resulting Collaborator interactions.)

A bug that could cause HTTP Basic authentication credentials to leak to another domain when following redirections. The impact of this bug is that if a user configures HTTP Basic authentication for domain A, performs a scan of domain A, domain A redirects to domain B, and the user has included domain B within their target scope, then the credentials would be leaked. The same leakage could occur when working manually if a user manually follows a redirection to a malicious domain using Burp Repeater.

A bug that could allow an active MITM attacker to spoof textual content within the BApp Store tab and updates dialogs. Note that code signing prevents a MITM attacker from manipulating the actual installation of BApps or updates.

Some bugs in Burp's project repair function that caused some actually recoverable data to be lost.

A bug that prevented autocomplete popups from closing on some Linux window managers.

A bug that prevented temporary projects from being saved as a disk-based project more than once within the same Burp session.

A bug that prevented MacOS app nap from being disabled, with the result that automatic activity is slowed when Burp runs in the background.

A bug that prevented the Proxy from correctly handing requests that use a literal IPv6 address in the domain name of the requested URL.

The following enhancements have been made:

Burp ClickBandit has been updated to support sandboxed iframes.

A fix has been applied following a change in JRuby 9.2.0.0 that prevented Burp extensions written in Ruby from running.

Note that some of the security issues were reported through our bug bounty program, which pays generously for bugs large and small. Thanks are due to Bruno Morisson and Juho Nurminen.
