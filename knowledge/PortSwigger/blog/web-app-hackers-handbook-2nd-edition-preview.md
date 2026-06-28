# Web App Hacker's Handbook 2nd Edition - Preview

Source: https://portswigger.net/blog/web-app-hackers-handbook-2nd-edition-preview
Fetched: 2026-06-28T09:15:28.244084+00:00

Web App Hacker's Handbook 2nd Edition - Preview

Dafydd Stuttard |

Wednesday, 11 May 2011 at 10:01 UTC

books

The first draft of the new edition of WAHH is now completed, and the lengthy editing and production process is underway. Just to whet everyone's appetite, I'm posting below an exclusive extract from the Introduction, describing what has changed in the second edition.

(And in a vain attempt to quell the tidal wave of questions: the book will be published in October; there won't be any more extracts; we don't need any proof readers, thanks.)

What’s Changed in the Second Edition?

In the four years since the first edition of this book was published, much has changed and much has stayed the same. The march of new technology has, of course, continued apace, and this has given rise to specific new vulnerabilities and attacks. The ingenuity of hackers has also led to the development of new attack techniques, and new ways of exploiting old bugs. But neither of these factors, technological or human, has created a revolution. The technologies used in today’s applications have their roots in those that are many years old. And the fundamental concepts involved in today’s cutting-edge exploitation techniques are older than many of the researchers who are applying them so effectively. Web application security is a dynamic and exciting area to work in, but the bulk of what constitutes our accumulated wisdom has evolved slowly over many years, and would have been distinctively recognizable to practitioners working a decade or more ago.

This second edition is by no means a “complete rewrite” of the first edition. Most of the material in the first edition remains valid and current today. Approximately 30% of the content in the second edition is either completely new or extensively revised. The remaining 70% has had minor modifications or none at all. For readers who have upgraded from the first edition and may feel disappointed by these numbers, you should take heart. If you have mastered all of the techniques described in the first edition, then you already have the majority of the skills and knowledge that you need. You can focus your reading on what is new in this second edition, and quickly learn about the areas of web application security that have changed in recent years.

One significant new feature of the second edition is the inclusion throughout the book of real examples of nearly all of the vulnerabilities that are covered. Any place you see a Try it! link, you can go online and work interactively with the example being discussed, to confirm that you can find and exploit the vulnerability it contains. There are several hundred of these labs, which you can work through at your own pace as you read the book. The online labs are available on a subscription basis for a modest fee, to cover the costs of hosting and maintaining the infrastructure involved.

For readers wishing to focus their attention on what is new in the second edition, there follows a summary of the key areas where material has been added or rewritten.

Chapter 1, “Web Application (In)security”, has been partly updated to reflect new uses of web applications, some broad trends in technologies, and the ways in which a typical organization’s security perimeter has continued to change.

Chapter 2, “Core Defense Mechanisms”, has received minor changes, with a few examples added of generic techniques for bypassing input validation defenses.

Chapter 3, “Web Application Technologies”, has been expanded with some new sections describing technologies that are either new or were described more briefly elsewhere within the first edition. The areas added include REST, Ruby on Rails, SQL, XML, web services, CSS, VBScript, the document object model, Ajax, JSON, the same-origin policy, and HTML5.

Chapter 4, “Mapping the Application”, has received various minor updates to reflect developments in techniques for mapping content and functionality.

Chapter 5, “Bypassing Client-Side Controls”, has been updated more extensively. In particular, the section on browser extension technologies has been largely rewritten to include more detailed guidance on generic approaches to bytecode decompilation and debugging, how to handle serialized data in common formats, and how to deal with common obstacles to your work, including non-proxy-aware clients and problems with SSL. The chapter also now covers Silverlight technology.

Chapter 6, “Attacking Authentication”, remains current and has received only minor updates.

Chapter 7, “Attacking Session Management”, has been updated to cover new tools for automatically testing the quality of randomness in tokens. It also contains new material on attacking encrypted tokens, including practical techniques for token tampering without knowing either the cryptographic algorithm or the encryption key being used.

Chapter 8, “Attacking Access Controls”, now covers access control vulnerabilities arising from direct access to server-side methods, and from platform misconfiguration where rules based on HTTP methods are used to control access. It also describes some new tools and techniques that you can use to partially automate the frequently onerous task of testing access controls.

The material in Chapters 9 and 10 has been reorganized to create more manageable chapters and a more logical arrangement of topics. Chapter 9, “Attacking Data Stores” focuses on SQL injection and similar attacks against other data store technologies. As SQL injection vulnerabilities have become more widely understood and addressed, this material now focuses more on the practical situations where SQL injection is still to be found. There are also minor updates throughout to reflect current technologies and attack methods, and there is a new section on using automated tools for exploiting SQL injection vulnerabilities. The material on LDAP injection has been largely rewritten to include more detailed coverage of specific technologies (Microsoft Active Directory and OpenLDAP), as well as new techniques for exploiting common vulnerabilities. This chapter also now covers attacks against NoSQL.

Chapter 10, “Attacking Back-End Components”, covers the other types of server-side injection vulnerabilities that were previously included in Chapter 9. There are new sections covering XML external entity injection and injection into back-end HTTP requests, including HTTP parameter injection/pollution and injection into URL rewriting schemes.

Chapter 11, “Attacking Application Logic”, includes more real-world examples of common logic flaws in input validation functions. With the increased usage of encryption to protect application data at rest, we also include an example of how to identify and exploit encryption oracles to decrypt encrypted data.

The topic of attacks against other application users, previously covered by Chapter 12, has now been split into two separate chapters, as this material was becoming unmanageably large as a single chapter. Chapter 12, “Attacking Users: Cross-Site Scripting” focuses solely on XSS, and this material has been extensively updated in various areas. The sections on bypassing defensive filters to introduce script code have been completely rewritten to cover new techniques and technologies, including various little-known methods for executing script code on current browsers. There is also much more detailed coverage of methods for obfuscating script code to bypass common input filters. There are several new examples of real-world XSS attacks. There is a new section on delivering working XSS exploits in challenging conditions, which covers escalating an attack across application pages, exploiting XSS via cookies and the Referer header, and exploiting XSS in non-standard request and response content such as XML. There is a detailed examination of browsers’ built-in XSS filters, and how these can be circumvented to deliver exploits. There are new sections on specific techniques for exploiting XSS in webmail applications and in uploaded files. Finally, there are various updates to the defensive measures that can be used to prevent XSS attacks.

The new Chapter 13, “Attacking Users: Other Techniques”, draws together the remainder of this huge area. The topic of cross-site request forgery has been updated to include CSRF attacks against the login function, common defects in anti-CSRF defenses, UI redress attacks, and common defects in framebusting defenses. A new section on cross-domain data capture includes techniques for stealing data by injecting text containing non-scripting HTML and CSS, and various techniques for cross-domain data capture using JavaScript and E4X. A new section examines the same-origin policy in more detail, including its implementation in different browser extension technologies, the changes brought by HTML5, and ways of crossing domains via proxy service applications. There are new sections on client-side cookie injection, SQL injection and HTTP parameter pollution. The section on client-side privacy attacks has been expanded to include storage mechanisms provided by browser extension technologies and HTML5. Finally, a new section has been added drawing together general attacks against web users that do not depend upon vulnerabilities in any particular application. These attacks can be delivered by any malicious or compromised web site, or by an attacker who is suitably positioned on the network.

Chapter 14, “Automating Customized Attacks”, has been expanded to cover common barriers to automation, and how to circumvent these. Many applications employ defensive session-handling mechanisms that terminate sessions, use ephemeral anti-CSRF tokens, or use multi-stage processes to update application state. Some new tools are described for handling these mechanisms, which let you continue using automated testing techniques. A new section examines CAPTCHA controls, and some common vulnerabilities that can often be exploited to circumvent them.

Chapter 15, “Exploiting Information Disclosure”, contains new sections about XSS in error messages and exploiting decryption oracles.

Chapter 16, “Attacking Compiled Applications”, has not been updated.

Chapter 17, “Attacking Application Architecture”, contains a new section about vulnerabilities that arise in cloud-based architectures, and updated examples on exploiting architecture weaknesses.

Chapter 18, “Attacking the Application Server”, contains several new examples of interesting vulnerabilities in application servers and platforms, including Jetty, the JMX management console, ASP.NET, Apple iDisk server, Ruby WEBrick web server, and Java web server. It also has a new section looking at practical approaches to circumventing web application firewalls..

Chapter 19, “Finding Vulnerabilities in Source Code”, has not been updated.

Chapter 20, “A Web Application Hacker’s Toolkit”, has been updated with details of the latest features in proxy-based tool suites. It contains new sections about how to proxy the traffic of non-proxy-aware clients, and how to eliminate SSL errors in browsers and other clients, caused by the use of an intercepting proxy. There is a detailed description of the workflow that is typically employed when you are testing using a proxy-based tool suite. There is a new discussion about current web vulnerability scanners, and the optimal approaches to using these in different situations.

books

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
