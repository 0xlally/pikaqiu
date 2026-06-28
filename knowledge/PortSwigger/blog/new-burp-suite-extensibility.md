# New Burp Suite Extensibility

Source: https://portswigger.net/blog/new-burp-suite-extensibility
Fetched: 2026-06-28T09:15:21.631930+00:00

New Burp Suite Extensibility

Dafydd Stuttard |

Monday, 10 December 2012 at 11:30 UTC

burp extender

burp

We will shortly be releasing Burp Suite Pro v1.5.01, which contains a new framework for extensibility in Burp.

A Short History

Burp has supported extensions for years. Burp's extensibility began its live very simple, and has evolved gradually without any overall plan.

The existing API is fairly limited, and its main uses have been for:

Changing HTTP messages on the fly

Initiating some testing tasks (e.g. to automate crawling / scanning)

The existing framework has been used to good effect to extend Burp's capabilities, for example:

WCF Binary Soap plugin, by GDS

Deflate plugin, by GDS

DSer plugin for JAVA serialized objects, by Attack & Defense Labs

w3af plugin, by David Robert

Current Limitations

The existing extensibility framework contains some significant limitations:

You can only run one extension at a time.

You can only load an extension at launch time, by modifying Burp's classpath.

Only the Java language is natively supported.

The processing of writing, compiling and loading an extension can be challenging for non-programmers.

The API doesn't expose very much in many areas that would be extremely useful to be able to extend. For example: Burp's user interface, the Scanner, Intruder and session handling.

Extensions are effectively bolt-ons, not properly integrated with Burp's internals.

In an attempt to address these limitations, several people have developed extensibility frameworks layered over Burp's, including:

Buby (Ruby)

Burp Suite Extended (Python)

Hiccup (Python)

Resty-Burp (REST / JSON)

These third-party frameworks are well designed, and address some of Burp's shortcomings. Nevertheless, it is cumbersome to need to install an additional framework, and the limitations in the current API still remain.

The efforts that people were evidently going to, in an attempt to improve on what Burp itself offered, made me realize: it's time to fix Burp natively.

Objectives for New Extensibility

The overall objectives for the new extensibility framework are:

Allow multiple extensions to run simultanously.

Support dynamic loading and unloading of extensions at runtime.

Support languages other than Java. In the initial release, Python is supported via the Jython interpreter.

Provide a much, much richer API that allows extensions to really integrate with Burp's internals.

Use a more future-proof API design, to allow easier enhancements in future.

As far as possible, ensure backwards compatibility with legacy extensions.

A key aspiration for the new extensibility is that people should find it quick and easy to create extensions mid-testing to work around all kinds of obstacles that can arise. For example, tasks like writing a Scanner check, creating a session handling action, or adding a new HTTP message analyzer to Burp's editor, should all be achievable in less time than it takes to work around an obstacle manually. With the new support for Python scripting, and a much more helpful API, even users without much programming experience will hopefully feel tempted to have a go, and so dramatically enhance the power of their testing with Burp.

burp extender

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
