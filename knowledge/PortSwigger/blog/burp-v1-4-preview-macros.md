# Burp v1.4 preview - Macros

Source: https://portswigger.net/blog/burp-v1-4-preview-macros
Fetched: 2026-06-28T09:15:11.994791+00:00

Burp v1.4 preview - Macros

Dafydd Stuttard |

Thursday, 24 March 2011 at 14:44 UTC

burp

A key part of Burp's new session handling functionality is the ability to run macros, as defined in session handling rules. A macro is a predefined sequence of one or more requests. Typical use cases for macros include:

Fetching a page of the application (such as the user's home page) to check that the current session is still valid.

Performing a login to obtain a new valid session.

Obtaining a token or nonce to use as a parameter in another request.

When scanning or fuzzing a request in a multi-step process, performing the necessary preceding requests, to get the application into a state where the targeted request will be accepted.

Macros are recorded using your browser. When defining a macro, Burp displays a view of the Proxy history, from which you can select the requests to be used for the macro. You can select from previously made requests, or record the macro afresh and select the new items from the history.

When you have recorded the macro, the macro editor shows the details of the items in the macro, which you can review and configure as required:

As well as the basic sequence of requests, each macro includes some important configuration about how items in the sequence should be handled, and any interdependencies between items:

For each item in the macro, the following settings can be configured:

Whether cookies from the session handling cookie jar should be added to the request.

Whether cookies received in the response should be added to the session handling cookie jar.

For each parameter in the request, whether it should use a preset value, or a value derived from a previous response in the macro.

The ability to derive a parameter's value from a previous response in the macro is particularly useful in some multi-stage processes, and in situations where applications make aggressive use of anti-CSRF tokens. When a new macro is defined, Burp tries to automatically find any relationships of this kind, by identifying parameters whose values can be determined from the preceding response (form field values, redirection targets, query strings in links, etc.). You can easily review and edit the default macro configuration applied by Burp before the macro is used. Further, the configured macro can be tested in isolation, and the full request/response sequence reviewed, to check that it is functioning in the way you require.

Of course, the full power of using macros is only realised once they are incorporated into suitable session handling rules, to control the way that different requests are processed by Burp's tools, and work with the session handling mechanism and related functionality being used by the target application. As is perhaps already apparent, the configuration required in many real-world situations is complex, and mistakes are easily made. There is a need for a full in-tool debugger for troubleshooting the session handling configuration. In the meantime, an effective workaround is to chain a second instance of Burp as an upstream proxy from the instance being configured. The proxy history in the upstream instance will show you the full sequence of requests and responses that occur when your session handling rules are executed, helping you to find and fix any problems in your configuration.

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
