# Lab: Reflected XSS with some SVG markup allowed

Source: https://portswigger.net/web-security/cross-site-scripting/contexts/lab-some-svg-markup-allowed
Fetched: 2026-06-28T09:17:44.854829+00:00

Web Security Academy

Cross-site scripting

Contexts

Lab

Lab: Reflected XSS with some SVG markup allowed

This lab has a simple reflected XSS vulnerability. The site is blocking common tags but misses some SVG tags and events.

To solve the lab, perform a cross-site scripting attack that calls the alert() function.

Solution

Inject a standard XSS payload, such as:

<img src=1 onerror=alert(1)>

Observe that this payload gets blocked. In the next few steps, we'll use Burp Intruder to test which tags and attributes are being blocked.

Open Burp's browser and use the search function in the lab. Send the resulting request to Burp Intruder.

In the request template, replace the value of the search term with: <>

Place the cursor between the angle brackets and click Add § to create a payload position. The value of the search term should now be: <§§>

Visit the XSS cheat sheet and click Copy tags to clipboard.

In Burp Intruder, in the Payloads side panel, click Paste to paste the list of tags into the payloads list. Click Start attack.

When the attack is finished, review the results. Observe that all payloads caused a 400 response, except for the ones using the <svg>, <animatetransform>, <title>, and <image> tags, which received a 200 response.

Go back to the Intruder tab and replace your search term with:

<svg><animatetransform%20=1>

Place the cursor before the = character and click Add § to create a payload position. The value of the search term should now be:

<svg><animatetransform%20§§=1>

Visit the XSS cheat sheet and click Copy events to clipboard.

In Burp Intruder, in the Payloads side panel, click Clear to remove the previous payloads. Then click

Paste to paste the list of attributes into the payloads list. Click Start attack.

When the attack is finished, review the results. Note that all payloads caused a 400 response, except for the onbegin payload, which caused a

200 response.

Visit the following URL in the browser to confirm that the alert() function is called and the lab is solved:

https://YOUR-LAB-ID.web-security-academy.net/?search=%22%3E%3Csvg%3E%3Canimatetransform%20onbegin=alert(1)%3E

Community solutions

z3nsh3ll

Intigriti

Michael Sommer

Find XSS vulnerabilities using Burp Suite

Try for free
