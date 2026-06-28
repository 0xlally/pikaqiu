# [MoBP] Can we automate? Yes we can

Source: https://portswigger.net/blog/mobp-can-we-automate-yes-we-can
Fetched: 2026-06-28T09:15:20.209860+00:00

[MoBP] Can we automate? Yes we can

Dafydd Stuttard |

Tuesday, 18 November 2008 at 07:22 UTC

MoBP

burp

automation

scanners

Anyone who has read chapter 19 of The Web Application Hacker's Handbook knows what I think about the limitations of automated vulnerability discovery. And I haven't had a Damascene conversion to a blind faith in the virtues of web scanners. So Burp Scanner was designed with a clear awareness of the kinds of issues that scanners can reliably look for.

The issues that Burp Scanner is able to identify mostly fall into three categories:

Input-based vulnerabilities targetting the client side, like XSS, CRLF injection, open redirection, etc.

Input-based vulnerabilities targetting the server side, like SQL injection, OS command injection, file path traversal, etc.

Non-input-based vulnerabilities which can be deduced directly by inspecting application requests and responses, like clear-text password submission, insecure cookie attributes, information leakage, etc.

Issues in category #1 can typically be detected by automated scanners with a very high degree of reliability. In most cases, everything that is relevant to finding the bug is visible on the client side. For example, with reflected XSS, the scanner can submit some benign input to the application, and look for this being echoed in responses. If it is echoed, the scanner can parse the response content to determine the context(s) in which the echoed input appears. It can then supply various modified inputs to determine whether strings that constitute an attack in those contexts are also echoed. If the scanner has knowledge of the wide range of broken input filters, and associated bypasses, that arise with web applications, it can check for all that apply to the context. By implementing a full decision tree of checks, driven by feedback from preceding checks, the scanner can effectively emulate the actions that a skilled and methodical human tester would perform. The only bugs that the scanner will miss are those with some unusual feature requiring intelligence to understand, such as a custom scheme for encapsulating inputs.

Issues in category #2 are inherently less amenable to automated detection, because in many cases the behaviours that are relevant to identifying the bugs occur only on the server, with little manifestation on the client side. For example, SQL injection bugs may return nice database errors in responses, or they may be fully blind. Burp employs various techniques to identify blind server-side injection issues, by inducing time delays, changing boolean conditions and performing fuzzy response diffing, etc. These techniques are inherently more error prone than the methods that are available in category #1. Nevertheless, Burp Scanner achieves a high success rate in this area. In fact, based on our pre-release testing, I'm willing to make a bold claim: Burp Scanner performs markedly better than the big commercial scanners that you have heard of.

Issues in category #3 can generally be reported with near-perfect reliability by an automated scanner, because they are visible within the application's own requests and responses, and only require good content parsers and a robust set of rules concerning what issues to infer from what observed behaviours.

Every issue that Burp Scanner reports is given a rating both for severity (high, medium, low, informational) and for confidence (certain, firm, tentative). When an issue has been identified using a less reliable technique, Burp makes you aware of this, by dropping the confidence level. Burp also shows you the full requests and responses that were used to identify each issue, with relevant sections of these highlighted, enabling you to quickly understand the application's behaviour, and reach your own conclusions.

Users of some other web scanners will notice that some issues which those scanners attempt to report do not appear on the above lists, most notably broken access controls and cross-site request forgery. In my experience, scanners do a terrible job of identifying these issues, reporting literally hundreds of false positives and missing many genuine bugs. These are vulnerabilities which require genuine intelligence to understand and identify, because their existence depends upon the context and meaning of the application's behaviour, and today's computers do not understand these features. As was described yesterday, Burp Scanner is designed for hackers - for users who know how to attack an application, but can benefit from using automation to speed up parts of their work. In my opinion, it is preferable to leave areas like access controls and XSRF to the human tester. Let Burp automate everything that can be reliably automated, giving you confidence in its output, and leaving you to focus on the aspects of the job that require human experience and intelligence to deliver.

MoBP

burp

automation

scanners

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
