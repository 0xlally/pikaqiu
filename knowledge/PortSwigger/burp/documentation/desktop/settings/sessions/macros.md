# Macro editor

Source: https://portswigger.net/burp/documentation/desktop/settings/sessions/macros
Fetched: 2026-06-28T09:15:55.724465+00:00

Support Center

Documentation

Desktop editions

Settings

Sessions

Macros

ProfessionalCommunity Edition

Macro editor

Last updated:

June 18, 2026

Read time:

4 Minutes

The macro editor enables you to add and edit macros. You can open the macro editor from Settings > Sessions > Macros. Either select Add to add a new macro in the Editor, or Edit to edit an existing one.

Record macro

Macros are made up of requests taken from the Proxy history. The first step in adding a macro is to select these requests. To do so:

Click Add to open the Macro Recorder dialog.

Select the items you need from the Proxy history list. If required, you can use Burp's browser to add new requests.

Click OK to add the items to the Macro Editor.

Note

You cannot record new items using the browser if Proxy interception is turned on. You can disable interception by clicking Intercept is on in the corner of the macro recorder.

Configure item

The macro editor displays an editable list of items in the macro. You can modify macro items directly by selecting them in the list and then editing them in the request viewer.

Each macro specifies how items in the sequence should be handled, and any interdependencies between items. To edit this configuration, select the relevant item in the list and click Configure item to open the Configure Macro Item dialog.

Cookie handling

You can configure:

Whether cookies received in the response should be added to the session handling cookie jar.

Whether cookies from the session handling cookie jar should be added to the request.

Parameter handling

You can configure the values of the request parameters in the macro. The available options are:

Use preset value - The parameter always takes the specified value.

Derive from prior response - The parameter takes the value of an equivalent parameter from an earlier response.

The ability to derive a request parameter's value from a previous response is particularly useful in some multi-stage processes, and in situations where applications make aggressive use of CSRF tokens.

Parameter derivation is based on the parameter name and the URL requested. If you specify that a parameter's value should be derived from a previous response, Burp examines that response for instances where the named parameter was submitted to the relevant URL. For example, a form that uses the given action URL and contains a field with the given name. If Burp finds a suitable source, it extracts the parameter's value from that response and updates it in the request.

When you define a new macro, Burp automatically tries to find any relationships of this kind by identifying parameters whose values can be determined from the preceding response. For example: form field values, redirection targets, or query strings in links. You can override the automatic analysis if required.

Custom parameter locations in response

Automatic parameter matching works for standard parameter locations within responses, such as form field values and query strings in links. In some cases, you may need to manually specify the location within a response that contains a parameter. For example, an application might define a CSRF token within a JavaScript string, and dynamically add this token to a script-generated request. To create a macro capable of deriving this parameter, you need to add a custom parameter location. Custom parameter locations tell Burp the location of the parameter within the response that contains the script, and the name used for that parameter in subsequent requests.

To add a custom parameter, click Add in the Custom parameter locations in response section to display the Define custom parameter dialog.

From here you can specify the following:

The Parameter name.

Whether the value extracted from the response is URL-encoded. This setting ensures that Burp can correctly encode the value when it is used in subsequent requests.

The location of the parameter within the response item being configured. You can specify this location using Burp's standard response extraction rules.

More information

For information on using Burp's response extraction rules, see the Response extraction rules page.

Burp makes the configured parameter available for use in subsequent macro requests, or the request being processed by a session handling rule, as described in the Parameter Handling section.

Re-analyze macro

When you add a new macro, Burp automatically tries to find any relationships between macro items by identifying parameters whose values can be determined from the preceding response. You can repeat this automatic analysis using the Re-analyze macro button. This is useful if you have modified the items in the macro manually.

Test macro

The Test macro feature enables you to verify that your macro configuration works as intended. Burp issues the macro requests in sequence and attempts to derive any parameter values.

Once the macro has run, Burp displays the following:

All requests and responses.

The values of any cookies received.

The details of any parameters that Burp attempted to derive values for.
