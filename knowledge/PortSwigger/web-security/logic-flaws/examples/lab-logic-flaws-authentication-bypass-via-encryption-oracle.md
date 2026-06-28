# Lab: Authentication bypass via encryption oracle

Source: https://portswigger.net/web-security/logic-flaws/examples/lab-logic-flaws-authentication-bypass-via-encryption-oracle
Fetched: 2026-06-28T09:17:59.385457+00:00

Web Security Academy

Business logic vulnerabilities

Examples

Lab

Lab: Authentication bypass via encryption oracle

This lab contains a logic flaw that exposes an encryption oracle to users. To solve the lab, exploit this flaw to gain access to the admin panel and delete the user carlos.

You can log in to your own account using the following credentials: wiener:peter

Solution

Log in with the "Stay logged in" option enabled and post a comment. Study the corresponding requests and responses using Burp's manual testing tools. Observe that the stay-logged-in cookie is encrypted.

Notice that when you try and submit a comment using an invalid email address, the response sets an encrypted notification cookie before redirecting you to the blog post.

Notice that the error message reflects your input from the email parameter in cleartext:

Invalid email address: your-invalid-email

Deduce that this must be decrypted from the notification cookie. Send the POST /post/comment and the subsequent GET /post?postId=x request (containing the notification cookie) to Burp Repeater.

In Repeater, observe that you can use the email parameter of the POST request to encrypt arbitrary data and reflect the corresponding ciphertext in the Set-Cookie header. Likewise, you can use the notification cookie in the GET request to decrypt arbitrary ciphertext and reflect the output in the error message. For simplicity, double-click the tab for each request and rename the tabs encrypt and decrypt respectively.

In the decrypt request, copy your stay-logged-in cookie and paste it into the notification cookie. Send the request. Instead of the error message, the response now contains the decrypted stay-logged-in cookie, for example:

wiener:1598530205184

This reveals that the cookie should be in the format username:timestamp. Copy the timestamp to your clipboard.

Go to the encrypt request and change the email parameter to administrator:your-timestamp. Send the request and then copy the new notification cookie from the response.

Decrypt this new cookie and observe that the 23-character "Invalid email address: " prefix is automatically added to any value you pass in using the email parameter. Send the notification cookie to Burp Decoder.

In Decoder, URL-decode and Base64-decode the cookie.

In Burp Repeater, switch to the message editor's "Hex" tab. Select the first 23 bytes, then right-click and select "Delete selected bytes".

Re-encode the data and copy the result into the notification cookie of the decrypt request. When you send the request, observe that an error message indicates that a block-based encryption algorithm is used and that the input length must be a multiple of 16. You need to pad the "Invalid email address: " prefix with enough bytes so that the number of bytes you will remove is a multiple of 16.

In Burp Repeater, go back to the encrypt request and add 9 characters to the start of the intended cookie value, for example:

xxxxxxxxxadministrator:your-timestamp

Encrypt this input and use the decrypt request to test that it can be successfully decrypted.

Send the new ciphertext to Decoder, then URL and Base64-decode it. This time, delete 32 bytes from the start of the data. Re-encode the data and paste it into the notification parameter in the decrypt request. Check the response to confirm that your input was successfully decrypted and, crucially, no longer contains the "Invalid email address: " prefix. You should only see administrator:your-timestamp.

From the proxy history, send the GET / request to Burp Repeater. Delete the session cookie entirely, and replace the stay-logged-in cookie with the ciphertext of your self-made cookie. Send the request. Observe that you are now logged in as the administrator and have access to the admin panel.

Using Burp Repeater, browse to /admin and notice the option for deleting users. Browse to /admin/delete?username=carlos to solve the lab.

Community solutions

Michael Sommer

Find business logic vulnerabilities using Burp Suite

Try for free
