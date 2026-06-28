# Custom actions writing guide

Source: https://portswigger.net/burp/documentation/desktop/extend-burp/bambdas/creating/writing-custom-actions/writing-guide
Fetched: 2026-06-28T09:15:45.635153+00:00

Support Center

Documentation

Desktop editions

Extending Burp

Bambdas

Creating scripts

Writing custom actions

Writing guide

Professional

Custom actions writing guide

Last updated:

June 18, 2026

Read time:

11 Minutes

Custom actions are scripts that run directly in Burp Repeater to automate tasks and extract information during manual testing.

This page includes useful code snippets and building block examples of custom actions. If you're new to custom actions, we recommend starting with our worked example to see a breakdown of a complete script. Once you're familiar with the basics, use this page as a reference to build your own.

Related pages

Custom actions worked example.

Custom actions.

Creating custom actions.

Developing AI features in custom actions.

To view examples of custom actions that have been created by our researchers and the community, see our Bambdas GitHub repository - Custom actions.

On this page

API access

Step 1: Accessing request and response data

Step 2: Processing data

Step 3: Logging and using data

Example use cases

Decoding data

Encoding data

Sending modified requests

Sending repeated requests to test for race condition vulnerabilities

Fetching external data

Running shell commands

API access

Seven objects of the Montoya API are available to help you write custom action scripts:

HttpRequestResponse - Represents the full HTTP request and response.

RequestResponseSelection - Represents selected portions of a request or response.

HttpEditor - Provides access to editable HTTP message components in Repeater.

MontoyaApi - Provides access to Burp features.

Utilities - Provides access to the Montoya API helper functions.

Logging - Enables logging output to the Output panel in the Custom actions side panel.

Ai - Enables your custom actions to send prompts to a Large Language Model (LLM).

Related pages

Montoya API JavaDoc

Step 1: Accessing request and response data

To work with a HTTP message, you'll first need to access its contents.

Retrieving the full request or response

You can access the entire HTTP request or response using the HttpRequestResponse object:

// Get the full HTTP request

var request = requestResponse.request();

// Get the full HTTP response

var response = requestResponse.response();

Extracting specific parts of the message

If you only need to analyze a section of the message, you can retrieve specific parts of the request or response, such as the body or headers. For example:

// Get response body as a string

var responseBody = requestResponse.response().bodyToString();

// Get the value of a specific request header

var userAgent = requestResponse.request().headerValue("User-Agent");

Extracting user-selected content

If the user will select a specific section of the request or response when using the custom action, you can access the selection using RequestResponseSelection:

// Get selected text from the response as a string

var selectedText = selection.responseSelection().contents().toString();

// Get selected text from the request if available, or from the response, as a string

var messageSelection = selection.hasRequestSelection() ? selection.requestSelection() : selection.responseSelection();

var selectedText = messageSelection.contents().toString();

Extracting the HTTP service

To identify the request destination, retrieve the HttpService object. This is useful when integrating with external tools or running shell commands.

// Get the HTTP service from the request

var service = requestResponse.request().httpService();

Always check that the HttpService is not null before using it:

if (service == null) {

return;

}

Handling empty or missing content

To avoid unnecessary processing or errors, add checks for null or empty content before acting on a response or user selection. This is particularly important if you're using the content as input for an AI model, as it can reduce unnecessary costs. For example:

// Check for an empty or missing response

if (requestResponse.response() == null || requestResponse.response().toString().isEmpty()) {

return;

}

// Check for an empty user selection in the response

if (!selection.hasResponseSelection()) {

return;

}

Step 2: Processing data

Once you've accessed the message, you can process and analyze the data in various ways:

Using AI to analyze messages

To learn how to add AI-powered features to your custom actions, see Developing AI features in custom actions.

Modifying editor content

You can programmatically update the request or response shown in an HTTP editor using the requestPane() and responsePane() methods. These return EditorPane objects, which provide methods for modifying content:

// Set plain text in the request editor

httpEditor.requestPane().set("example");

// You can also pass other objects, their toString() output will be used

httpEditor.requestPane().set(123); // Sets the content to "123"

// Set binary content using a ByteArray

httpEditor.requestPane().set(ByteArray.byteArray("example"));

// Replace all instances of a placeholder string in the response

httpEditor.responsePane().replace("replace_all_occurances_of_this", "with_this");

EditorPane.set() doesn't update the underlying message object. To log or reuse the updated content in the same custom action, store it in a variable before calling set(). For example:

// This logs the original request

httpEditor.requestPane().set("example");

logging().logToOutput(requestResponse.request());

// This logs the updated value that you set in the editor

var newContent = "example";

httpEditor.requestPane().set(newContent);

logging.logToOutput(newContent);

Note

For practical examples of custom actions that modify requests and set responses, see Sending modified requests.

Replacing selected content in the editor

If you need to modify or replace a section of the message using selected text, you'll need to know exactly where that selection occurs. Use offsets() to get the start and end positions of the selection:

int start = selection.requestSelection().offsets().startIndexInclusive();

int end = selection.requestSelection().offsets().endIndexExclusive();

Then, get the complete request as a string so you can rebuild it:

var requestStr = requestResponse.request().toString();

You can then insert your own content into the original message in the correct location:

var updatedRequest = requestStr.substring(0, start) + "NEW_VALUE" + requestStr.substring(end);

// Set the updated request in the request editor

httpEditor.requestPane().set(updatedRequest)

Note

It's best practice to add a check for null or empty content before acting on a user selection. This helps avoid unnecessary processing or errors. For more information, see Handling empty or missing content.

Step 3: Logging and using the data

You can extract, log, and forward the results of your custom action in any way that fits your workflow.

Logging to output

To log data to the Output pane in the Custom actions side panel, use the logging().logToOutput() method. For example:

// Log a simple message

logging.logToOutput("Custom action triggered");

// Log the length of the response body

var responseBody = requestResponse.response().bodyToString();

logging.logToOutput("Response body length: " + responseBody.length());

Sending data to other Burp tools

You can send data to other Burp tools using the api() object. This can be useful when you want to integrate your custom action into your testing workflow:

// Send the original request to a new Organizer tab

api.organizer().sendToOrganizer(requestResponse.request());

// Add a custom header and send the request to a new Repeater tab

var updatedRequest = requestResponse.request().withUpdatedHeader("X-Debug", "true");

api.repeater().sendToRepeater(updatedRequest);

Logging data to a file

You can log data to an external file, for example a text file in the user's home directory. Make sure to handle errors gracefully to avoid unexpected failures, such as when the file path doesn't exist or can't be written to:

// Define the path to a file called "output.txt" in the user's home directory

var filePath = System.getProperty("user.home") + File.separator + "output.txt";

// Get the content you want to log

var line = requestResponse.httpService().toString();

// Open the file in append mode and make sure it closes automatically afterward

try (FileWriter writer = new FileWriter(filePath, true)) {

writer.write(line + "\n"); // Append the HTTP service to the file, followed by a newline

// Log a success message to the Output panel

logging.logToOutput("HTTP service recorded.");

} catch (IOException e) {

// Log an error message if writing to the file fails

logging.logToError("Could not write to " + filePath, e);

}

Example use cases

This section covers the following use cases:

Decoding data.

Encoding data.

Sending modified requests.

Sending repeated requests to test for race condition vulnerabilities.

Fetching external data.

Running shell commands.

Decoding data

To decode data in a request or response, you'll need to do the following:

Extract the relevant section of the message.

Use a regular expression or decoding logic to process the data.

Output the result, or replace the original data with the decoded version.

The following example decodes any \uXXXX Unicode escape sequences found in user-selected sections of a response and replaces the selection with the decoded characters:

//Check for an empty user selection in the response

if (!selection.hasResponseSelection()) {

return;

}

// Get selected text from the response as a string

var selectedResponseText = selection.responseSelection().contents().toString();

// Create a regex pattern to find \uXXXX Unicode escape sequences

var pattern = Pattern.compile("\\\\u([0-9a-fA-F]{4})");

// Match Unicode escape sequences in the selected text, extract the 4 hex digits, convert them to an integer, then to a character

var decodedText = pattern.matcher(selectedResponseText).replaceAll(match -> String.valueOf((char) Integer.parseInt(match.group(1), 16)));

// Log the decoded sequences to the Output pane

logging.logToOutput(decodedText);

// Convert the entire HTTP request to a string for modification

var responseStr = requestResponse.response().toString();

// Get the start and end indices of the selection

int start = selection.responseSelection().offsets().startIndexInclusive();

int end = selection.responseSelection().offsets().endIndexExclusive();

// Replace the selected portion in the response with the decoded text

var updatedResponse = responseStr.substring(0, start)

+ decodedText

+ responseStr.substring(end);

// Set the updated response in the editor

httpEditor.responsePane().set(updatedResponse);

Encoding data

To encode data in a request or response, you'll need to do the following:

Extract the relevant section of the message.

Apply an encoding transformation to the data.

Output the result, or replace the original data with the encoded version.

The following example encodes the selected portion of a request using the MIME encoded-word format with base64 encoding, and replaces the selection with the encoded result. This can be useful for testing how systems handle obfuscated values, such as email addresses.

//Check for an empty user selection in the request

if (!selection.hasRequestSelection()) {

return;

}

// Get the selected string from the request

var input = selection.requestSelection().contents().toString();

// Set the character set used in the encoded-word

var charset = "iso-8859-1";

// Encode the selected input using base64

var encodedWord = api.utilities().base64Utils().encode(input);

// Construct the full encoded-word string

var encodedWordPlusMeta = "=?"+charset+"?b?"+encodedWord+"?=";

// Convert the entire HTTP request to a string for modification

var requestStr = requestResponse.request().toString();

// Get the start and end indices of the selection

int start = selection.requestSelection().offsets().startIndexInclusive();

int end = selection.requestSelection().offsets().endIndexExclusive();

// Replace the selected portion in the request with the encoded word

var updatedRequest = requestStr.substring(0, start)

+ encodedWordPlusMeta

+ requestStr.substring(end);

// Set the updated request in the editor

httpEditor.requestPane().set(updatedRequest);

Sending modified requests

You can create custom actions that modify requests before sending them, then analyze or update the response. This is useful for testing how the server behaves when you modify headers, paths, or other request components.

To modify and send a request:

Get the relevant section of the request.

Change, remove, or add elements of the request.

Send the updated request using the api() object.

Log or update the response.

This example can help identify access control vulnerabilities by removing the Authorization and Cookie headers from the request, sending the request, then updating the response:

// Get the original HTTP request

var request = requestResponse.request();

// Remove the "Authorization" and "Cookie" headers from the request

var modifiedRequest = request.withRemovedHeader("Authorization").withRemovedHeader("Cookie");

// Update the request editor to reflect the modified request

httpEditor.requestPane().set(modifiedRequest);

// Send the modified request and get the response

var response = api().http().sendRequest(modifiedRequest).response();

// Update the response editor to show the new response

httpEditor.responsePane().set(response);

This example explores path traversal behavior by changing the request path, sending the request, then updating the response:

// Add /../../ to the original request path

var modifiedRequest = requestResponse.request().withPath("/../../");

// Send the modified request and get the response

var response = api().http().sendRequest(modifiedRequest).response();

// Update the response pane to show the new response

httpEditor.responsePane().set(response);

Sending repeated requests to test for race condition vulnerabilities

To test how a server handles repeated requests, you can create a custom action that sends the same request multiple times, then logs output from the response. This enables you to test for race condition vulnerabilities with a single click.

The following example sends the same request multiple times in parallel, extracts the HTTP response status codes, and logs them to the output. It uses the single-packet attack for HTTP/2, and last-byte synchronization for HTTP/1:

// Set the number of requests to send

int NUMBER_OF_REQUESTS = 10;

// Create a list to hold the duplicated HTTP requests

var reqs = new ArrayList<HttpRequest>();

// Duplicate the request multiple times and add them to the list

for (int i = 0; i < NUMBER_OF_REQUESTS; i++) {

reqs.add(requestResponse.request());

}

// Send all the requests in parallel and get the responses

var responses = api().http().sendRequests(reqs);

// Extract the HTTP status codes from the responses

var codes = responses.stream()

.map(HttpRequestResponse::response)

.map(HttpResponse::statusCode)

.toList();

// Log the status codes

logging.logToOutput(codes);

Fetching external data

You can make outbound HTTP requests to retrieve external data.

To fetch external data:

Set the URL to fetch data from.

Send the request using the api() object.

Parse the response body to extract the data you need.

Output the result.

This example sends a GET request to PortSwigger's research RSS feed and extracts the link to the latest article:

// Sets the URL to fetch data from

var apiURL = "https://portswigger.net/research/rss";

// Send a GET request and get the response body

var responseBody = api().http().sendRequest(HttpRequest.httpRequestFromUrl(apiURL)).response().bodyToString();

// Use string splitting to extract the first link from the first >item< in the RSS feed

var extractedData = responseBody.split(">item<")[1].split(">link<")[1].split("<")[0];

// Log the extracted link

logging.logToOutput(extractedData);

Running shell commands

You can run shell commands from your custom action using utilities().shellUtils(). This can be useful for triggering external tools and scripts, or collecting information from the underlying operating system.

There are two ways to run commands:

// Pass the command and its arguments as separate strings

var output = utilities().shellUtils().execute("my-command", "arg1", "arg2");

// Run the shell command using a single string

var output = utilities().shellUtils().dangerouslyExecute("my-command arg1 arg 2");

Warning

Avoid using dangerouslyExecute() with any user-controlled input. It passes the entire string directly to a shell, which can be exploited for command injection.

To safely include dynamic arguments, use execute() and pass the command and each argument as separate strings. Never use user input as the first argument, as this controls which command is run and could be exploited to run unintended programs. Always hard-code the command and only pass user input as separate arguments.

To customize how a command runs, use the ExecuteOptions object. For a full list of available options, see the API documentation.

This example runs a traceroute command to the host of the current request and logs the result:

// Get the HttpService from the current request

HttpService service = requestResponse.request().httpService();

// Exit early if no service is available

if (service == null) {

return;

}

// Run the traceroute command using the host from the service

String output = utilities().shellUtils().execute(

executeOptions()

// Set a 15-second timeout

.withTimeout(Duration.ofSeconds(15))

// Allow the command to time out without failing

.withTimeoutBehavior(TimeoutBehavior.ALLOW_TIMEOUT),

// Merge errors with the standard output; all output appears in the Output pane

.withStderrBehavior(StderrBehavior.MERGE)

// Silently ignore any non-zero exit codes returned by the traceroute

.withExitCodeBehavior(ExitCodeBehavior.ALLOW_NON_ZERO)

// Add the command and arguments

"traceroute", service.host()

);

// Log the traceroute output to the Output panel

logging().logToOutput(output);

This example runs the aws sts get-caller-identity command to return information about the current AWS credentials, using environment variables to authenticate:

// Run the AWS CLI command to identify the caller identity

String output = utilities().shellUtils().execute(

executeOptions()

// Set the AWS access key ID

.withEnvironmentVariable("AWS_ACCESS_KEY_ID", "AKIAEXAMPLEKEY123")

// Set the AWS secret access key

.withEnvironmentVariable("AWS_SECRET_ACCESS_KEY", "supersecretkeyvalue")

// Set the AWS region

.withEnvironmentVariable("AWS_DEFAULT_REGION", "us-west-2"),

// Add the command and arguments

"aws", "sts", "get-caller-identity"

);

// Log the result to the Output panel

logging().logToOutput(output);

Related pages

To get feedback, showcase your work, and connect with other developers, share your custom action on our PortSwigger Discord #bambdas channel.

To share your custom actions with the community, add them to our ever-growing GitHub repository. For more information, see Submitting Bambdas to our GitHub repository.
