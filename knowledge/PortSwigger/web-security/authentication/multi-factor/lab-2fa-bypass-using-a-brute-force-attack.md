# Lab: 2FA bypass using a brute-force attack

Source: https://portswigger.net/web-security/authentication/multi-factor/lab-2fa-bypass-using-a-brute-force-attack
Fetched: 2026-06-28T09:17:40.592983+00:00

Web Security Academy

Authentication vulnerabilities

Multi-factor

Lab

Lab: 2FA bypass using a brute-force attack

This lab's two-factor authentication is vulnerable to brute-forcing. You have already obtained a valid username and password, but do not have access to the user's 2FA verification code. To solve the lab, brute-force the 2FA code and access Carlos's account page.

Victim's credentials: carlos:montoya

Note

As the verification code will reset while you're running your attack, you may need to repeat this attack several times before you succeed. This is because the new code may be a number that your current Intruder attack has already attempted.

Hint

You will need to use Burp macros in conjunction with Burp Intruder to solve this lab. For more information about macros, please refer to the Burp Suite documentation. Users proficient in Python might prefer to use the Turbo Intruder extension, which is available from the BApp store.

Solution

With Burp running, log in as carlos and investigate the 2FA verification process. Notice that if you enter the wrong code twice, you will be logged out again. You need to use Burp's session handling features to log back in automatically before sending each request.

In Burp, click Settings to open the Settings dialog, then click Sessions. In the Session Handling Rules panel, click Add. The Session handling rule editor dialog opens.

In the dialog, go to the Scope tab. Under URL Scope, select the option Include all URLs.

Go back to the Details tab and under Rule Actions, click Add > Run a macro.

Under Select macro click Add to open the Macro Recorder. Select the following 3 requests:

GET /login

POST /login

GET /login2

Then click OK. The Macro Editor dialog opens.

Click Test macro and check that the final response contains the page asking you to provide the 4-digit security code. This confirms that the macro is working correctly.

Keep clicking OK to close the various dialogs until you get back to the main Burp window. The macro will now automatically log you back in as Carlos before each request is sent by Burp Intruder.

Send the POST /login2 request to Burp Intruder.

In Burp Intruder, add a payload position to the mfa-code parameter.

In the Payloads side panel, select the Numbers payload type. Enter the range 0 - 9999 and set the step to 1. Set the min/max integer digits to 4 and max fraction digits to 0. This will create a payload for every possible 4-digit integer.

Click on Resource pool to open the Resource

pool side panel. Add the attack to a resource pool with the Maximum concurrent requests set to 1.

Start the attack. Eventually, one of the requests will return a 302 status code. Right-click on this request and select Show response in browser. Copy the URL and load it in the browser.

Click My account to solve the lab.

Community solutions

Rana Khalil

Michael Sommer

Find vulnerabilities in your authentication using Burp Suite

Try for free
