# When good XSRF defence turns bad

Source: https://portswigger.net/blog/when-good-xsrf-defence-turns-bad
Fetched: 2026-06-28T09:15:28.419370+00:00

When good XSRF defence turns bad

Dafydd Stuttard |

Sunday, 6 January 2008 at 11:44 UTC

xsrf

Talk about cross-site request forgery bugs seems to be in vogue, with various explanations of what the vulnerability is, and how to avoid it. As awareness has increased, and more developers attempt to defend against XSRF, it is not uncommon to find cases where someone has followed a standard piece of advice, but achieves nothing in terms of preventing attacks.

An application is vulnerable to XSRF if an "important" user action is performed using requests all of whose non-cookie parameters can be determined in advance by an attacker. For example, in a banking application a user might perform a funds transfer using the following request:

POST /TransferFunds.asp HTTP/1.0

Host: mybank.com

Content-Length: 48

Cookie: sessid=191r309ru13d10219029r31r90f1re029e

FromAccount=current&ToSortCode=123456&

ToAccountNumber=12345678&Amount=1000.00&When=now

An attacker wishing to induce a victim to transfer funds to his account can forge a request containing all of the necessary parameters with the exception of the cookie containing the session token. If this request is initiated from a web site the attacker controls, at a time when the user is logged in to the banking application, then the user's browser will automatically add the cookie parameter, and so the funds transfer will be carried out.

Now, a common recommendation for preventing XSRF attacks is that "important" actions like funds transfers should be implemented in two steps. In response to the first request, the application sends a nonce (an unpredictable value) to the client, which is submitted as a parameter in the second request. The application verifies the nonce in the second request, and only performs the action if this is valid.

The thought behind this defence is that the two-step approach confirms that the action originated from an authentic user, and not from a third-party web site. Although code running in an attacker's web page can initiate requests to the bank, the browser's same origin policy prevents it from accessing the bank's responses, and so the attacker's code will be unable to retrieve the nonce required for the second request. However, given the vague way in which the defence is often characterised, a developer who isn't thinking for themselves may be forgiven for getting it wrong.

I recently came across an application which had previously been full of XSRF flaws. Developers had reimplemented numerous functions using two steps, by issuing and validating a nonce. However, to enhance usability, the second step was implemented as an HTTP redirect. So the preceding request returned a response like the following:

HTTP/1.0 302 Object Moved

Location: /TransferFunds2.asp?nonce=120491746317280

The user's browser follows the redirect, thereby submitting the nonce (together with the user's session cookie), which is validated by the server. But the defence achieves nothing, because the user's browser behaves in just the same way if the first request originated from a third-party web site. The fact that the same origin policy prevents the attacker's code from accessing the bank's responses is irrelevant because it does not need to - it just relies upon the browser to process and resubmit the nonce in the normal way. A lot of development time had been wasted.

For the nonce-based defence to be effective, the request in which the nonce is resubmitted must result from some informed user interaction. For example, instead of performing a redirect, the first response could display the details of the proposed transfer, with the nonce in a hidden form field, which is submitted using "confirm" or "cancel" buttons. Because code on the attacker's web page cannot access this response, it cannot parse out the nonce and resubmit it. If performing actions over two stages is undesirable for usability reasons, then the nonce can be placed into the original form used to initiate the action. Provided the application properly ties the nonce to the session in which it was issued, then (in the absence of another vulnerability) an attacker will be unable to determine all of the necessary parameters to the original request, and so the main prerequisite for an XSRF attack to get going is not fulfilled.

xsrf

Dafydd Stuttard

@DafyddStuttard

Latest Posts

Burp Extensibility 2026: Awards, Talks, and Highlights

19 June 2026

Burp Extensibility 2026: Awards, Talks, and Highlights

The beast needs a cage: What's next for AppSec post-Mythos

12 May 2026

The beast needs a cage: What's next for AppSec post-Mythos

3 ways custom scan checks turn practitioner knowledge into scalable automation

01 May 2026

3 ways custom scan checks turn practitioner knowledge into scalable automation

Senior pentesters have a deeply refined intuition about what is vulnerable in an environment. The problem? That expertise is often siloed with an individual and trapped in their notes or Python scripts.
