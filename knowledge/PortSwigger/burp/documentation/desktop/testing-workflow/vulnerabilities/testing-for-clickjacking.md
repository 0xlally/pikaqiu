# Testing for clickjacking

Source: https://portswigger.net/burp/documentation/desktop/testing-workflow/vulnerabilities/testing-for-clickjacking
Fetched: 2026-06-28T09:16:01.655706+00:00

Support Center

Documentation

Desktop editions

Testing workflow

Testing for vulnerabilities

Testing for clickjacking

Professional

Testing for clickjacking

Last updated:

June 18, 2026

Read time:

3 Minutes

Clickjacking is a web security vulnerability that allows an attacker to trick users into clicking on hidden web page elements. It's done by overlaying a disguised or invisible UI layer (usually using iframes) on top of a target web page, fooling users into believing they're clicking something totally different. For example, users may think they're entering a draw to win a luxury cruise but, in reality, they're sending money to an attacker.

Steps

You can follow along with the process below using the Basic clickjacking with CSRF token protection lab from our Web Security Academy.

Scanning for clickjacking vulnerabilities

If you're using Burp Suite Professional, you can use Burp Scanner to test for clickjacking vulnerabilities:

Open your target web page in Burp's browser. In this example, we're going to use the My account page of our fictional blog.

In Proxy > HTTP history, right-click the requests you want to test, then click Do active scan.

When the scan has finished, go to the Dashboard tab and select the scan from the

Tasks list. In the main panel, go to the Issues tab to identify any Frameable response issues that Scanner found.

These indicate that your target web page is vulnerable to clickjacking attacks.

Exploiting clickjacking vulnerabilities

Although you can manually create a clickjacking proof of concept, this can be fairly tedious and time-consuming in practice.

When you're testing for clickjacking, we recommend using Burp's Clickbandit tool instead.

Once you've identified a vulnerable web page with an element that an attacker might target:

Load your target web page in Burp's browser.

In Burp Suite, open the top-level Burp menu, then click Burp Clickbandit. This opens the Burp Clickbandit window.

Click Copy Clickbandit to clipboard. This copies the Clickbandit script.

Return to your target web page in Burp's browser, then paste the Clickbandit script into the Developer Tools Console. The Clickbandit banner appears.

Click Start. This reloads the target web page within a frame, ready for the attack to be performed. Clickbandit is now active in Record mode.

Click all the elements you've identified as potential targets for attackers. Clickbandit records each of your clicks. If you don't want a click to register during this stage, you can Disable click actions using the checkbox on the Clickbandit banner. This is helpful if a click will result in an action you don't want to happen.

Click Finish to end Record mode and enter Review mode. In Review mode, Clickbandit replays your click journey around the target site, with an attack UI overlaid, mimicking a real world clickjacking attack.

Click the attack UI buttons to verify each step of the clickjacking attack. If you need to adjust the attack layer, you can:

Adjust the zoom using + and -.

Toggle transparency (to show or hide the target web page behind the attack layer).

Change the iframe position using the arrow keys on your keyboard.

Reset the attack layer to its original state (removing any changes you've made to its zoom or position).

(Optional) Click Save to download the attack script as an HTML file.

Related pages

Burp Clickbandit

Clickjacking (UI redressing)
