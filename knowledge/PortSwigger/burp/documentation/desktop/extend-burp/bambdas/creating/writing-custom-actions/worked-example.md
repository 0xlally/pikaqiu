# Custom action worked example

Source: https://portswigger.net/burp/documentation/desktop/extend-burp/bambdas/creating/writing-custom-actions/worked-example
Fetched: 2026-06-28T09:15:45.488277+00:00

Support Center

Documentation

Desktop editions

Extending Burp

Bambdas

Creating scripts

Writing custom actions

Worked example

Professional

Custom action worked example

Last updated:

June 18, 2026

Read time:

2 Minutes

Custom actions are scripts that run directly in Burp Repeater to automate tasks and extract information during manual testing.

In the worked example below, we'll use Java to write a custom action that extracts a CSRF token from the response body, modifies it, then logs the modified CSRF token.

In this example, our custom action script is:

var resp = requestResponse.response().bodyToString();

if (resp.contains("csrf=")){

var csrfIndex = resp.lastIndexOf("csrf=")+5;

var csrf = resp.substring(csrfIndex, csrfIndex+16);

csrf = csrf.replace("a", "b").replace("c", "d");

logging.logToOutput(csrf);

}

else{

logging.logToOutput("No CSRF token");

}

Step 1: Get the response body

var response = requestResponse.response().bodyToString();

This retrieves the body of the HTTP response and stores it as a string in the response variable.

Breakdown of the code:

requestResponse represents the request/response pair the action is applied to.

response().bodyToString() gets the response object and converts the body to a string.

Step 2: Check the response body for the CSRF token

if (response.contains("csrf=")) {

This checks whether the response body object contains the string csrf=. If the string is found, the statement returns true.

Step 3: Extract and process the token

var csrfIndex = response.lastIndexOf("csrf=") + 5;

var csrf = response.substring(csrfIndex, csrfIndex + 16);

csrf = csrf.replace("a", "b").replace("c", "d");

This runs if the response body contains the string csrf=. It finds the last occurrence of csrf=, extracts the 16-character token that follows, and modifies it by replacing certain characters.

Breakdown of the code:

lastIndexOf("csrf=") returns the index of the last occurrence of csrf= in the response.

+5 moves the index to the start of the actual token, just after csrf=.

response.substring(csrfIndex, csrfIndex + 16) extracts the 16 characters of the token from the response, starting at csrfIndex and ending at csrfIndex + 16.

replace("a", "b").replace("c", "d") replaces characters a with b, and c with d in the extracted CSRF token.

Step 4: Log the result

logging.logToOutput(csrf);

This logs the modified CSRF token to the Output panel in the Custom actions side panel.

Step 5: Handle the situation where no token is found

else{

logging.logToOutput("No CSRF token");

}

If the csrf= string isn't found in Step 2, this logs the message No CSRF token.

Related pages

For useful code snippets and building block examples of custom actions, see our Custom

actions writing guide.

To learn how to add AI features to your custom actions, see Developing AI features in custom actions.

To learn more about how to use custom actions, see Custom actions.
