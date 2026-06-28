# Professional 1.6.35

Source: https://portswigger.net/burp/releases/professional-1-6-35
Fetched: 2026-06-28T09:16:27.833232+00:00

This release adds the capability to report three new Scanner issues relating to HTTPS:

Unencrypted communications - This is reported when requests are made to a host using plain HTTP. In the near future, browsers will display a prominent security warning whenever this occurs. Due to recent revelations about the mass interception of unencrypted communications by various powerful adversaries, there is a push to use HTTPS everywhere. See the screenshot below for more details.

Mixed content - This is reported when a page is loaded over HTTPS but loads other resources, such as scripts and images, over plain HTTP. Modern browsers are disabling the affected resources by default, leading to usability issues when mixed content is used. If a user elects to re-enable mixed content, then this presents a security issue.

Strict transport security not enforced - This is reported when a host fails to prevent users from connecting to it over plain HTTP, using the Strict-Transport-Security header. In this situation, a suitably positioned attacker can bypass the use of SSL by rewriting HTTPS links as HTTP.
