# Burp Intruder attack settings

Source: https://portswigger.net/burp/documentation/desktop/tools/intruder/configure-attack/settings
Fetched: 2026-06-28T09:16:05.157330+00:00

Support Center

Documentation

Desktop editions

Tools

Intruder

Configure attack

Settings

ProfessionalCommunity Edition

Burp Intruder attack settings

Last updated:

June 18, 2026

Read time:

7 Minutes

You can configure Burp Intruder attack settings before you launch an attack in the Settings side panel. You can open or close the side panel by clicking the Settings tab. You can also modify many of the settings while the attack is running. Edit these in the cloned

Settings side panel in the results window.

Note

To configure Burp Intruder user settings for startup and closing behavior, and to upload payload lists, go to the Intruder page in the

Settings dialog. To open the dialog, click Settings in the top toolbar. For more information, see Intruder settings.

Save attack

Professional By default, attacks are saved in-memory, so they are lost if you close Burp Suite. However, you can save them to your project file. Select Save attack to project file.

We recommend that you only save attacks when you find something interesting. If you save too many attacks to project files it can result in large files.

Request headers

These settings control whether Intruder updates the configured request headers during attacks:

Update Content-Length header - Add or update the Content-Length header in each request with the correct length of the request's HTTP body. This is useful for attacks that insert variable-length payloads into the body of the template HTTP request. If the correct length is not specified, then the target server may return an error, respond to an incomplete request, or wait indefinitely for further data to be received in the request.

Set Connection header - Add or update the Connection header with the value close. This may mean attacks are performed more quickly when the server does not itself return a valid Content-Length or Transfer-Encoding header.

Error handling

These settings control how Intruder handles network errors during an attack:

Number of retries on network failure - Specify the number of times Burp retries a request when a failure occurs. Intermittent network failures are common when testing, so it is best to retry the request several times.

Pause before retry - Specify the time (in milliseconds) that Burp waits before retrying a failed request. If the server is being overwhelmed with traffic, or an intermittent problem is occurring, it is best to wait a short time before retrying.

Attack results

These settings control what information is captured in the attack results:

Store requests / responses - Specify whether the attack saves the contents of individual requests and responses. This consumes disk space in your temporary directory, but enables you to:

View requests and responses in full during an attack.

Repeat individual requests if necessary.

Send requests or responses to other Burp tools.

Make unmodified baseline request - Set the attack to issue the template request with all payload positions set to their base values, in addition to the configured attack requests. The request shows as item 0 in the results table. This is useful to provide a base response against which to compare the attack responses.

Use denial-of-service mode - Set the attack to not process any responses received from the server. As soon as each request is issued, the TCP connection is closed. This is useful for application-layer denial-of-service attacks against vulnerable applications, as it repeatedly sends requests that initiate high-workload tasks on the server, while avoiding locking up local resources by holding sockets open for the server to respond.

Store full payloads - Store the full payload values for each result. This consumes additional memory but may be required to perform certain actions at runtime, such as modifying payload grep settings, or resending requests with a modified request template.

Auto-pause attack

These settings automatically pause the attack when a specified expression appears in or is missing from a response.

To auto-pause the attack:

Select Enable auto-pause.

Choose one of the following options:

Pause if an expression in the list appears in a response.

Pause if an expression in the list is missing from a response.

Add expressions to the list that you want to check for in responses.

Select the Match type for your expressions:

Simple string - Match the exact string.

Regex - Match a regular expression.

If required, enable Case-sensitive match to match uppercase and lowercase exactly as typed.

During the attack, Burp automatically pauses the attack if a response contains (or doesn't contain) the expressions. You can resume the attack at any time by clicking . Once resumed, Burp will pause the attack each time a response meets the auto-pause condition.

Grep - match

These settings flag result items that contain specified expressions in the response.

Flag responses matching these expressions - Specify a list of expressions to flag. By default, the expressions list shows some common error strings that are useful when fuzzing.

Match type - Specify whether the expressions are simple strings or regular expressions.

Case sensitive match - Specify whether the check for the expression is case-sensitive.

Exclude HTTP headers - Specify whether the HTTP response headers are excluded from the check.

During the attack, Burp adds a results column for each expression in the list. This records the number of times the expression is found in the response. To identify results with the expression, click on the column header to sort the results.

Related pages

You can use the Grep - match settings to quickly identify interesting items from large sets of results. For more information, and some common use cases, see:

Fuzzing for vulnerabilities.

Enumerating identifiers.

Grep - extract

These settings extract information from responses.

To specify an interesting string for information extraction, select Extract the following items from responses, and click Add. A new window opens in which you can define the location of the item to be extracted.

Note

To extract information from multiple occurrences of an item, add the item multiple times in succession. This is useful, for example, when an HTML table contains useful information but there are no unique prefixes with which to automatically pick out each item.

To configure a maximum length that Burp captures for each item, enter a value in the Maximum capture length field.

During the attack, Burp adds a results column for the extracted information. Click the column header to sort the results.

Related pages

For more information on how to configure the details of items to extract, see Response extraction rules.

You can use the Grep - extract settings to mine data from an application. For more information and some common use cases, see Harvesting useful data.

Grep - payloads

These settings can be used to flag result items containing reflections of the submitted payload:

Case sensitive match - Specify whether the check for the payload is case-sensitive.

Exclude HTTP headers - Specify whether the HTTP response headers should be excluded from the check.

Match against pre-URL-encoded payloads - Check responses for payloads in their pre-encoded form. This may be necessary if you have configured Intruder to URL-encode payloads within requests. These are normally decoded by the application and echoed in their original form.

During the attack, Burp adds a results column that records the number of times the payload is found in the response. If more than one payload set is used, a separate column is added for each payload set.

You can use the Grep - payloads settings to detect cross-site scripting and other response injection vulnerabilities, which can arise when user input is dynamically inserted into the application's response.

Redirections

These settings control how Burp handles redirections when performing attacks. It is often necessary to follow redirections to achieve the objectives of your attack. For example:

In a password guessing attack, the result of each attempt might only be displayed by following a redirection.

When fuzzing, relevant feedback might only appear in an error message that is returned after an initial redirection response.

Note

Automatically following redirections may sometimes cause problems for your attack. For example, if the application responds to a malicious request with a redirection to the logout page, then your session may be terminated.

The following settings are available:

Follow redirections - Control the targets of redirections. You can choose from:

Never.

On-site only.

In-scope only.

Always.

Process cookies in redirections - Resubmit any cookies set in the redirection response when the redirection target is followed. This may be necessary, for example, if you are attempting to brute force a login challenge that always returns a redirection to a page indicating the login result, and a new session is created in response to each login attempt.

Burp follows up to 10 chained redirections. A column in the results table indicates whether a redirect was followed for each individual result. The full requests and responses in the redirection chain are stored with each result item.

You can configure the types of redirection that Burp processes in the suite-wide redirection settings. These are found under Proxy in the Settings dialog. Click on Settings to open the dialog. For more information, see HTTP Settings.

Note

It may be necessary to use only a single-threaded attack when following redirections. For example, when the application stores the result of the initial request within your session, and retrieves this when delivering the redirection response.

HTTP/1 connection reuse

Use this setting to control whether Burp Intruder reuses connections to issue multiple HTTP/1 requests. This can greatly increase the speed of your attacks.

If you deselect HTTP/1 connection reuse, Burp opens a new connection for each request and closes it after receiving a response.

HTTP version

Use this setting to control whether Burp Intruder uses HTTP/2 or HTTP/1 for the current attack.

If you enable Override the project-level HTTP/2 setting, then Burp ignores the current project-level HTTP/2 setting configuration.

You can then choose whether to use HTTP/2 or HTTP/1 for the current attack. Select Default to HTTP/2 if

the server supports it to use HTTP/2 with all servers that advertise support for it during the TLS handshake. Deselect this option to use HTTP/1 even if the server supports HTTP/2.

Note

HTTP settings - HTTP/2 - Gives more information about the project-level HTTP/2 setting.
