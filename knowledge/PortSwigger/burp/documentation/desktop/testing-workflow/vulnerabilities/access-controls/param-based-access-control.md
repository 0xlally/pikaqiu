# Testing for parameter-based access control

Source: https://portswigger.net/burp/documentation/desktop/testing-workflow/vulnerabilities/access-controls/param-based-access-control
Fetched: 2026-06-28T09:15:58.916025+00:00

Support Center

Documentation

Desktop editions

Testing workflow

Testing for vulnerabilities

Testing access controls

Testing for parameter-based access control

ProfessionalCommunity Edition

Testing for parameter-based access control

Last updated:

June 18, 2026

Read time:

2 Minutes

Some sites use insecure access controls based on request parameters. For example, a site might use a role_id parameter to denote whether the user should be treated as having admin privileges in the associated response.

Even if these parameters don't enable you to bypass server-side access controls, they might still be able to get past some client-side controls. For example, they might reveal additional attack surface, such as an admin page that you can view but not necessarily interact with.

You can test the effect that these parameters have by using Burp Suite's match and replace rules to swap out values and analyze the results.

Before you start

Before you start, you should map out the application's visible attack surface. See Mapping the visible attack surface with Burp Suite for more information.

Steps

Select Burp > Search from the top-level menu to open the Burp Suite search dialog.

Use the Search bar to search for any potentially-insecure parameter values such as false and read. Note any values that return results.

Go to Proxy > Match and replace.

Under HTTP match and replace rules, click Add.

Configure a new match and replace rule:

Select Request header from the Type drop-down list.

Enter one of the parameter values that returned results during the search into the Match field.

Enter the value that Burp should replace the selected parameter with into the Replace field. For example, replace the parameter value false with the value true.

Click OK to save your rule.

Repeat step 4 to set up rules for Request body and Request param value.

Set up rules for any other parameter values found in the search that you want to test.

Use the process described in Mapping the visible attack surface with Burp Suite to re-map the site. Note whether the attack surface has changed as a result of the new match and replace rules.

Related pages

Match and replace

Lab: User role controlled by request parameter - This lab shows an example of an access control vulnerability in which admin status is denoted by a request header.
