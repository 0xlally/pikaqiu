# On-site request forgery

Source: https://portswigger.net/blog/on-site-request-forgery
Fetched: 2026-06-28T09:15:22.385647+00:00

On-site request forgery

Dafydd Stuttard |

Thursday, 3 May 2007 at 08:09 UTC

xsrf

XSS

Request forgery is a familiar attack payload for exploiting stored XSS vulnerabilities. In the MySpace worm, Samy placed a script within his profile which caused any user viewing the profile to perform various unwitting actions, including adding Samy as a friend and copying his script into their own profile. In many XSS scenarios, when you simply wish to perform a particular action with different privileges, on-site request forgery is easier and more reliable than attempting to hijack a victim’s session.

What is less well appreciated is that stored on-site request forgery bugs can exist when XSS is not possible. Consider a message board application which lets users submit items that are viewed by other users. Messages are submitted using a request like the following:

POST /submit.php

Content-Length: 34

type=question&name=daf&message=foo

which results in the following being added to the messages page:

<tr>

<td><img src="/images/question.gif"></td>

<td>daf</td>

<td>foo</td>

</tr>

In this situation, you would of course test for XSS. However, it turns out that the application is properly HTML-encoding any " < and > characters which it inserts into the page. Having satisfied yourself that this defence cannot be bypassed in any way, you might move on to the next test.

But look again. We control part of the target of the <img> tag. Although we can’t break out of the quoted string, we can modify the URL to cause any user who views our message to make an arbitrary on-site GET request. For example, submitting the following value in the type parameter will cause anyone viewing our message to make a request which attempts to add a new administrative user:

../admin/newUser.php?username=daf2&password=0wned &role=admin#

When an ordinary user is induced to issue our crafted request, it will of course fail. But when an administrator views our message, our backdoor account gets created. We have performed a successful on-site request forgery attack even though XSS is not possible. And of course, the attack will succeed even if administrators take the precaution of disabling JavaScript.

(In the above attack string, note the # character which effectively terminates the URL before the .gif suffix. We could just as easily use & to incorporate the suffix as a further request parameter.)

xsrf

XSS

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
