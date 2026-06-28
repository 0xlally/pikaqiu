# Lab: Reflected XSS with AngularJS sandbox escape and CSP

Source: https://portswigger.net/web-security/cross-site-scripting/contexts/client-side-template-injection/lab-angular-sandbox-escape-and-csp
Fetched: 2026-06-28T09:17:43.809941+00:00

Web Security Academy

Cross-site scripting

Contexts

Client-side template injection

Lab

Lab: Reflected XSS with AngularJS sandbox escape and CSP

This lab uses CSP and AngularJS.

To solve the lab, perform a cross-site scripting attack that bypasses CSP, escapes the AngularJS sandbox, and alerts document.cookie.

Solution

Go to the exploit server and paste the following code, replacing YOUR-LAB-ID with your lab ID:

<script>

location='https://YOUR-LAB-ID.web-security-academy.net/?search=%3Cinput%20id=x%20ng-focus=$event.composedPath()|orderBy:%27(z=alert)(document.cookie)%27%3E#x';

</script>

Click "Store" and "Deliver exploit to victim".

The exploit uses the ng-focus event in AngularJS to create a focus event that bypasses CSP. It also uses $event, which is an AngularJS variable that references the event object. The path property is specific to Chrome and contains an array of elements that triggered the event. The last element in the array contains the window object.

Normally, | is a bitwise or operation in JavaScript, but in AngularJS it indicates a filter operation, in this case the orderBy filter. The colon signifies an argument that is being sent to the filter. In the argument, instead of calling the alert function directly, we assign it to the variable z. The function will only be called when the orderBy operation reaches the window object in the $event.path array. This means it can be called in the scope of the window without an explicit reference to the window object, effectively bypassing AngularJS's window check.

Community solutions

Michael Sommer

Find XSS vulnerabilities using Burp Suite

Try for free
