# Generating a CSRF proof-of-concept with Burp Suite

Source: https://portswigger.net/burp/documentation/desktop/testing-workflow/vulnerabilities/session-management/csrf-poc
Fetched: 2026-06-28T09:16:00.778319+00:00

Support Center

Documentation

Desktop editions

Testing workflow

Testing for vulnerabilities

Testing session management mechanisms

Generating a CSRF proof-of-concept

Professional

Generating a CSRF proof-of-concept with Burp Suite

Last updated:

June 18, 2026

Read time:

2 Minutes

Cross-site request forgery (CSRF) attacks force a victim user to perform unintended actions on a website. If a website is vulnerable to CSRF, an attacker can bypass the same-origin policy, which usually prevents websites from interfering with each other. This means the attacker can create a web page that causes the victim user's browser to submit a request directly to the vulnerable website.

You can use Burp Suite Professional to automatically generate HTML for a proof-of-concept (PoC) CSRF attack. This is much quicker and easier than manually creating the HTML, which can be particularly cumbersome when the request contains a larger number of parameters.

Steps

You can follow along with the process below using our lab: CSRF vulnerability with no defenses.

To generate a CSRF proof-of-concept:

Identify a request that you think may be vulnerable to CSRF. You can use Burp Scanner to identify

requests that are potentially vulnerable.

Right-click the request and select Engagement tools > Generate CSRF PoC. A dialog opens with HTML based on the selected request.

In the HTML, edit the value in the fields you want to change in the PoC attack. For example, the

email value in the change email request.

Click Copy HTML to copy the HTML to your clipboard.

Paste the HTML into a web page. If you're using the lab, paste the HTML into the exploit server instead.

View the web page in a browser that is logged into the vulnerable website.

Review the response in your browser and Burp's HTTP history to see whether the desired action occurred. In this example, the user's email address is successfully updated.

To verify the vulnerability, log into the application with a different account. Repeat the attack with the same HTML. A successful attack confirms that the application is vulnerable to CSRF.

Related pages

Academy: Cross-site request forgery (CSRF)

Generate CSRF PoC
