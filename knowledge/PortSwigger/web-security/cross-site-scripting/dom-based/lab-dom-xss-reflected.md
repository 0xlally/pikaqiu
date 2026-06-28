# Lab: Reflected DOM XSS

Source: https://portswigger.net/web-security/cross-site-scripting/dom-based/lab-dom-xss-reflected
Fetched: 2026-06-28T09:17:45.136578+00:00

Web Security Academy

Cross-site scripting

DOM-based

Lab

Lab: Reflected DOM XSS

This lab demonstrates a reflected DOM vulnerability. Reflected DOM vulnerabilities occur when the server-side application processes data from a request and echoes the data in the response. A script on the page then processes the reflected data in an unsafe way, ultimately writing it to a dangerous sink.

To solve this lab, create an injection that calls the alert() function.

Solution

In Burp Suite, go to the Proxy tool and make sure that the Intercept feature is switched on.

Back in the lab, go to the target website and use the search bar to search for a random test string, such as "XSS".

Return to the Proxy tool in Burp Suite and forward the request.

On the Intercept tab, notice that the string is reflected in a JSON response called search-results.

From the Site Map, open the searchResults.js file and notice that the JSON response is used with an eval() function call.

By experimenting with different search strings, you can identify that the JSON response is escaping quotation marks. However, backslash is not being escaped.

To solve this lab, enter the following search term:

\"-alert(1)}//

As you have injected a backslash and the site isn't escaping them, when the JSON response attempts to escape the opening double-quotes character, it adds a second backslash. The resulting double-backslash causes the escaping to be effectively canceled out. This means that the double-quotes are processed unescaped, which closes the string that should contain the search term.

An arithmetic operator (in this case the subtraction operator) is then used to separate the expressions before the alert() function is called. Finally, a closing curly bracket and two forward slashes close the JSON object early and comment out what would have been the rest of the object. As a result, the response is generated as follows:

{"searchTerm":"\\"-alert(1)}//", "results":[]}

Community solutions

z3nsh3ll

Michael Sommer

Find XSS vulnerabilities using Burp Suite

Try for free
