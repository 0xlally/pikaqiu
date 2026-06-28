# Comparing web application scanners, part 2

Source: https://portswigger.net/blog/comparing-web-application-scanners-part-2
Fetched: 2026-06-28T09:15:13.676135+00:00

Comparing web application scanners, part 2

Dafydd Stuttard |

Monday, 28 June 2010 at 09:52 UTC

burp

scanners

A new paper has been published by UCSB analysing the performance of various web application vulnerability scanners, which the authors say is "the largest evaluation of web application scanners in terms of the number of tested tools ... and the class of vulnerabilities analyzed".

The authors created their own test application containing a wide variety of vulnerabilities and crawling challenges, and carried out what appears to be a very detailed and rigorous analysis of each scanner's performance against this application.

Scanners were scored based on their ability to identify different types of vulnerabilities in different scanning modes. The overall scores, together with the prices of each scanner, were as follows:

ScannerScore  Price

Acunetix14$4,995-$6,350

Webinspect13$6,000-$30,000

Burp13$191

N-Stalker13$899-$6,299

AppScan10$17,550-$32,500

w3af9Free

Paros6Free

Hailstorm6$10,000

NTOSpider4$10,000

Milescan4$495-$1,495

Grendel-Scan  3Free

In addition to these core results, the authors also drew the following conclusions:

There are whole classes of vulnerabilities that cannot be detected by the state-of-the-art scanners, including weak passwords, broken access controls and logic flaws.

The crawling of modern web applications can be a serious challenge for today’s web vulnerability scanners, due to incomplete support for common client-side technologies and the complex stateful nature of today's applications.

There is no strong correlation between price and capability, as some of the free or very cost-effective scanners performed as well as scanners that cost thousands of dollars.

I must say, I completely agree with these conclusions. Firstly, Burp Scanner was designed with a clear awareness of the kinds of issues that scanners can reliably look for. It seeks to automate everything that can be reliably automated, giving you confidence in its output, and leaving you to focus on the aspects of the job that require human experience and intelligence to deliver. Secondly, devising a fully automated crawler that provides comprehensive coverage of today's applications, with their widely varied technologies and stateful designs, is a Herculean task. Even the best crawlers fall very far short of this, and claiming otherwise only gives false reassurance that this key part of application testing can be left to a machine. Burp Spider does provide crawling capabilities, both active and passive, but this feature is designed to be used in tandem with manual application mapping, and human sense-checking of the coverage achieved and the requests that need to be scanned for vulnerabilities.

I was, of course, pleased to see this recognition of Burp Scanner's capabilities, and the above comparison of scanners' performance versus price should make interesting reading for anyone who is deciding which products to spend their money on. Rest assured, I'll be going through the raw results from this survey in detail, and looking at ways to make Burp even more effective.

burp

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
