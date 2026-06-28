# Session handling rule editor

Source: https://portswigger.net/burp/documentation/desktop/settings/sessions/session-handling-rules
Fetched: 2026-06-28T09:15:55.742495+00:00

Support Center

Documentation

Desktop editions

Settings

Sessions

Session handling rule editor

ProfessionalCommunity Edition

Session handling rule editor

Last updated:

June 18, 2026

Read time:

7 Minutes

The session handling rule editor enables you to configure the session handling rules that Burp uses. To open the rule editor, select Settings > Sessions > Session handling rules and then either select Add to add a new rule, or Edit to edit an existing one.

The session handling rule editor has two tabs:

Details enables you to specify the actions that the rule performs when it is applied to a request.

Scope enables you to specify the tools, URLs and parameters that the rule applies to.

Rule description

Access the Rule Description setting from the Details tab. This setting enables you to describe what the rule does. The description you provide appears on the rule editor's list of active rules.

Rule actions

Access the Rule Actions setting from the Details tab. This setting enables you to configure the actions that the rule performs.

Each rule includes one or more actions that should be carried out when the rule is applied. Burp performs these actions in sequence, unless one of the actions specifies that no further actions should be applied to the request.

Click Add to add the following actions to your rules:

Add cookies from the session handling cookie jar.

Set a specific cookie or parameter value.

Check whether the current session is valid, and perform sub-actions conditionally on the result.

Prompt the user for in-browser session recovery.

Run a macro.

Run a post-request macro - this issues the current request, and then executes a further macro.

Invoke a Burp extension.

Set a specific header value.

Replace matching part of the request

You can combine any of these actions to handle virtually any session handling mechanism. For example, you could configure a rule to run a macro and update specified cookie and parameter values based on the result. You could use this to automatically log back in to an application part way through an automated scan or Intruder attack.

Use cookies from the session handling cookie jar

This action updates the request with cookies from Burp's cookie jar. You can configure the action to update all cookies (optionally, with specific exclusions), or to only update certain specific cookies.

More information

For more information on how Burp's cookie jar works, see Sessions.

Set a specific cookie or parameter value

This action sets a specific value in a named parameter or cookie of the request. If the named parameter or cookie is not already present in the request, you can specify whether it should be added as:

A URL parameter.

A body parameter.

A cookie.

Check session is valid

This action checks whether the current session is valid. If it is not, you can choose to perform a further action to obtain a new valid session.

Make requests to validate session

Burp issues one or more requests to determine the validity of the current session. When running this action, Burp can:

Issue the current request that is being processed by the rule.

Run a macro.

If Burp issues the current request and the rule determines that the session is valid, then the system cannot perform any further actions on the current request.

Optionally, you can configure Burp to validate the session after a set number of requests. This helps you to avoid making unnecessary requests in cases where the application rarely invalidates your session.

Inspect responses to determine session validity

Having made the configured requests, Burp examines the response to determine whether the session is valid. If Burp ran a macro, it examines the response from the final request made by the macro.

To determine whether the session is valid, Burp checks whether or not the response contains a specified expression. You can configure Burp to search for:

HTTP response headers.

Response body.

The URL of any redirection target.

You can search for a literal string or a regular expression. You can make the search case sensitive.

Define behavior dependent on session validity

This setting enables you to configure how Burp behaves once the validity check is complete.

If the session is valid, you can select whether Burp should process any further rules or actions for the current request.

If the session is invalid, you can configure Burp to perform one of the following actions in order to obtain a new valid session:

Run a macro.

Prompt for in-browser session recovery.

Run a macro to obtain a new valid session

If you select Run a macro, then Burp runs one or more macros to attempt to obtain a new valid session. You can specify the macros to run from the Select macro menu.

More information

For information on recording and editing macros, see Macro editor.

Once the macro has run, you can select whether Burp should update the current request with parameters matched from the final macro response. You can also select whether Burp should update the current request with cookies from the session handling cookie jar. Burp can either update the request using specific parameters and cookies, or update using all parameters and cookies except those specified.

Tolerate URL mismatch when matching parameters

If you select Tolerate URL mismatch when matching parameters then Burp tolerates mismatches in the URL.

Normally, when deriving parameters from a prior response, Burp matches the parameter name and URL inferred from the response to the parameter name and URL in the subsequent request. This option is useful if the application employs CSRF tokens that are URL agnostic - that is, tokens that can be obtained from one location in the application and reused in another.

The Tolerate URL mismatch when matching parameters option simplifies these rules. It enables you to define a rule that runs on any request containing the CSRF token parameter, and that runs a single macro to obtain a new token from a fixed location.

Prompt for in-browser session recovery

This action causes Burp to prompt you to recover a valid session using Burp's browser. The cookies set by the application are added to Burp's session handling cookie jar, and can be updated in the current request if required.

You can select to either update all cookies (with specific exclusions if needed), or only certain specific cookies.

Run a post-request macro

This action issues the request that is currently being processed, and then runs a further macro. No further rules or actions are carried out on the request.

Post-request macros are useful if the request you are testing appears within a multi-stage process, and you need to step through the remaining stages to update the application's state and determine the effects of the targeted request.

You can configure Burp to use the response to the current request to update parameters in the first macro request. If this option is selected, then Burp can update all the parameters in the first macro request (with specific exclusions if required), or only specific parameters.

You can configure the action to pass the following back to the invoking tool:

The response from the current request, issued prior to executing the macro.

The final response from the macro.

The latter option is useful in cases where you are scanning or fuzzing input at one step in a multi-stage process, but a resulting error message is displayed at a later step in that process.

Invoke a Burp extension

This action invokes a Burp extension to process the current request. You can select the required extension from the list. Note that you can only select those extensions that have registered a session handling action handler.

Set a specific header value

This action replaces the value of a specified header within a request. Select the Add if not present checkbox to add the header to requests in which it is not already present.

Replace matching part of the request

This action replaces specified parts of requests sent by Burp to the target application. It can target any part of the request and is particularly useful for broad modifications, such as updating JSON content or modifying complex data formats.

To add a new action, specify the following:

Match - Define the string or regex pattern you want the rule to match. You can specify any

part of the request.

Replace - Define the string you want the rule to replace.

If you want Burp to treat the match parameter as a regex, select Regex match.

Note

As this action operates on the entire request, it doesn't take into account the Parameter scope setting in the Scope tab of the session handling rule editor.

Tools scope

The Tools scope settings are on the Scope tab of the session handling rule editor. These settings enable you to specify the Burp tools that each rule should apply to. Burp only processes rules for requests made by in-scope tools.

URL scope

The URL scope settings are on the Scope tab of the session handling rule editor. They enable you to specify the URLs that each rule should apply to. You can select from the following options:

All URLs. This setting is useful if you are creating a generic rule to use cookies from Burp's cookie jar.

The suite scope. This setting is useful if you are creating an application-wide rule, such as a rule to validate the current session.

A specific custom scope. This setting is useful if you are creating a rule affecting a single request.

More information

For more details on setting URL scope, see URL-matching rules.

Parameter scope

You can specify that rules should only apply to requests containing specific named parameters. This enables you to create a rule that updates a certain parameter across all requests, such as a CSRF token.
