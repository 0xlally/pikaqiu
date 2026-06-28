# Burp Suite now reports blind XXE injection

Source: https://portswigger.net/blog/burp-suite-now-reports-blind-xxe-injection
Fetched: 2026-06-28T09:15:10.341296+00:00

Burp Suite now reports blind XXE injection

Dafydd Stuttard |

Wednesday, 6 May 2015 at 14:33 UTC

Today's release of Burp Suite Professional updates the Scanner to find blind XML external entity (XXE) injection vulnerabilities.

Burp has previously checked for XXE injection by modifying client-submitted XML data to define an external entity that references a known file, for example:

<!DOCTYPE foo [<!ENTITY xxe7eb97 SYSTEM "file:///etc/passwd"> ]>

and then using the defined entity within a data field of the document. If the application responds with the contents of the specified file, then this indicates that the application processed the injected external entity, and Burp reports the issue.

This technique works well in situations where the application echoes the value of the defined entity in its response. But there are very many cases of blind XXE injection where this does not occur. In these situations, the application processes and evaluates the injected external entity but does not give any indication in its response that this has taken place.

Burp's new capability lets it report blind XXE injection in these situations. Burp now attempts to define an external entity that references a URL on an external domain, for example:

<!DOCTYPE foo [<!ENTITY xxe46471 SYSTEM "http://4mr71zbvk10c5vd1k074izfvbmhnxdi7xw.burpcollaborator.net"> ]>

When the vulnerable application processes this external entity, it fetches the contents of the specified URL, and so interacts with the Burp Collaborator server (typically a DNS lookup followed by an HTTP request). After sending the blind injection payload, Burp Suite polls the Collaborator server to determine that the interaction occurred, and so reports the issue.

Full details of the vulnerability are reported to the user, including both blind and non-blind behaviors, and all interactions with the Collaborator server:

Due to the lack of widespread testing for blind XXE injection vulnerabilities in the past, it appears that these vulnerabilities are relatively common in application functions where client-submitted XML is processed on the server side. Burp's new capability in detecting blind XXE injection is an excellent example of what it is possible to build on the core Burp Collaborator platform. Over the coming months, we will be adding a lot of new capabilities to Burp, based on this platform. Users are encouraged to make use of the Collaborator feature, either via the public Collaborator server or a private deployment.

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
