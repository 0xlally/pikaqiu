# Evaluating inputs with Burp Suite

Source: https://portswigger.net/burp/documentation/desktop/testing-workflow/analyzing/evaluating-inputs
Fetched: 2026-06-28T09:15:57.549404+00:00

Support Center

Documentation

Desktop editions

Testing workflow

Analyzing the attack surface

Evaluating inputs

ProfessionalCommunity Edition

Evaluating inputs with Burp Suite

Last updated:

June 18, 2026

Read time:

3 Minutes

Once you have discovered functionality that is worth investigating further, you can use a range of Burp's tools to evaluate the user controllable inputs. This enables you to determine which inputs are most important to the application's function. For example, these may be inputs that impact the session or state of the application.

To evaluate inputs with Burp Suite, you can:

Manually evaluate individual inputs.

Scan the inputs.

Fuzz the inputs.

Before you start

We recommend that you complete the following steps before starting this tutorial:

Set the test scope. For more information, see Setting the initial test scope in Burp Suite.

Map the target application. For more information, see Mapping the target website with Burp Suite.

Identify requests that you want to investigate further. For more information, see Identifying

high-risk functionality.

Steps

You can follow along with the process below using a lab with a SQL injection vulnerability. For example,

SQL injection in WHERE clause allowing retrieval of hidden data.

Manually evaluating individual inputs

You can manually evaluate how individual inputs impact the application:

Send a request to Burp Repeater.

Go to the Repeater tab and modify each input in turn. For example, you can:

Remove the input.

Give the input an empty value.

Insert a Collaborator payload in the input. Highlight the input, then right-click and select Insert

Collaborator payload.

Click Send to send the request.

Review the responses for noteworthy behavior, such as input reflections or differences in response times.

To identify subtle changes between responses, send the responses to Burp Comparer. In Burp Comparer:

Select the two responses to compare.

Click Words or Bytes to compare the responses. A new window opens with the results. Comparer

highlights any differences between the responses.

Scanning inputs

If you're using Burp Suite Professional, you can scan inputs to identify potential vulnerabilities, which Burp Scanner flags as issues.

To scan a single input:

Highlight the input. You can do this from any message editor in Burp, for example from Proxy >

HTTP history.

Right-click and select Scan selected insertion point. The scan launcher opens.

Click OK to start the scan using the default configuration.

To scan multiple inputs at the same time:

Send the request to Burp Intruder.

Go to Intruder. Add a payload position for each input you want to scan:

Select the input.

Click Add §.

Right-click the request and select Scan defined insertion points. The scan launcher opens.

Click OK to start the scan using the default configuration.

Burp Scanner audits the request using only the selected inputs. To view the issues identified by the scan:

Go to the Dashboard tab.

From the Tasks list, select the relevant scan task.

Go to the Issues tab. This contains a record of the issues found in the scan.

Fuzzing inputs

You can fuzz an input to identify potential vulnerabilities:

Highlight the input in the request, then right-click and select Send to Intruder.

Go to Intruder. Notice that the input is

automatically marked as a payload position.

In the Payloads side panel, under Payload configuration, add a list of fuzz strings. If you're using Burp Suite Professional, open the

Add from list

dropdown menu and select the built-in Fuzzing - full list. Otherwise, add your own list.

Click Start attack. The attack starts in a new dialog. Burp Intruder sends a request for each fuzz payload.

When the attack is finished, study the responses to look for any noteworthy behavior.

Related pages

Burp Intruder

Burp Repeater

Burp Comparer

Burp Collaborator
