# Sessions settings

Source: https://portswigger.net/burp/documentation/desktop/settings/sessions
Fetched: 2026-06-28T09:15:55.805316+00:00

Support Center

Documentation

Desktop editions

Settings

Sessions

ProfessionalCommunity Edition

Sessions settings

Last updated:

June 18, 2026

Read time:

6 Minutes

The Sessions settings enable you to configure Burp Suite's session handling functionality. You can configure the following:

Session handling rules.

Cookie jar.

Macros.

Session handling overview

When testing web applications, you may encounter challenges relating to session handling and application state. For example:

The application may terminate the testing session, either defensively or for other reasons. The sessions must be restored before you can send subsequent requests.

Some functions may require changeable tokens within each request in order to hinder request forgery attacks.

Some functions may require you to make a series of secondary requests in order to get the application into a suitable state to accept the request that you need to test.

Burp's session handling functionality enables you to configure the system to handle session-related challenges in the background, helping you to continue your testing uninterrupted.

Session handling rules

Burp's session handling rules give you fine-grained control over how Burp deals with a target's session handling mechanism and related functionality.

Each rule has two parts:

A scope denoting the tools, URLs and parameters that the rule applies to.

The actions that are performed when the rule is applied to a request.

Every time Burp makes an outgoing request, it determines which of the defined rules should apply to the request and then performs all of the relevant actions in order.

Note

Burp Scanner automatically handles sessions during crawling and crawl-driven auditing. Burp does not apply session handling rules to requests made by these scans, except for rules that only contain Set a specific cookie or parameter value and / or Invoke a Burp extension actions.

By creating multiple rules, you can define a hierarchy of behavior that Burp applies to different applications and functions.

For example, you could define the following rules for a particular test:

For all requests, add cookies from Burp's cookie jar.

For requests to a specific domain, validate that the current session with that application is still active. If the session is not active, run a macro to log back in to the application, and update the cookie jar with the resulting session token.

For requests to a specific URL containing the __csrftoken parameter, run a macro to obtain a valid __csrftoken value and use this value when making the request.

More information

For more details on configuring session handling rules, see the Session handling rule editor documentation.

Session handling tracer

The session handling tracer can help you when troubleshooting your session handling configuration. To view the tracer, click Open sessions tracer.

The tracer shows a listing of every request that has been handled by the session handling functionality (that is, those requests where at least one session rule has been applied). For each request handled, the tracer shows the sequence of rules and actions that were carried out. It also shows the changes made to the current request at each step in the sequence. This information can help you to see whether your current rule configuration is achieving the required results.

Note

The session handling tracer imposes a processing and storage overhead on all affected HTTP requests. We recommend that you only use the tracer when troubleshooting issues with session handling rules.

Session handling rules in Burp's tools

Burp's session handling rules interact with Burp's other functionality:

There is a default session handling rule that updates requests made by the Scanner with cookies from Burp's cookie jar. This rule does not apply when the Scanner is managing its own sessions during crawling and crawl-driven auditing. You can disable this rule if required.

If session handling rules modify a request before it is made (for example, to update a cookie or other parameter), Intruder and Repeater show the final, updated request. However, requests shown within reported Scanner issues are displayed as the original request. This enables you to compare the modified request with the base request. To view the final request for a scan issue, as modified by the session handler, send the request to Burp Repeater and issue it from there. Note that you must have the same session handling rules for both Repeater and Scanner in order for this process to work.

When the Scanner or Intruder makes a request that manipulates a cookie or parameter that is affected by a session handling action, the session handling action is not applied to that request. This avoids interference with the test that is being performed. For example, suppose you are using Intruder to fuzz all the parameters in a request, and you have configured a session handing rule to update the sessid cookie in that request. In this case, the sessid cookie is updated when Intruder is fuzzing other parameters. When Intruder is fuzzing the sessid cookie itself, the session handling rule does not update the cookie and Burp sends the Intruder payload string as the sessid value.

The Session handling rules settings are project settings. They apply to the current project only.

Cookie jar

Burp's cookie jar stores all of the cookies issued by websites you visit. The cookie jar is shared between all of Burp's tools.

Session handling rules and macros can use the cookie jar to automatically update outgoing requests with cookies.

By default, the cookie jar is updated based on traffic from the Proxy. However, you can configure the cookie jar to monitor any of the following tools to update cookies:

Proxy.

Intruder.

Scanner.

Sequencer.

Repeater.

Extensions.

In the case of the Proxy, Burp also inspects incoming requests from the browser. This is useful where an application has set a persistent cookie that is present in Burp's browser that is required to handle your session. Having Burp update its cookie jar based on requests through the Proxy means that all the necessary cookies are added to the cookie jar even if the application does not update the value of the cookie during your visit.

The cookie jar honors the domain and path scope of cookies.

Note

Crawls do not update the cookies stored in the cookie jar.

Managing the cookie jar

To manage the contents of the cookie jar, click Open cookie jar. You can edit cookies manually, remove cookies from the jar, or empty the jar altogether.

The Cookie jar settings are project settings. They apply to the current project only.

Macros

The Macros settings enable you to create and manage macros that Burp can use during testing.

A macro is a predefined sequence of one or more requests. You can use macros within session handling rules to perform various tasks, such as:

Fetching a page of the application (such as the user's home page) to check that the current session is still valid.

Performing a login to obtain a new valid session.

Obtaining a token or nonce to use as a parameter in another request.

When you scan or fuzz a request in a multi-step process, a macro can perform any requests necessary to get the application into a state where the targeted request is accepted.

In a multi-step process, a macro can complete the remaining steps of the process after the "attack" request. It can confirm the action was performed, or otherwise conclude the process.

As well as a sequence of requests, each macro specifies how cookies and parameters in the sequence should be handled, and any interdependencies between items.

You can add a new macro by clicking Add to display the Macro Editor dialog.

You can also edit your existing macros, or change their position in the list.

More information

For more details on recording macros, see the Macro Editor help.

The Macros settings are project settings. They apply to the current project only.
