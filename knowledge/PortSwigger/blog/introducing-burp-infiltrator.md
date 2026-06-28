# Introducing Burp Infiltrator

Source: https://portswigger.net/blog/introducing-burp-infiltrator
Fetched: 2026-06-28T09:15:17.702628+00:00

Introducing Burp Infiltrator

Dafydd Stuttard |

Tuesday, 26 July 2016 at 15:52 UTC

The latest release of Burp Suite introduces a new tool, called Burp Infiltrator.

Burp Infiltrator is a tool for instrumenting target web applications in order to facilitate testing using Burp Scanner. Burp Infiltrator modifies the target application so that Burp can detect cases where its input is passed to potentially unsafe APIs on the server side. In industry jargon, this capability is known as IAST (interactive application security testing).

Burp Infiltrator currently supports applications written in Java or other JVM-based languages such as Groovy. Java versions from 4 and upwards are supported. In future, Burp Infiltrator will support other platforms such as .NET.

How Burp Infiltrator works

The Burp user exports the Burp Infiltrator installer from Burp, via the "Burp" menu.

The application developer or administrator installs Burp Infiltrator by running it on the machine containing the application bytecode.

Burp Infiltrator patches the application bytecode to inject instrumentation hooks at locations where potentially unsafe APIs are called.

The application is launched in the normal way, running the patched bytecode.

The Burp user performs a scan of the application in the normal way.

When the application calls a potentially unsafe API, the instrumentation hook inspects the relevant parameters to the API. Any Burp payloads containing Burp Collaborator domains are fingerprinted based on their unique structure.

The instrumentation hook mutates the detected Burp Collaborator domain to incorporate an identifier of the API that was called.

The instrumentation hook performs a DNS lookup of the mutated Burp Collaborator domain.

Optionally, based on configuration options, the instrumentation hook makes an HTTP/S request to the mutated Burp Collaborator domain, including the full value of the relevant parameter and the application call stack.

Burp polls the Collaborator server in the normal way to retrieve details of any Collaborator interactions that have occurred as a result of its scan payloads. Details of any interactions that have been performed by the Burp Infiltrator instrumentation are returned to Burp.

Burp reports to the user that the relevant item of input is being passed by the application to a potentially unsafe API, and generates an informational scan issue of the relevant vulnerability type. If other evidence was found for the same issue (based on in-band behavior or other Collaborator interactions) then this evidence is aggregated into a single issue.

Issues reported by Burp Infiltrator

Burp Infiltrator allows Burp Scanner to report usage of potentially dangerous server-side APIs that may constitute a security vulnerability. It also allows Burp to correlate the external entry point for a vulnerability (for example a particular URL and parameter) with the back-end code where the vulnerability occurs.

In the following example, Burp Scanner has identified an XML injection vulnerability based on Burp's existing scanning techniques, and also reports the unsafe API call that leads to the vulnerability within the server-side application:

Burp Infiltrator enables Burp to report:

The potentially unsafe API that was called.

The full value of the relevant parameter to that API.

The application call stack when the API was invoked.

This information can be hugely beneficial for numerous purposes:

It provides additional evidence to corroborate a putative vulnerability reported using conventional dynamic scanning techniques.

It allows developers to see exactly where in their code a vulnerability occurs, including the names of code files and line numbers.

It allows security testers to see exactly what data is passed to a potentially unsafe API as a result of submitted input, facilitating manual exploitation of many vulnerabilities, such as SQL injection into complex nested queries.

Important considerations

Please take careful note of the following points before using Burp Infiltrator:

You should read all of the documentation about Burp Infiltrator before using it or inducing anyone else to use it. You should only use Burp Infiltrator in full understanding of its nature and the risks inherent in its utilization.

You can use a private Burp Collaborator server with Burp Infiltrator, provided the Collaborator server is configured using a domain name, not via an IP address.

You can install Burp Infiltrator within a target application non-interactively, for use in CI pipelines and other automated use cases.

During installation of Burp Infiltrator, you can configure whether full parameter values and call stacks should be reported, and various other configuration options.

For more details, including step-by-step instructions, please refer to the Burp Infiltrator documentation.

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
