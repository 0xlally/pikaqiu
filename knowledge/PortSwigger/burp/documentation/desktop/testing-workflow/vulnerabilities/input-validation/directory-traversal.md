# Testing for directory traversal vulnerabilities with Burp Suite

Source: https://portswigger.net/burp/documentation/desktop/testing-workflow/vulnerabilities/input-validation/directory-traversal
Fetched: 2026-06-28T09:15:59.898059+00:00

Support Center

Documentation

Desktop editions

Testing workflow

Testing for vulnerabilities

Testing input validation

Testing for directory traversal vulnerabilities

ProfessionalCommunity Edition

Testing for directory traversal vulnerabilities with Burp Suite

Last updated:

June 18, 2026

Read time:

2 Minutes

Directory traversal vulnerabilities (also known as file path vulnerabilities) allow an attacker to read arbitrary files on the server that is running an application. This might include application code and data, credentials for back-end systems, and sensitive operating system files.

You can use Burp to test for these vulnerabilities:

Professional Use Burp Scanner to automatically flag potential directory traversal vulnerabilities.

Use Burp Intruder to insert a list of directory traversal fuzz strings into a request. The strings may enable you to read arbitrary files on the server.

Steps

You can follow this process using the File path traversal, traversal sequences stripped with superfluous

URL-decode lab from our Web Security Academy.

Scanning for directory traversal vulnerabilities

If you're using Burp Suite Professional, you can use Burp Scanner to test for directory traversal vulnerabilities:

In Proxy > HTTP history, identify a request that you want to investigate.

Right-click the request and select Do active scan. Burp Scanner audits the request.

Review the Issues list on the Dashboard to identify any directory traversal issues that Burp Scanner flags.

Fuzzing for directory traversal vulnerabilities

You can alternatively use Burp Intruder to test for directory traversal vulnerabilities. This process also enables you to closely investigate any issues that Burp Scanner has identified:

In Proxy > HTTP history identify a request you want to investigate.

Right-click the request and select Send to Intruder.

Go to Intruder.

Highlight the parameter that you want to test and click Add § to mark it as a payload position.

In the Payloads side panel, under Payload configuration, add a list of directory traversal fuzz strings:

If you're using Burp Suite Professional, select the built-in Fuzzing - path traversal wordlist.

If you're using Burp Suite Community Edition, manually add a list.

Click Start attack. The attack starts running in a new dialog. Intruder sends a request for each fuzz string on the list.

When the attack is finished, study the responses to look for any noteworthy behavior. For example, look for responses with a longer length. These may contain data that has been returned from the requested file.

Related pages

Academy: Directory traversal

Scanning specific HTTP messages

Burp Intruder
