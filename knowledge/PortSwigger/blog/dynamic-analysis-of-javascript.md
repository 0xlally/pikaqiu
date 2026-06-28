# Dynamic analysis of JavaScript

Source: https://portswigger.net/blog/dynamic-analysis-of-javascript
Fetched: 2026-06-28T09:15:14.122170+00:00

Dynamic analysis of JavaScript

Dafydd Stuttard |

Monday, 13 August 2018 at 15:47 UTC

MoBP

Burp Suite

Burp's current Scanner can report a wide range of DOM-based vulnerabilities using static analysis techniques.

Static analysis of JavaScript involves parsing the code to construct an abstract syntax tree, identifying the tainted sources and dangerous sinks, and locating possible data flows through the code to identify paths via which malicious data could be propagated from a source to a sink.

Burp's new Scanner is getting a fantastic new capability. It will perform dynamic analysis of JavaScript to reliably discover DOM-based vulnerabilities.

Static and dynamic approaches to security testing have different inherent strengths and weaknesses:

Static analysis (SAST) is able to find some vulnerabilities that dynamic analysis misses, because it can identify code paths that could possibly be executed in the right circumstances, but which don't in fact get executed by the dynamic analysis. However, static analysis is inherently prone to false positives and noise, because it sees some code paths as possibly executable when in fact they are not, and because it fails to understand custom data validation logic that means taint paths from sources to sinks are not in fact exploitable.

Dynamic analysis (DAST) has the opposite characteristics. It is much less prone to false positives because if it actually observes suitable data being propagated from source to sink during execution, then this is concrete evidence for a vulnerability. However, it can suffer from false negatives in situations where the tainted data that it injects doesn't reach a sink due to the current state of the application or the values of other data, both of which an attacker might in fact be able to control.

Burp's new dynamic analysis of JavaScript uses an embedded headless browser. It loads HTTP responses into the browser, injects payloads into the DOM at locations that are potentially controllable by an attacker, and executes the JavaScript within the response. It also interacts with the page by creating mouse events to achieve as much code coverage as possible. It monitors dangerous sinks that could be used to perform an attack, to identify any injected payloads that reach those sinks.

The new JavaScript analysis has been in development for many months, during which time we have tested it against numerous bug bounty sites, and found a ton of exploitable vulnerabilities that couldn't be found by any existing tools. So we know just how well it works:

But it gets even better. The new Scanner still performs its old-style static analysis, and harnesses the joint benefits of both approaches. It correlates the results of the two techniques, and where available presents both types of evidence together. These issues may be regarded as rock-solid findings, and are reported as certain. In cases where only static analysis can detect a potential issue, Burp downgrades the confidence with which the issue is reported. This integrated approach to JavaScript analysis greatly assists a tester who is reviewing results to find the most important issues.

MoBP

Burp Suite

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
