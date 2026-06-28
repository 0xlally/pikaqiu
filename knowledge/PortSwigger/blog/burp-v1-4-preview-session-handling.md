# Burp v1.4 preview - Session handling

Source: https://portswigger.net/blog/burp-v1-4-preview-session-handling
Fetched: 2026-06-28T09:15:11.780505+00:00

Burp v1.4 preview - Session handling

Dafydd Stuttard |

Wednesday, 23 March 2011 at 17:02 UTC

Some problems commonly encountered when performing any kind of fuzzing or scanning of web applications are:

The application terminates the session being used for testing, either defensively or for other reasons, and the remainder of the testing exercise is ineffective.

Some functions use changing tokens that must be supplied with each request (for example, to prevent request forgery attacks).

Some functions require a series of other requests to be made before the request being tested, to get the application into a suitable state for it to accept the request being tested.

All of these problems can also arise when you are testing manually, and resolving them manually is often tedious, reducing your appetite for further testing.

The second broad area of new functionality in Burp v1.4 is a range of features to help in all of these situations, letting you continue your manual and automated testing while Burp takes care of the problems for you in the background. This functionality is quite complex, with a lot of configuration to explain. We'll start by looking at the core session handling features.

Firstly, Burp's cookie jar, which was previously part of the Spider tool, is now more sophisticated and is shared between all tools. Cookies set in responses are stored in the cookie jar, and can be automatically added to outgoing requests. All of this is configurable so, for example, you can update the cookie jar for cookies received by the Proxy and Spider, and have Burp automatically add cookies to requests sent by the Scanner and Repeater. The cookie jar configuration is shown in the new "sessions" tab within the main "options" tab:

As shown, by default the cookie jar is updated based on traffic from the Proxy and Spider tools. You can view the contents of the cookie jar and edit cookies manually if you wish:

For all tools other than the Proxy, HTTP responses are examined to identify new cookies. In the case of the Proxy, incoming requests from the browser are also inspected. This is useful where an application has previously set a persistent cookie which is present in your browser, and which is required for proper handling of your session. Having Burp update its cookie jar based on requests through the Proxy means that all the necessary cookies will be added to the cookie jar even if the application does not update the value of this cookie during your current visit.

Burp's cookie jar honours the domain scope of cookies, in a way that mimics Internet Explorer's interpretation of cookie handling specifications. Path scope is not honoured.

In addition to the basic cookie jar, Burp also lets you define a list of session handling rules, which give you very fine-grained control over how Burp deals with an application's session handling mechanism and related functionality. These rules are configured in the new "sessions" tab:

Each rule comprises a scope (what the rule applies to) and actions (what the rule does). For every outgoing request that Burp makes, it determines which of the defined rules are in-scope for the request, and performs all of those rules' actions in order (unless a condition-checking action determines that no further actions should be applied to the request).

The scope for each rule can be defined based on any or all of the following features of the request being processed:

The Burp tool that is making the request.

The URL of the request.

The names of parameters within the request.

Each rule can perform one or more actions. The following actions are currently implemented:

Add cookies from the session handling cookie jar.

Set a specific cookie or parameter value.

Check whether the current session is valid, and perform sub-actions conditionally on the result.

Run a macro.

Prompt the user for in-browser session recovery.

All of these actions are highly configurable, and can be combined in arbitrary ways to handle virtually any session handling mechanism. Being able to run arbitrary macros (defined request sequences), and update specified cookie and parameter values based on the result, allows you to automatically log back in to an application part way through an automated scan or Intruder attack. Being able to prompt for in-browser session recovery enables you to work with login mechanisms that involve keying a number from a physical token, or solving a CAPTCHA-style puzzle.

By creating multiple rules with different scopes and actions, you can define a hierarchy of behaviour that Burp will apply to different applications and functions. For example, on a particular test you could define the following rules:

For all requests, add cookies from Burp's cookie jar.

For requests to a specific domain, validate that the current session with that application is still active, and if not, run a macro to log back in to the application, and update the cookie jar with the resulting session token.

For requests to a specific URL containing the __csrftoken parameter, first run a macro to obtain a valid __csrftoken value, and use this when making the request.

We'll be examining some more details of how this functionality works shortly. In the meantime, it is worth noting a few points about how the new session handling features affect some of Burp's existing functionality:

There is a default session handling rule which updates all requests made by the Scanner and Spider with cookies from Burp's cookie jar. This changes the session handling of requests made by the Scanner. Previously, these requests were always made within the same session as the relevant base request - in other words, cookies appearing in the request that was sent to be scanned were used for all scan requests for that item. Now, different cookies may be used if Burp's cookie jar has been updated since the request was sent to be scanned. This change is normally desirable, as it ensures that all scan requests are made in-session, provided you maintain a valid session using your browser. It also means that items in the active scan queue that are loaded from a state file will be scanned within your current session, not the session that was active when the state file was saved. If this is not the behaviour you require, you should disable the default session handling rule before performing any scanning.

In previous versions of Burp, the Spider configuration included some basic settings for using cookies from the cookie jar. These settings have now been removed, and the Suite-wide session handling functionality should be used instead. The previously default behaviour for the Spider's handling of cookies is replicated by the new default session handling rule, as described above.

Similarly, Intruder previously included an option to run a specified request before each attack request, to obtain a new cookie to use in the attack request. This option has now been removed, and instead you should define a session handling rule to run a macro before each request (or, more likely, use some more elegant configuration to achieve the same objective).

In cases where session handling rules modify a request before it is made (for example, to update a cookie or other parameter), some of Burp's tools will show the final, updated request, for purposes of clarity. This applies to the Intruder, Repeater and Spider tools. Requests that are shown within reported Scanner issues continue to show the original request, to facilitate clear comparison with the base request, where necessary. To observe the final request for a scan issue, as modified by the session handler, you can send the request to Burp Repeater and issue it there.

When the Scanner or Intruder makes a request that manipulates a cookie or parameter that is affected by a session handling action, the action is not applied to that request, to avoid interfering with the test that is being performed. For example, if you are using Intruder to fuzz all the parameters in a request, and you have configured a session handing rule to update the "sessid" cookie in that request, then the "sessid" cookie will be updated when Intruder is fuzzing other parameters. When Intruder is fuzzing the "sessid" cookie itself, Burp will send the Intruder payload string as the "sessid" value, and will not update it as is done normally.

As I said, the new session handling is powerful and complex. In the next couple of posts, we'll look at how it works in more detail.

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
