# Comparing web application scanners

Source: https://portswigger.net/blog/comparing-web-application-scanners
Fetched: 2026-06-28T09:15:13.602964+00:00

Comparing web application scanners

Dafydd Stuttard |

Tuesday, 22 June 2010 at 14:37 UTC

burp

scanners

Earlier this year, Larry Suto published a paper comparing web application vulnerability scanners. It contained plenty that was worthy of discussion, but I was particularly interested in what he said about Burp Scanner. Rather belatedly (I've been busy), here are my thoughts about this.

Larry ran each scanner against various test applications developed by other scan vendors for the purpose of showcasing their products. He ran each scanner in "point and shoot" mode (where it is given just the URL for the application) and also in "trained" mode (where it is manually shown which pages it is supposed to test). Larry then added up all of the vulnerabilities found by each scanner against all of the test applications.

Now, in contrast to the other scanners, Burp is not designed to be a "point and shoot" tool, where the user provides a URL and hits "go". Rather, it is designed to support hands-on penetration testing. What Larry calls "training" for the other scanners is the primary modus operandi for Burp. Therefore, I wasn't much interested in the "point and shoot" numbers for Burp, as they aren't applicable to its intended use.

After Larry had "trained" each scanner in the test applications, he reported the following numbers of vulnerabilities found by each scanner:

NTOSpider145

Hailstorm96

Appscan85

Acunetix73

Burp56

WebInspect 52

Qualys44

When I first saw these numbers, I was surprised that Burp came significantly behind some other products. Based on my own comparisons with these scanners, and on very widespread feedback from users, this did not ring true. My immediate thought was that Burp had not been "trained" properly on the test applications. Burp provides the user with very fine-grained control over what gets scanned. To ensure complete coverage of an application, you need to ensure that Burp scans every request - that is, every page, every form submission, every asynchronous client request, etc. I suspected that Larry had not made Burp scan all of the relevant application requests, and so had missed a lot of bugs.

I spent just a couple of hours running Burp against the test applications used in the survey, and got very different results. Simply by ensuring that Burp was actually scanning every relevant request, and doing nothing else to optimise its performance, I found that Burp performed significantly better:

NTOSpider145

Hailstorm96

Burp95

Appscan85

Acunetix73

WebInspect 52

Qualys44

This was a relief, and closer to my expectations of Burp's capabilities. Still, the most striking feature of the above numbers is the fact that NTOSpider appears to be ahead by a mile. This surprised many people, and led some to suggest that cheating or collusion had occurred. I doubt this - the reality is more mundane. When we drill down into Larry's raw data of the vulnerabilities found by each scanner, we find a few cases where NTO alone identifies XSS or SQL injection in a request containing a large number of parameters, and each parameter is counted as a separate vulnerability in the raw numbers. This might be reasonable if each parameter represented a different flavour of the vulnerability type, designed to establish scanners' ability to find different varieties of bugs. But this was not the case: each parameter manifested identical behaviour in these cases.

In some cases, NTO deserves credit for reporting issues where other scanners did not (for example, in a user registration page which required a different username in each request in order to uncover bugs in other parameters). Nevertheless, crudely summing the raw numbers in these cases has skewed the results quite misleadingly. If these duplicated issues with multiple parameters are consolidated, NTO's numbers come down into line with the other leading products.

I know that other scan vendors have also responded to Larry, and in some cases attacked his methodology or claimed unfair treatment. I think that Larry has had a decent stab at an inherently difficult task, and I don't think he deserves to be flamed about it. There is plenty of interesting and subtle analysis behind the headline numbers in his paper. But I do contend that the raw numbers are misleading and certainly don't reflect Burp Scanner's true capabilities.

I do actually have reason to thank Larry for what he has done. In the course of reperforming his analysis of Burp, I did identify a few cases where Burp was missing a trick, and have recently made some enhancements to the core scanning engine to rectify these (coming in release v1.3.06). After these revisions, Burp now correctly reports an additional 16 vulnerabilities within the test applications, which is good news for users of Burp.

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
