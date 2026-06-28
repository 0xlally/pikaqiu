# SAML roulette: the hacker always wins

Source: https://portswigger.net/research/saml-roulette-the-hacker-always-wins
Fetched: 2026-06-28T09:17:29.063069+00:00

SAML roulette: the hacker always wins

Gareth Heyes

Researcher

@garethheyes

Published: Tuesday, 18 March 2025 at 14:55 UTC

Updated: Monday, 31 March 2025 at 07:10 UTC

Introduction

In this post, we’ll show precisely how to chain round-trip attacks and namespace confusion to achieve unauthenticated admin access on GitLab Enterprise by exploiting the ruby-saml library.

While researching this, GitHub independently discovered and patched our vulnerabilities. However, their disclosure omits key technical details, including the specific mutation and how to exploit it without authentication.

https://github.blog/security/sign-in-as-anyone-bypassing-saml-sso-authentication-with-parser-differentials/

We believe sharing the full details on how these attacks work is crucial for improving security by empowering everyone with the knowledge needed to identify, mitigate, and defend against such threats effectively.

This research began after we came across a fascinating post by Juho Forsén

detailing an XML round-trip vulnerability. What started as curiosity quickly spiraled into a deep dive into the intricacies of SAML, uncovering far more than we initially expected. We spent months exploring various round-trip attacks with the goal of presenting our findings at Black Hat. However, as luck would have it, we ran into a research collision with Alexander Tan (

ahacker1

), leading to our discoveries being patched before we could submit. Despite that twist, we believe this work is still worth sharing, and while it may not be hitting Black Hat this year, we hope you find it just as compelling.

Round-trip attacks 101

SAML libraries often parse an XML document, store it as a string, and later re-parse it. In Ruby-SAML, this process involves two different parsers: REXML, which is used to parse the document and validate the signature, and Nokogiri, which is used to access attributes. If any mutations occur during this process, the document may not be identical when parsed a second time.

For secure authorization, the document must be parsed and serialized consistently; otherwise, structural inconsistencies may arise. These inconsistencies can be exploited in a round-trip attack. By leveraging XML comments and CDATA sections, an attacker can manipulate the document’s structure during mutation, bypassing signature verification and effectively gaining unauthorized access by assuming another user's identity.

Round-trip attack on Ruby SAML/REXML

To facilitate testing, we developed a testbed to identify round-trip vulnerabilities and efficiently evaluate multiple SAML libraries. I began by examining the document type definition (DOCTYPE), as similar vulnerabilities had been discovered in the past. My initial approach focused on analyzing how XML entities were parsed, so I conducted tests in that area.

In Juho's original discovery, notation declarations were used to introduce inconsistencies in how quotes were interpreted. Building on this, I investigated whether any additional vulnerabilities had been overlooked. After extensive testing, I found that mutations could be introduced within the SYSTEM identifier.

During the initial parsing of the document, the first tag encountered is the original "assertion":

However, upon re-parsing the document, the outcome changes entirely, now reflecting the attacker's "assertion":

As shown, the single-quoted system identifier is converted to double quotes. However, since the identifier contains double quotes internally, this alters the XML document’s syntax, causing the XML comment to be processed and resulting in an entirely different node. My highly skilled colleague, Zak, refined this mutation into a more streamlined and effective attack vector:

This vector allowed exploitation of GitLab and any other application using the Ruby-SAML library by manipulating the document and forging assertions, effectively enabling an attacker to log in as any user. However, this was only part of the attack. My colleague Zak will demonstrate how this can be escalated to achieve unauthenticated administrator access on GitLab.

Privilege escalation at Gitlab via Round-trip attack

Understanding the vulnerability

GitLab relies on the Ruby-SAML library for SAML authentication. However, to achieve unauthenticated access, we need to take a closer look at the validation process, as it plays a critical role in the attack.

Before a round-trip occurs, the library verifies whether the SAMLResponse contains a valid certificate embedded in the document. This is done by computing the hash of the certificate and comparing it with the fingerprint stored on the server. Later, this certificate is used to validate the signature. Keep in mind that the signature is a key aspect of this attack, as it allows for a full account takeover without access to an organization's credentials.

The Signature Validation Process

Once the certificate is extracted from the SAMLResponse, the actual signature validation process begins. First, the document is converted back to XML format from its in-memory representation. This is where Gareth's round trip attack comes into play. At this stage, the library ignores attacker assertion and proceeds to validate the signature on the original element.

If an attacker forges the assertion element in a way that bypasses signature validation, additional security checks come into play. The most critical checks include:

The signed element's ID should match in both documents.

Canonicalization properties (which normalize XML documents) must be identical in both versions.

However, all other validation checks operate on the attacker assertion rather than the original signed document. This allows an attacker to arbitrarily modify validation fields without breaking the signature verification process:

Overcoming XML Schema Restrictions

One challenge in forging a signed XML document is that XML schema validation is performed using Nokogiri with predefined schema files. This presents a limitation: for an attacker to forge a valid signed XML document, they must first obtain a document that passes XML schema validation.

Understanding XML Schema Validation

An XML schema defines the structure of SAML XML documents, specifying:

Valid elements and attributes

The order and number of child elements

Data types for elements and attributes

In other words, the signed element must be a valid SAML protocol element—such as a login response, logout response, or metadata. You might find signed XML documents on developer forums, but that scenario is unlikely. Therefore, we will take a different approach. Instead, we introduce the Namespace confusion attack, which enables unauthenticated access to any application using Ruby-SAML.

Unauthenticated access to Gitlab

Before diving into the attack, let's recall how SAML schema validation works. The Identity Provider (IdP) signs only the Signature node, not the entire assertion.

Since Ruby-SAML uses two XML parsers:

REXML reads the Signature element.

Nokogiri reads the DigestValue.

A discrepancy between these two parsers can allow us to bypass signature validation.

Ruby-SAML searches for the Signature element using an XPath query:

Here, ds refers to the XML namespace. Normally, namespaces prevent element name conflicts, but we exploit a discrepancy in how namespaces are interpreted in XPath searches.

Consider the following scenario:

First Signature element lacks a direct namespace declaration (xmlns="http://www.w3.org/2000/09/xmldsig#"). Instead, we use an XML Doctype trick:

Security experts often focus on !ENTITY declarations in XXE attacks, but !ATTLIST declarations can also be used for exploitation. The !ATTLIST defines the Signature element and assigns it a namespace attribute. Both REXML and Nokogiri support doctype-based namespace declarations, but REXML has a crucial flaw:

XML standards prohibit duplicate attributes with the same name.

However, REXML ignores this restriction in doctype declarations.

This allows an attacker to define two conflicting namespace attributes, where the second one overrides the first.

As a result, REXML reads a FAKE digest value, while Nokogiri reads the REAL one.

Exploit Strategy

To exploit this discrepancy:

Create two Signature elements:

One with a valid Digest value.

One with a forged one.

This allows the attacker to bypass Ruby-SAML's Digest Validation process.

Exploiting Ruby < 3.4.2 by combining Namespace Confusion with Round-trip attack

While Namespace Confusion alone can exploit Ruby-SAML, it faces one limitation:

REXML's poor handling of XML marshalling/unmarshalling introduces another round trip issue. Before Ruby 3.4.2, REXML truncated !ATTLIST strings in doctype declarations, making the exploit fragile. In GitLab, this breaks the attack, but a combination of both vulnerabilities can still be used:

First XML parsing: REXML initially ignores the !ATTLIST value, treating it as a string literal. Second XML parsing: REXML then recognizes the !ATTLIST declaration, leading to full exploitation.

Leveraging WS-Federation to Obtain Signed XML

Finding a valid signed XML document can be challenging. Fortunately, Identity Providers (IdPs) silently support Single Sign-On protocol: WS-Federation by default for every tenant. WS-Federation provides signed metadata XML endpoints, such as:

https://login.microsoftonline.com/contoso.onmicrosoft.com....

Federation metadata documents are publicly accessible to any unauthorized user—all that’s required is the application's unique ID, which can be easily extracted from the Identity Provider's URL or found using a search engine.

While this metadata is not a valid SAML metadata document, a namespace confusion attack only requires a valid Signature element—one that is signed with the same certificate stored at the Service Provider. And it is.

By using this publicly available signed document, an attacker can:

Extract a legitimate Signature element.

Forge a fake signed assertion.

Completely bypass GitLab SAML authentication.

Conclusion

This attack highlights how combining round-trip attacks with namespace confusion can lead to unauthenticated access to GitLab. The vulnerability stems from inconsistencies in how different XML parsers handle document validation, allowing an attacker to manipulate signature verification.

Key Takeaways:

Differences in XML parsing can introduce exploitable inconsistencies.

Namespace confusion can be leveraged to bypass signature validation.

Legitimate signed WS-Federation metadata XML can be repurposed to forge assertions.

Mitigation

To prevent this type of attack, ensure that the same library is used for both parsing and validating signed XML documents. Avoid marshaling and unmarshaling untrusted user data. These vulnerabilities where fixed in versions 17.9.2, 17.8.5, 17.7.7 for GitLab Community Edition (CE) and Enterprise Edition (EE).

Make sure to follow us on X (formerly Twitter) and Bluesky, and join the official PortSwigger Discord to stay updated!

XML

SAML

Authorization

Back to all articles

Related Research

The Fragile Lock:

Novel Bypasses For SAML Authentication

10 December 2025

The Fragile Lock:

Novel Bypasses For SAML Authentication
