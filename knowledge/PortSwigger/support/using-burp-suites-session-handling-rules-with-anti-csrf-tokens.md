# Using Burp's Session Handling Rules with anti-CSRF Tokens

Source: https://portswigger.net/support/using-burp-suites-session-handling-rules-with-anti-csrf-tokens
Fetched: 2026-06-28T09:17:35.333062+00:00

This page may be out of date

We haven't updated it for a while because we're busy working on new, improved content to help you get the

most out of Burp Suite. In the meantime, please note that the information on this page may no longer be

accurate.

Visit our Support Center

Using Burp's Session Handling Rules with anti-CSRF Tokens

Anti-CSRF tokens are randomly generated "challenge" tokens that are associated with the user’s current session. They are inserted within HTML forms and links associated with sensitive server-side operations. When users perform the sensitive operation (e.g. a banking transfer) the anti-CSRF token should be included in the request. The server should then verify the existence and authenticity of this token before processing the request. If the token is missing or incorrect, the request is rejected.

Using Burp Suite against a target application that has developed a strong defence against CSRF attacks can be cause issues, due to the fact that the application should not allow a request to be repeated without updating the anti-CSRF token.

In this article we demonstrate how to use Burp's session handling rules and a macro to automatically retrieve a response, extract the anti-CSRF token, and insert the token within the appropriate request.

This tutorial uses the login function from the "

DVWA".

Identifying the Token

The first step is to identify the anti-CSRF token.

In this example, when we submit our credentials to the application during the login process, the request includes a user_token. This token is the anti-CSRF token.

If the value of this token does not match the value expected by the web server then this request will be deemed invalid.

The token is sent to the browser in the previous server response.

In this example as a hidden fieldset in a web form.

Creating a Macro

A macro is a predefined sequence of one or more requests. You can use macros within session handling rules to perform various tasks.

We can use a macro to fetch the token.

Go to Project options > Sessions > Add to record a new macro.

The Burp Macro Recorder and Macro Editor windows will pop up.

In our example we want the macro to fetch the token from the response of the initial GET request.

We select the appropriate item from the proxy history and click "OK".

In the Macro Editor we can change the description, configure, re-record, re-analyze or test the macro.

Configuring The Session Handling Rule

Burp lets you define a list of session handling rules, giving you very fine-grained control over how Burp deals with an application's session handling mechanism and related functionality.

Go to Project options > Sessions > Session Handling Rules > Add to create a new rule.

Add an appropriate rule description.

Then click the ‘Add’ button, under the ‘Rule Actions’ section.

Click the ‘Run a macro’ in the drop-down menu.

In the Session handling action editor pop-up window, select the macro you want to run.

Click the ‘Scope’ tab.

Select the tools you want the rule to be applied to.

Testing The Rule

We can use Burp Intruder to test our configuration.

Intruder allows us to evaluate each request to determine if the POST parameter that possesses the anti-CSRF token is being updated.

The anti-CSRF token parameter should be updated within each request.
