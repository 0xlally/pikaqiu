# Maintaining an authenticated session

Source: https://portswigger.net/burp/documentation/desktop/testing-workflow/vulnerabilities/session-management/maintaining-authenticated-session
Fetched: 2026-06-28T09:16:01.172823+00:00

Support Center

Documentation

Desktop editions

Testing workflow

Testing for vulnerabilities

Testing session management mechanisms

Maintaining an authenticated session

ProfessionalCommunity Edition

Maintaining an authenticated session

Last updated:

June 18, 2026

Read time:

3 Minutes

When testing, some actions may result in an application terminating your session. For example, an application may automatically log you out if you submit suspicious input. This may prevent you from performing actions such as fuzzing with Burp Intruder.

Burp enables you to configure a session handling rule to automatically log back into an application. The session handling rule determines whether a session is valid. If it's invalid, it will run a macro to update the session cookies and log back in.

You can follow along with the process below using ginandjuice.shop, our deliberately vulnerable demonstration site. The process consists of three steps:

Identifying a valid login expression.

Configuring a session handling rule.

Checking the session handling rule.

Identifying an invalid login expression

Before you configure a session handling rule, you need to identify how the target site behaves when the session is invalid.

In Burp's browser, log in to the target site using valid credentials. If you're using ginandjuice.shop, the credentials are carlos:hunter2.

Go to a page that requires you to be logged in to access it. If you're using ginandjuice.shop, visit My Account.

Log out.

Try to get back to My Account without logging in. If you're using ginandjuice.shop, notice that you are redirected to the login page instead.

In Burp, go to the Proxy > HTTP history tab to identify the behavior of the target site when an unauthorized user tries to access a restricted page. If you're using ginandjuice.shop, trying to access My Account when you're not logged in results in a 302 redirect to /login.

Configuring a session handling rule

To configure a session handling rule that enables you to maintain an authenticated session:

Click Settings to open the Settings dialog.

Under Sessions > Session handling rules, click Add. The session handling rule editor opens.

Go to the Scope tab. Select the tools and URLs that you want the rule to apply to. The default tool scope and the suite URL scope are suitable for most use cases.

Go to the Details tab. Add a unique rule description.

Under Rule actions, click Add, then select Check session is valid from the drop-down menu. The session handling action editor opens.

Under Inspect response to determine session validity, specify the expression that is found in an invalid login response. This should be the expression you identified earlier. Also, specify the aspects of each in-scope response that Burp should inspect for the expression:

Location(s) - Select the locations in the response that you want Burp to inspect. If you're using ginandjuice.shop, select URL of redirection target.

Look for expression - Specify the expression that is found in a valid login response. If you're using ginandjuice.shop, enter login.

Match type - Select whether the expression is a literal string or regex. If you're using ginandjuice.shop, select Literal string.

Case-sensitivity - Select whether the expression is case-sensitive or insensitive. If you're using ginandjuice.shop, select Insensitive.

Match indicates - Select whether a match indicates that the session is valid or invalid. If you're using ginandjuice.shop, select Invalid session.

Under Define behavior dependent on session validity, select If session is invalid, perform the action below > Run a macro.

Click Add. The Macro editor and Macro recorder dialogs open.

In the Macro recorder dialog, select the login requests, then click OK. If you're using ginandjuice.shop, select the GET /login and the two POST /login requests.

Click OK to close all open dialogs. The rule is added to the list of session handling rules.

Checking the session handling rule

It's a good idea to check that the session handling rule works. To do this:

In Burp's browser, log out of the website.

In Proxy > HTTP history, identify a request for a page that you need to be logged in to access. For example, if you're using ginandjuice.shop, you can use a GET /my-account request. The page should contain a session cookie that is now invalid.

Right-click the request and select Send to Repeater.

Go to the Repeater tab and send the request. Notice that the session cookies automatically update.

Review the response to confirm that you've logged in successfully.

Note

If Repeater is set to never follow redirects you will need to click Follow redirect to complete the login sequence.

For more information on configuring redirects in Repeater, see Repeater settings - Redirects.

Related pages

Sessions settings

Session handling rule editor

Macro editor

Session handling tracer - Use the session handling tracer to troubleshoot your session handling configuration.
