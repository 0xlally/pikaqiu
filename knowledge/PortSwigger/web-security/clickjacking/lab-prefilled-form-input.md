# Lab: Clickjacking with form input data prefilled from a URL parameter

Source: https://portswigger.net/web-security/clickjacking/lab-prefilled-form-input
Fetched: 2026-06-28T09:17:42.944235+00:00

Web Security Academy

Clickjacking

Lab

Lab: Clickjacking with form input data prefilled from a URL parameter

This lab extends the basic clickjacking example in Lab: Basic clickjacking with CSRF token protection. The goal of the lab is to change the email address of the user by prepopulating a form using a URL parameter and enticing the user to inadvertently click on an "Update email" button.

To solve the lab, craft some HTML that frames the account page and fools the user into updating their email address by clicking on a "Click me" decoy. The lab is solved when the email address is changed.

You can log in to your own account using the following credentials: wiener:peter

Note

The victim will be using Chrome so test your exploit on that browser.

Hint

You cannot register an email address that is already taken by another user. If you change your own email address while testing your exploit, make sure you use a different email address for the final exploit you deliver to the victim.

Solution

Log in to the account on the target website.

Go to the exploit server and paste the following HTML template into the "Body" section:

<style>

iframe {

position:relative;

width:$width_value;

height: $height_value;

opacity: $opacity;

z-index: 2;

}

div {

position:absolute;

top:$top_value;

left:$side_value;

z-index: 1;

}

</style>

<div>Test me</div>

<iframe src="YOUR-LAB-ID.web-security-academy.net/my-account?email=hacker@attacker-website.com"></iframe>

Make the following adjustments to the template:

Replace YOUR-LAB-ID with your unique lab ID so that the URL points to the target website's user account page, which contains the "Update email" form.

Substitute suitable pixel values for the $height_value and $width_value variables of the iframe (we suggest 700px and 500px respectively).

Substitute suitable pixel values for the $top_value and $side_value variables of the decoy web content so that the "Update email" button and the "Test me" decoy action align (we suggest 400px and 80px respectively).

Set the opacity value $opacity to ensure that the target iframe is transparent. Initially, use an opacity of 0.1 so that you can align the iframe actions and adjust the position values as necessary. For the submitted attack a value of 0.0001 will work.

Click Store and then View exploit.

Hover over "Test me" and ensure the cursor changes to a hand indicating that the div element is positioned correctly. If not, adjust the position of the div element by modifying the top and left properties of the style sheet.

Once you have the div element lined up correctly, change "Test me" to "Click me" and click Store.

Change the email address in your exploit so that it doesn't match your own.

Deliver the exploit to the victim to solve the lab.

Find clickjacking vulnerabilities using Burp Suite

Try for free
