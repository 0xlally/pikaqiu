# Fuzzing for vulnerabilities

Source: https://portswigger.net/burp/documentation/desktop/tools/intruder/uses/fuzzing
Fetched: 2026-06-28T09:16:05.955340+00:00

Support Center

Documentation

Desktop editions

Tools

Intruder

Uses

Fuzzing

ProfessionalCommunity Edition

Fuzzing for vulnerabilities

Last updated:

June 18, 2026

Read time:

1 Minute

You can use Burp Intruder to identify input-based vulnerabilities by analyzing the attack results for error messages and other exceptions.

Related pages

For more information on input-based vulnerabilities, see:

SQL injection.

Cross-site scripting.

Directory traversal.

Given the size and complexity of today's applications, manually fuzzing for vulnerabilities is a time-consuming process. You can automate the process with Burp Intruder.

Step 1: Set the payload positions

Set payload positions at the values of all request parameters.

Step 2: Set the payload type

Select the simple list payload type, then add a list of attack strings under Payload configuration.

You can use your own list of attack strings, or one of Burp's predefined payload lists of common fuzz strings if you're using Burp Suite Professional. For more information, see Predefined payload lists.

Step 3: Set the match grep

Configure the Grep - Match settings to flag responses that contain various common error message strings. For more information, see Burp Intruder attack settings.

You can use your own expressions, or use the default items.

Step 4: Analyze the results

Sort the attack results by the match grep expressions to identify any results with the common error message strings.

Note

To test a large number of requests with the same payloads and match grep configuration, you can save or copy the tab's configuration. For more information, see Configuring Burp Intruder attacks.
