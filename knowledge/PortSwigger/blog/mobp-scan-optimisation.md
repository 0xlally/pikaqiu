# [MoBP] Scan optimisation

Source: https://portswigger.net/blog/mobp-scan-optimisation
Fetched: 2026-06-28T09:15:20.816517+00:00

[MoBP] Scan optimisation

Dafydd Stuttard |

Saturday, 22 November 2008 at 08:37 UTC

MoBP

burp

I guess some people are getting bored of hearing about how Burp Scanner is going to solve all of the world's ills, so this will be the last post on the subject. There are still a few other rabbits to pull out of the hat during the rest of the month.

One of my complaints about existing scanners was that they give you limited feedback or control over what is happening during scans. Burp tries to address this problem in a few ways.

First, take another look at the active scan queue:

For each request that is being scanned, you can monitor the progress of that individual request. The table shows you the number of "insertion points" where Burp is placing payloads, and the number of attack requests that have been generated. The latter is not a linear function of the former - observed application behaviour feeds back into subsequent attack requests, just as it would for a human tester.

This information lets you quickly see whether any of your scans are progressing too slowly, and understand the reasons why. Given this information, you can then take action to optimise your scans. Within the scan queue, there is a context menu which lets you cancel or re-prioritise individual items. You can also tweak the scanner configuration based on what you have learnt about the application.

A key factor in the speed and effectiveness of scans is the selection of attack insertion points. Burp gives you fine-grained control over the locations within the base request where attack payloads will be placed. You can tell Burp to skip time-consuming server-side injection tests for specific parameters which you believe are not vulnerable (client-side tests like XSS are always performed because they impose minimal overhead for non-vulnerable parameters). You can also tell Burp to intelligently select attacks based on the base values of parameters - for example, if a parameter's value contains characters that don't normally appear in filenames, Burp will skip file path traversal checks. The UI for all of this configuration looks like this:

The rest of the Scanner configuration lets you fine-tune other aspects of attacks. You can configure the size of the scanning thread pool, and the way Burp should handle dropped connections. You can also turn on or off each individual category of check. So if you know that an application does not use any LDAP, you can turn off LDAP injection tests. Or you can configure Burp to do a quick once-over of an application, checking only for XSS and SQL injection in URL and body parameters, before returning later to carry out more comprehensive testing. The key point is that you can see everything that the Scanner is doing, and control exactly how its actions should be applied to different areas of the application.

MoBP

burp

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
