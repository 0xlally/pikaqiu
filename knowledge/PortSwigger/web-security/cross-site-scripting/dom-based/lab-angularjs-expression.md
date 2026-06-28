# Lab: DOM XSS in AngularJS expression with angle brackets and double quotes HTML-encoded

Source: https://portswigger.net/web-security/cross-site-scripting/dom-based/lab-angularjs-expression
Fetched: 2026-06-28T09:17:45.044893+00:00

Web Security Academy

Cross-site scripting

DOM-based

Lab

Lab: DOM XSS in AngularJS expression with angle brackets and double quotes HTML-encoded

This lab contains a DOM-based cross-site scripting vulnerability in a AngularJS expression within the search functionality.

AngularJS is a popular JavaScript library, which scans the contents of HTML nodes containing the ng-app attribute (also known as an AngularJS directive). When a directive is added to the HTML code, you can execute JavaScript expressions within double curly braces. This technique is useful when angle brackets are being encoded.

To solve this lab, perform a cross-site scripting attack that executes an AngularJS expression and calls the alert function.

Solution

Enter a random alphanumeric string into the search box.

View the page source and observe that your random string is enclosed in an ng-app directive.

Enter the following AngularJS expression in the search box:

{{$on.constructor('alert(1)')()}}

Click search.

Community solutions

Jarno Timmermans

z3nsh3ll

Michael Sommer

Find XSS vulnerabilities using Burp Suite

Try for free
