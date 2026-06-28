# Using Burp to find Clickjacking Vulnerabilities

Source: https://portswigger.net/support/using-burp-to-find-clickjacking-vulnerabilities
Fetched: 2026-06-28T09:17:36.309473+00:00

This page may be out of date

We haven't updated it for a while because we're busy working on new, improved content to help you get the

most out of Burp Suite. In the meantime, please note that the information on this page may no longer be

accurate.

Visit our Support Center

Using Burp to find Clickjacking Vulnerabilities

Clickjacking is a technique in which an attacker uses multiple transparent or opaque layers to trick a user into clicking on a button or link on another page when they were intending to click on the top level page. Thus, the attacker is "hijacking" clicks meant for their page and routing them to another page, most likely owned by another application, domain, or both.

Manually crafting a proof of concept attack can mean laborious hours of offset-tweaking. However, you can use Burp Clickbandit, a point-and-click tool for generating clickjacking attacks, to expedite the process. When you have found a web page that may be vulnerable to clickjacking, you can use Burp Clickbandit to quickly craft an attack, to prove that the vulnerability can be successfully exploited.

Detecting Frameable Response (Potential Clickjacking)

If a page fails to set an appropriate X-Frame-Options or Content-Security-Policy HTTP header, it might be possible for a page controlled by an attacker to load it within an iframe. This may enable a clickjacking attack, in which the attacker's page overlays the target application's interface with a different interface provided by the attacker.

Burp Scanner passively checks for this potential security flaw.

If the application you are testing is potentially susceptible to Clickjacking, an informational issue will be reported in the Target site map.

Clickjacking POC: Burp Clickbandit

Burp Clickbandit runs in your browser using JavaScript. It works on all modern browsers except for Internet Explorer and Microsoft Edge. To run Clickbandit, use the following steps.

In Burp, go to the Burp menu and select "Burp Clickbandit".

On the dialog that opens, click the "Copy Clickbandit to clipboard" button. This will copy the Clickbandit script to your clipboard.

In your browser, visit the web page that you want to test, in the usual way.

In your browser, open the web developer console. This might also be called "developer tools" or "JavaScript console".

Paste the Clickbandit script into the web developer console, and press enter.

The Burp Clickbandit banner will appear at the top of the browser window and the original page will be reloaded within a frame, ready for the attack to be performed.

Note: If you want to prevent the actions that your clicks will perform being executed during recording, use the "disable click actions" checkbox.

Then simply execute the sequence of clicks you want your victim to perform.

In this example, we are deleting an account. We click the delete button, then click "OK" in the pop up box.

When you've finished recording, click the "finish" button. This will then display your attack for review.

In this view you can adjust the zoom factor using the plus and minus buttons, toggle transparency allowing you to see the site underneath the button and also change the iframe position using the arrow keys.

Reset allows you to restore the original attack removing any modifications you may have made to the zoom factor or position.

Click the "save" button to download your proof-of-concept attack and save it locally.

When the clickjacking attack is complete (after the victim has clicked the last link) the message "you've been clickjacked" appears.

You can alter this message in the code to suit your needs.
