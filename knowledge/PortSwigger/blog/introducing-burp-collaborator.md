# Introducing Burp Collaborator

Source: https://portswigger.net/blog/introducing-burp-collaborator
Fetched: 2026-06-28T09:15:18.103358+00:00

Introducing Burp Collaborator

Dafydd Stuttard |

Thursday, 16 April 2015 at 10:42 UTC

Today's release of Burp Suite introduces Burp Collaborator. This new feature has the potential to revolutionize web security testing. Over time, Burp Collaborator will enable Burp to detect issues like blind XSS, server-side request forgery, asynchronous code injection, and various as-yet-unclassified vulnerabilities.

In the coming months, we will be adding many exciting new capabilities to Burp, based on the Collaborator technology. See the "Release roadmap" section towards the end of this post for more details.

This blog post looks at:

Some important limitations of the conventional web testing model.

How Burp Collaborator will address these limitations.

Lots of real-world vulnerabilities that don't fit into the usual classifications.

The conventional web testing model

At its core, conventional web security testing is fairly simple: we send payloads to the target application, and analyze responses to identify security vulnerabilities.

This model is well established and understood, and enables us to identify many kinds of security issues. Much of the work can also be automated with a degree of reliability.

However, the conventional testing model also misses lots of bugs, for example:

We miss "super-blind" injection vulnerabilities. People often refer to "blind SQL injection", meaning only that an application doesn't return helpful error messages when a payload breaks the interpreted query. But in some situations, a successful injection has no detectable effect on application responses: that is, no difference in response contents or timing. For example, SQL injection into an asynchronous logging function is typically super-blind in this sense.

We miss many vulnerabilities involving stored data. Bugs like stored XSS are easy to find in principle (by monitoring later responses for earlier payloads). But other stored bugs are much harder to find. For example, in stored (or second-order) SQL injection, data placed safely into a database is later read back and concatenated into a SQL query. To find bugs like this in the conventional model, we might need to brute force every combination of requests within the application, to send a payload in request 1 and look for effects via request 2.

We miss vulnerabilities where a successful attack can only be detected in areas of the application that are not directly visible to the tester. For example, stored XSS vulnerabilities affecting admin-only pages.

We miss many vulnerabilities involving interaction with external systems. Bugs in this category are often given labels like "server-side request forgery" and "remote file include".

Enter Burp Collaborator

Burp Collaborator augments the conventional testing model with a new component, distinct from Burp and the target application. Burp Collaborator can:

Capture external interactions initiated by the target that are triggered by Burp's attack payloads.

Deliver attacks back against the target in responses to those interactions.

Enable the reliable detection of many new vulnerabilities.

The basic design of Burp Collaborator includes the following features:

The Burp Collaborator server runs on the public web (by default).

It uses its own dedicated domain name, and the server is registered as the authoritative DNS server for this domain.

It provides a DNS service that answers any lookup on its registered domain (or subdomains) with its own IP address.

It provides an HTTP/HTTPS service, and uses a valid, CA-signed, wildcard SSL certificate for its domain name.

In future, custom implementations of various other network services will be provided, such as SMTP and FTP.

Detecting external service interaction

External service interaction occurs when a payload submitted to the target application causes it to interact with an arbitrary external domain using some network protocol:

This behavior is sometimes referred to as "server-side request forgery". We prefer the term "external service interaction" because this captures more general behavior: interactions can be triggered using protocols other than HTTP, such as SMB or FTP.

External service interaction can represent a serious vulnerability because it can allow the application server to be used as an attack proxy to target other systems. This may include public third-party systems, internal systems within the same organization, or services available on the local loopback adapter of the application server itself. Depending on the network architecture, this may expose highly vulnerable internal services that are not otherwise accessible to external attackers.

The Burp payload includes a random subdomain of the main Collaborator domain. When an HTTP-based external service interaction occurs, the Collaborator server will typically receive a DNS lookup for this subdomain, followed by an HTTP request. However, it is noteworthy that the DNS lookup alone is sufficient to report an issue. If a payload starting "http://..." causes a DNS-only interaction, then this strongly indicates that outbound HTTP from the server is being blocked at the network layer. In this situation, a follow-up attack could target other systems internal to the organization or running on the server's loopback adapter. For this reason, Burp separately reports any DNS and HTTP interactions that are triggered.

In its issue advisory, Burp reports the in-band request that was made to the application, and the full details of the interactions that occurred with the Collaborator server:

Detecting out-of-band resource load

Out-of-band resource load occurs when a payload submitted to the target application causes it to fetch content from an arbitrary external domain using some network protocol, and incorporate that content into its own response to the request that contained the payload:

This behavior is sometimes referred to as "remote file include". However, this label has connotations of vulnerabilities like PHP remote script inclusion. We prefer the term "out-of-band resource load" because this captures the more general behavior where content obtained out-of-band is somehow incorporated into the application's own responses. (Server-side execution of content obtained out-of-band is discussed later in this post.)

Out-of-band resource load is a potentially high-risk issue. An attacker can leverage the application as a two-way attack proxy, sending arbitrary payloads to, and retrieving content from, other systems that the application server can interact with. Again, this may include third-party systems or sensitive internal systems that are otherwise inaccessible.

Additionally, the application's processing of out-of-band content exposes some important and non-conventional attack surface. The possible ways of targeting this are described in more detail later in this post.

Burp reports the full details of the interactions that occurred with the Collaborator server, showing how the content returned from the Collaborator is propagated back in the application's in-band response to the user:

Detecting out-of-band XSS

In cases where out-of-band resource load is identified, the most obvious related issue to check for is out-of-band XSS:

Out-of-band XSS doesn't fall under the usual XSS classifications:

Not reflected: the payload isn't reflected from the current in-band request to the target application.

Not stored: the payload isn't (necessarily) stored by the target application.

Not DOM-based: existing JavaScript isn't (necessarily) involved.

Out-of-band versions of some other client-side issues arise in a similar way, including HTTP response header injection, and open redirection.

Detecting "super-blind" injection bugs

In cases where a code injection attack cannot trigger any detectable effect in the application's own responses (that is, any difference in response contents or timing), we can often detect the vulnerability by using payloads that trigger an external service interaction when the injection is successful:

Viable payloads exist for many categories of injection vulnerabilities, including SQL injection, XXE injection, OS command injection, etc. With these payloads, Burp does not need to observe any effect in the application's own responses, and successful injection can be detected solely through the fact that the external interaction occurred. Note also that in this situation, only a DNS interaction is needed to confirm the injection. Since outbound DNS is almost always permitted because servers need to use it, network-layer filters are unlikely to hinder detection.

Detecting out-of-band injection bugs

When any type of external service interaction is identified, we can use the Collaborator server's responses to deliver conventional input-based payloads back to the application. Depending on how the application processes the Collaborator's responses, potentially any input-based vulnerability could exist, including SQL injection and server-side code execution:

Vulnerabilities like this might be surprisingly common because they are not thoroughly tested for at present.

Detecting stored out-of-band bugs

In addition to the out-of-band injection bugs described in the previous section, there is the potential for stored out-of-band attacks in any situation where the target application processes data that it receives in responses from the Collaborator server.

Detecting stored out-of-band resource load is straightforward:

Based on the above behavior, we can also test for stored out-of-band XSS:

Whenever we discover stored out-of-band resource load, we are able to link an entry point and a retrieval point within the application. We know that the application is storing and processing data between the two locations, so we can check for stored out-of-band versions of any type of input-based bug:

Detecting blind stored vulnerabilities

We already described how we can detect "super-blind" injection bugs using payloads that trigger an external service interaction when the injection is successful. We can also detect cases where these (or other) payloads are stored and processed later in an unsafe way. Deferred interactions with the Collaborator server enable us to report blind stored versions of many input-based bugs.

For example, blind stored XSS arises when the result of a stored XSS attack cannot be detected from the tester's perspective, because the tester does not have access to the area of the application where the stored attack executes. We can detect these issues by submitting stored XSS payloads that will trigger an interaction with the Collaborator server when the attack later executes:

In this example, when an application administrator visits the relevant protected page, the stored attack executes, and Burp can confirm this via the Collaborator server. Further, the HTTP Referer header in the administrator's incoming request to the Collaborator lets us identify the location of the XSS retrieval page, which we cannot directly see ourselves.

Reporting deferred interactions

In general, any Collaborator-related payload that Burp sends to the target application might cause deferred interactions with the Collaborator server. This can happen in two main ways:

Conventional storage and later processing of input, e.g. stored SQL injection.

Immediate asynchronous processing, e.g. by a mail spooler.

When Burp polls the Collaborator server to retrieve details of any interactions that were triggered by a given test, it will also receive details of any deferred interactions that have resulted from its earlier tests. Burp can then report the relevant issues to the user retrospectively.

Because every Collaborator payload that Burp sends to the target includes a unique, one-time random identifier, when a deferred interaction occurs, Burp can use the identifier to pinpoint exactly where the payload originated, including the original request, the insertion point and the full payload.

Imagine this: A day after you finish your test, you fire up Burp Suite and open the same project. Burp polls the Collaborator and reports some deferred-interaction issues, with all the usual details. You call up the client and tell them about all their blind stored XSS ...

Other network services

We have focused on vulnerabilities involving DNS and HTTP interactions between the target application and Burp Collaborator. In fact, we can use payloads to trigger Collaborator interactions using various other protocols. For example, we can potentially:

Inject into mail headers and detect this via SMTP interactions with the Collaborator.

Trigger a connection to an SMB share and capture the NTLM handshake.

Trigger a connection to an SSH service and capture credentials.

How prevalent are these issues?

Some of the application behavior we have described is relatively rare, for example:

Getting a URL from a request parameter.

Fetching the response from the URL.

Processing the response contents in some way.

Other behavior is relatively common, for example:

Storage of conventional user-supplied data.

Later reuse in a potentially unsafe manner.

Super-blind processing of results.

It seems fair to say that the cases where the relevant behavior exists are relatively untested, even by skilled attackers:

Full Collaborator-style functionality is expensive to create, requiring a custom domain name, wildcard SSL certificate, and custom implementations of various network protocols.

Even with a suitable Collaborator-like server deployed, manually correlating input entry points and results of stored and deferred interactions is time consuming and error-prone.

No automated scanner currently does everything that we've described.

Hence, we may reasonably conclude that where the relevant behavior exists, there is lots of low hanging fruit to be found. Anecdotal evidence from skilled bug bounty hunters supports this conclusion. (Sorry guys, Burp will soon open up these bugs to the masses!)

Manual testing tools

In the hands of a well-designed automated scanner, the Collaborator concept is incredibly powerful. There is also potential for some great manual tools that leverage the Collaborator's capabilities. These tools would let users manually verify and exploit issues that Burp Scanner has reported (for example, performing custom data exfiltration via super-blind SQL injection), and also do their own targeted testing of relevant attack surface.

Two key manual tools are planned:

Burp Collaborator client

Burp Intruder integration

Burp Collaborator client

This will include the following components

Monitoring function - This will generate a unique Collaborator identifier for you to use in your own test payloads. It will poll the Collaborator and give full details of any interactions that result from using this identifier.

Response-control function - This will let you configure the response that the Collaborator should return to targets that interact with it.

Used in conjunction with Burp Repeater, the Collaborator client will give you real-time three-way interaction between Burp, the target application, and the Collaborator server, all under full manual control.

Burp Intruder integration

This will provide a new Intruder attack option to use out-of-band payload delivery when an external service interaction has been identified. With the option enabled, Burp will send a unique Collaborator URL as the in-band payload to the target application. When the target performs the external interaction, the Collaborator server will return the actual configured payload to the target.

Security of Collaborator data

At this point, you may be forgiven for asking "Does this mean that the Collaborator server holds details of all the vulnerabilities that are found using it? What's to stop anyone else fetching the details of my issues?".

In fact, you're not just forgiven for asking this: we'd be disappointed if you didn't. We've spent a lot of time ourselves thinking about these questions.

What data does the Collaborator server store?

In most cases, when a vulnerability is found, the Collaborator server will not receive enough information to identify the vulnerability. It does not see the HTTP request that was sent from Burp to the target application. In a typical case, it will record that an interaction was received from somewhere, including a random identifier that was generated by Burp. Occasionally, the Collaborator server will receive some application-specific data: for example, the contents of an email generated through a user registration form.

How is retrieval of Collaborator data controlled?

The Collaborator functionality is designed so that only the instance of Burp that generated a given payload is able to retrieve the details of any interactions that result from that payload. This requirement is implemented as follows:

Each instance of Burp generates a securely random secret.

Each Collaborator-related payload that Burp sends to the target application includes a random identifier that is derived from a one-way hash (cryptographic checksum) of the secret.

Any resulting interactions with the Collaborator will include this identifier in the transmitted data (for example, in the subdomain of a DNS lookup, or the Host header of an HTTP request).

The secret is only ever sent by Burp to the Collaborator server, to poll for details of the resulting interactions. This is done using HTTPS, unless overridden in Burp's options.

When the Collaborator server receives a polling request, it performs the one-way hash of the submitted secret, and retrieves the details of any recorded interactions containing identifiers that are derived from that hash.

Hence, only the instance of Burp that generated the secret is able to retrieve the details of any interactions that are triggered by its payloads.

Further to this mechanism, the following precautions are also implemented in the Collaborator server to protect against unauthorized access to its data:

Details of interactions are stored in ephemeral process memory only.

No data of any kind is in recorded in any persistent form: for example, a database or log file.

Details of interactions are typically retrieved by Burp shortly after they occur, and are then discarded by the server.

Details of old interactions that have not been retrieved by Burp are discarded after a fixed interval.

There is no administrative function for viewing interaction details, only the retrieval mechanism already described.

The Collaborator server does not by design receive any data that could be used to identify any individual Burp user (such as an account name or license key).

Private Collaborator servers

Users who remain paranoid about any data passing through the shared Burp Collaborator server have two alternative options. If you wish, you can completely disable use of the Collaborator feature within Burp. Even better, you can choose to run your own private Collaborator server:

Anyone with a Burp Suite Professional license can run their own instance of the Collaborator server. To do this fully effectively, you will need a host server, a dedicated domain name, and a valid CA-signed wildcard SSL certificate. Private Collaborator servers without a suitable domain name or SSL certificate will be able to support some, but not all, of the Collaborator-related capabilities within Burp.

You can protect your private Collaborator instance at the network layer: you can configure different network interfaces to receive interactions and answer polling requests, and you can apply whatever IP restrictions you want, given the locations of your targets and testers. The option to use a private Collaborator server is likely to appeal to penetration testing firms and in-house security teams. It can also enable individual testers to deploy a Collaborator instance when testing on private closed networks with no Internet access.

See the documentation on deploying a private Collaborator server for more details.

Release roadmap

Today's Burp Suite release includes the following elements:

Core Burp Collaborator platform and server.

Support for DNS, HTTP and HTTPS services.

Reporting of external service interaction and out-of-band resource load.

Support for private Collaborator servers.

In the coming months, we will deliver some of the other capabilities described in this post, including:

Out-of-band versions of all input-based scan checks.

Detection of various "super-blind" vulnerabilities.

Checks for stored versions of all relevant vulnerabilities.

Handling of deferred interactions and retrospective reporting of resulting issues.

Support for other network service protocols, and associated test payloads.

Manual testing tools.

Read the full Burp Collaborator documentation

Have fun!

Dafydd Stuttard

@DafyddStuttard

Latest Posts

Burp Extensibility 2026: Awards, Talks, and Highlights

19 June 2026

Burp Extensibility 2026: Awards, Talks, and Highlights

The beast needs a cage: What's next for AppSec post-Mythos

12 May 2026

The beast needs a cage: What's next for AppSec post-Mythos

3 ways custom scan checks turn practitioner knowledge into scalable automation

01 May 2026

3 ways custom scan checks turn practitioner knowledge into scalable automation

Senior pentesters have a deeply refined intuition about what is vulnerable in an environment. The problem? That expertise is often siloed with an individual and trapped in their notes or Python scripts.
