# Burp gets new JavaScript analysis capabilities

Source: https://portswigger.net/blog/burp-gets-new-javascript-analysis-capabilities
Fetched: 2026-06-28T09:15:08.552000+00:00

Burp gets new JavaScript analysis capabilities

Dafydd Stuttard |

Monday, 28 July 2014 at 15:43 UTC

The latest release of Burp includes a new engine for static analysis of JavaScript code. This enables Burp Scanner to report a range of new vulnerabilities, including:

DOM-based XSS

JavaScript injection

Client-side SQL injection

WebSocket hijacking

Local file path manipulation

DOM-based open redirection

Cookie manipulation

Ajax request header manipulation

DOM-based denial of service

Web message manipulation

HTML5 storage manipulation

In the initial release, the new functionality is officially experimental, and will be enhanced in future releases based on user feedback. The key areas for further enhancement are as follows:

Burp supports most core JavaScript language features, including local and global variables, function calls and return values, assignments, arrays, and relevant platform APIs. Two important language features are not supported: object dereferences and function pointer variables. Some vulnerabilities that are dependent on these language features are not currently reported.

Static code analysis is resource intensive. We have worked hard on the code analysis engine to minimize memory and CPU consumption, and its performance has been extensively tested against real-world code. However, there is more work yet to do in this area, and in the initial release it may be necessary to (a) increase the memory that is assigned to the Java process; (b) restrict static code analysis to key targets of interest; (c) configure a suitable maximum analysis time for complex items. See the static code analysis options for more details.

In a future release, we may provide a UI similar to the active scan queue, containing a view of pending and current code analysis tasks, and enabling the user to pause, resume or cancel individual tasks.

Some further refinement may be necessary of Burp's rules for identifying tainted sources and dangerous sinks, and mapping these to vulnerability types.

Despite the above opportunities for enhancement, the current functionality is sufficiently powerful that it would be wrong for us to sit on it any longer, and it's time for users to try it out in real-world situations. Feedback is actively welcomed about the new capabilities, to help drive the above and other improvements.

How does Burp's code analysis work? We don't simply match suspicious code based on patterns, which is too error-prone and only finds the simplest bugs. We don't execute the code, or fuzz the DOM in an instrumented browser, as this can lead to worse performance problems, many missed vulnerabilities, and poor code coverage due to missed execution branches. We don't employ any external dependencies as these can be brittle and a pain for users to set up.

Rather, Burp contains a home-grown language parser and dataflow analysis engine. We identify places in the code where data is read from potentially tainted sources within the DOM, and trace this data through possible execution paths in the code. If the data can reach a dangerous sink, then a potential vulnerability is reported. This is not, of course, a new approach to static code analysis, but there are many challenges in the details that we believe we have solved in novel and effective ways.

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
