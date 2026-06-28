# XSS Filters: Beating Length Limits Using Spanned Payloads

Source: https://portswigger.net/support/xss-filters-beating-length-limits-using-spanned-payloads
Fetched: 2026-06-28T09:17:37.567064+00:00

This page may be out of date

We haven't updated it for a while because we're busy working on new, improved content to help you get the

most out of Burp Suite. In the meantime, please note that the information on this page may no longer be

accurate.

Visit our Support Center

XSS Filters: Beating Length Limits Using Spanned Payloads

A powerful technique for beating length limits is to span an attack payload across multiple different locations where user-controllable input is inserted into the same returned page.

The example uses Hackxor, a web application hacking game.

Consider the following form. Clicking the 'Submit data' button returns a page containing the following:

<input type='hidden' id='hash' name='hash' type='text' value=''>

<input name='text' id='text' value='aaaa'>

<input id='img' name='img' type='text' value='bbbb'>

<input id='sound' name='sound' type='text' value='cccc'>

We can see our input reflected. Additionally, the hidden input field hash is reflected in the response.

However, the input fields are restricted to a length limit of 10.

Our payload is being truncated.

Regardless, we can still deliver a working exploit by spanning our payload across the four available input fields. Using JavaScript comments we can make our the browser ignore the chunks of source code that would otherwise separate our payload.

hash=<script>/*&

text=*/alert(1)/*&

img=*///&

sound=%0a%3c%2f%73%63%72%69%70%74%3e&

We have used a single line comment to remove the source code between img and sound inputs. This allows us to use a ten byte payload: ;</script>.

Here we can see our modified payload in the response and the effect of the JavaScript comments on the source code.

Finally, we can reload the page in our browser to confirm that our payload fires.
