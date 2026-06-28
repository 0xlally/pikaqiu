# Lab: Reflected XSS with AngularJS sandbox escape without strings

Source: https://portswigger.net/web-security/cross-site-scripting/contexts/client-side-template-injection/lab-angular-sandbox-escape-without-strings
Fetched: 2026-06-28T09:17:43.797625+00:00

Web Security Academy

Cross-site scripting

Contexts

Client-side template injection

Lab

Lab: Reflected XSS with AngularJS sandbox escape without strings

This lab uses AngularJS in an unusual way where the $eval function is not available and you will be unable to use any strings in AngularJS.

To solve the lab, perform a cross-site scripting attack that escapes the sandbox and executes the alert function without using the $eval function.

Solution

Visit the following URL, replacing YOUR-LAB-ID with your lab ID:

https://YOUR-LAB-ID.web-security-academy.net/?search=1&toString().constructor.prototype.charAt%3d[].join;[1]|orderBy:toString().constructor.fromCharCode(120,61,97,108,101,114,116,40,49,41)=1

The exploit uses toString() to create a string without using quotes. It then gets the String prototype and overwrites the charAt function for every string. This effectively breaks the AngularJS sandbox. Next, an array is passed to the orderBy filter. We then set the argument for the filter by again using toString() to create a string and the String constructor property. Finally, we use the fromCharCode method generate our payload by converting character codes into the string x=alert(1). Because the charAt function has been overwritten, AngularJS will allow this code where normally it would not.

Community solutions

Michael Sommer

Find XSS vulnerabilities using Burp Suite

Try for free
