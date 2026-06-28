# Burp v1.4 preview - Session handling: putting it all together

Source: https://portswigger.net/blog/burp-v1-4-preview-session-handling-putting-it-all-together
Fetched: 2026-06-28T09:15:11.835532+00:00

Burp v1.4 preview - Session handling: putting it all together

Dafydd Stuttard |

Friday, 25 March 2011 at 09:46 UTC

The functionality needed to let Burp automatically handle a wide variety of session handling challenges is necessarily complex, and often requires a lot of careful configuration. The best way to illustrate the power of the new features, and show how the configuration works in practice, is via an example.

Let's look at an application function which can only be accessed within an authenticated session, and employs a further token to defend against CSRF attacks. You want to test this function for various input-based vulnerabilities like XSS and SQL injection. Previously, performing automated (and some manual) testing of this function would have faced two challenges: (a) ensuring that the session being used remained valid; and (b) obtaining a valid token to use in each request. The new functionality can take care of both these challenges.

To do this, we're going to define some session handling rules. These rules will be applied to each request that is made to the function we are testing by the Intruder, Scanner and Repeater tools:

Check whether the current session is valid, by requesting the user's landing page in the application, and inspecting the response to confirm that the user is still logged in.

If the user is not logged in, log them back in to obtain a valid session.

Request the page containing the form whose submission we are going to test. This form contains the anti-CSRF token that we need, within a hidden field.

Update the request to the function we are testing with the value of the anti-CSRF token.

In most situations, we need to make use of Burp's own session handling cookie jar, so the first rule we define tells Burp to add cookies from the cookie jar to every request. This is, in fact, the default rule for the Scanner and Spider tools, so we'll just modify the default rule to apply to the Intruder and Repeater tools as well. This rule performs a single action, shown below:

The rule's scope is defined to include the relevant tools, and apply to all URLs:

Next, we need to check that the user's current session on the target application is valid. Assuming we want to apply this rule to all requests within the target application, we can define it to be in-scope for the whole of the application's domain:

We then add a suitable description and add an action of the type "check session is valid":

This opens the editor for this type of action, which contains a lot of configuration options:

The first set of options determines which request Burp uses to validate the current session. The options are:

Issue the actual request that is currently being processed. This option is ideal if the application always responds to out-of-session requests with a common response signature, such as a redirection to the login.

Run a macro, to make one or more other requests. This option is ideal if, to identify whether the session is valid, you need to request a standard item, such as the user's home page. It is also the best option if you need to apply further rules to modify the request currently being processed - for example (as in the present case) to update an anti-CSRF token in the request. If the option to run a macro is selected, you have a further option whether to do this every for every request, or only every N requests. If the application is aggressive in terminating sessions in response to unexpected input, it is recommended that you validate the session every time; otherwise, you can speed things up by only validating the session periodically.

For the current example, we are going to run a macro to fetch the user's landing page in the application, to check that their session is valid. To do this, we need to define our macro, by clicking on the "new" button in the previous screenshot. This opens the macro recorder, enabling us to select the request(s) that we wish to include in the macro. In the present case, we only need to select the GET request for the user's landing page:

The second set of options in the "check session is valid" action controls how Burp inspects the (final) response from the macro to determine whether the session is valid. Various options are available, and the configuration we need in the present case is shown below:

The final set of options for this action determines how Burp will behave depending on whether the current session is valid:

You can tell Burp not to perform any further actions for this request if the session is valid. Using this option lets you define subsequent, separate actions to recover a valid session. This option is mandatory if the request itself has already been issued in order to determine whether the session is valid.

You can tell Burp to perform a sub-action if the session is invalid, and then continue to process subsequent actions. This is useful when you need to define subsequent actions in any case, following the session validity check, for example to run a macro to obtain a request token or modify the application's state.

In the present example, we need to use the second option. If the session is invalid, we will run a macro to log the user back in. We need to record a further macro, to perform the actual login, and tell Burp to run this macro and update the session handling cookie jar based on the results:

At this point, we have configured Burp to update requests with cookies from its cookie jar, and to log the user back in to the target application when their session is invalid. To complete the required configuration, we need to define a further rule to deal with the anti-CSRF token used in the function we want to test. The request we are testing looks like this:

POST /auth/4/NewUserStep2.ashx HTTP/1.1

Content-Type: application/x-www-form-urlencoded

Host: mdsec.net

Content-Length: 137

Cookie: SessionId=39DD9F0CB979BFB431005524A4010244

realname=testuser&username=testuser&userrole=user&password=letmein1

To ensure that our requests to this function are properly handled, we need to ensure that a valid nonce is supplied with each request. The value of this nonce is supplied by the application in a hidden field within the form that generates the above request. So our rule needs to run a macro to fetch the page containing the form, and update the current request with the value of the nonce parameter. We add a further rule with an action of the type "run macro" and configure it as follows:

In the above configuration, we have specified that Burp should run a new macro, which fetches the form containing the anti-CSRF token, and then obtain the nonce parameter from the (final) macro response, and update this in the request. Alternatively, we could select the "update all parameters" option, and Burp would automatically attempt to match parameters in the request with those specified in the macro response.

In terms of the scope for this rule, this obviously needs to be defined more narrowly than the whole application domain. For example, we could define the rule to apply only to the exact URL in the above request. This is the best option if the application only employs anti-CSRF tokens in a few locations. However, in some applications, tokens are used for a large number of functions, and a token obtained within one function can be submitted within a different function. In this situation, we could define a rule that applies to the whole domain, but only to requests containing a specified parameter name. In this way, any time a request is made to the application that contains an anti-CSRF token, the rule will execute and Burp will fetch a new valid token to use in the request.

The full configuration, with its three session handling rules and three macros, looks like this within the main Burp UI:

You can test the configuration is working by logging out of the application, sending the authenticated, token-protected request to Burp Repeater, and verifying that it performs the required action. The request will probably take longer to return than normal, because behind the scenes Burp is making several other requests, to validate your session, log in again if necessary, and obtain a token to use in the request. Once you are happy that all of this is working correctly, you can send the request to Burp Intruder or Scanner, to perform your automated testing in the normal way.

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
