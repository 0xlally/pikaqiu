# Bypassing CSP with dangling iframes

Source: https://portswigger.net/research/bypassing-csp-with-dangling-iframes
Fetched: 2026-06-28T09:17:21.736872+00:00

Bypassing CSP with dangling iframes

Gareth Heyes

Researcher

@garethheyes

Published: Tuesday, 14 June 2022 at 14:00 UTC

Updated: Tuesday, 14 June 2022 at 14:00 UTC

Introduction

Our Web Security Academy has a topic on dangling markup injection - a technique for exploiting sites protected by CSP. But something interesting happened when we came to update to Chrome 97 - because one of our interactive labs mysteriously stopped working. When we originally made this lab, Chrome prevented dangling markup-based attacks by looking for raw whitespace followed by "<" characters - but forgot to prevent background attributes (as discovered by Masato Kinugawa).

Unfortunately, from Chrome 97 this technique no longer worked, so I was tasked to try and find an alternative. I tried many different attributes and CSS-based animations to delay assignments to try and bypass this protection. They all failed - it appears the force is strong with Mike West, who authored this change.

I took a step back and analysed the CSP:

default-src 'self';object-src 'none'; style-src 'self'; script-src 'self'; img-src *;

This looks watertight, right (apart from the img-src)? What if I told you that you could remove the 'img-src' directive and yet still conduct a dangling markup attack without a click? Let's see how ...

Cross domain iframe issues

First I fired up the Hackability inspector which is a security-focussed enumerator I coded a while back and began to dissect the inner workings of iframes. The Inspector is convenient for testing multiple domains for cross-domain leaks. I added the first iframe and inside that instance, I added another iframe:

<iframe name=test>

Then from the parent, I inspected the cross domain window with the following input:

x.contentWindow

To my surprise, the Inspector showed the name of the iframe as "test" - what was going on here? Well, the Inspector has a few known properties it tries - with "test" being one of them. But this then means that a cross-domain iframe can discover the iframe name attribute. I did a few tests and it appears that you can't enumerate the iframe for the name of the frame, but you can use typeof to determine if the name exists or not. For example you can ask yes/no questions on the name attribute of any cross-domain iframe:

if(typeof x.contentWindow.myWinName === 'object') {

//window name exists

} else {

//window name doesn't exist

}

This is good, but doesn't really help me bypass the CSP; it's no use trying to brute force a CSRF token asking yes / no questions. Inspecting various properties of the cross-domain iframe, I tried changing the values - changing the location of the iframe to about:blank. To my surprise, even though this was cross-domain, Chrome allowed it:

x.contentWindow[0].location='about:blank'

Not only that, but the full window was able to be enumerated, and I was able to access location.ancesterOrigins - which leaked an external domain. But what I was really interested in was the window.name and if it could be read. Sure enough, the window name was readable and writable - and you could even execute JavaScript regardless of the parent page's CSP. What appears to happen is that when you assign it to about:blank the ownership of the iframe changes to the domain that set it.

Finally, here's the exploit that solved the lab:

<script>

function cspBypass(win) {

win[0].location = 'about:blank';

setTimeout(()=>alert(win[0].name), 500);

}

</script>

<iframe src="//subdomain1.portswigger-labs.net/bypassing-csp-with-dangling-iframes/target.php?email=%22><iframe name=%27" onload="cspBypass(this.contentWindow)"></iframe>

Proof of concept

Conclusion

CSP treats about:blank URLs as the same origin - however when an attacker sets a cross domain iframe to about:blank, it becomes readable by an attacker and is definitely not the same origin. The Chrome mitigations for dangling markup attacks prevent some attacks, but by abusing browser quirks, it's possible to sidestep those mitigations and gain access to cross domain information via an injection - even with JavaScript disabled in your CSP.

Timeline

2022-02-10 08:55 AM GMT - Reported bug to Google

2022-02-10 09:38 AM GMT - Reported to Mozilla

2022-06-14 15:00 PM GMT - Published this post

csp

dangling markup

Back to all articles

Related Research

Using form hijacking to bypass CSP

05 March 2024

Using form hijacking to bypass CSP

Bypassing CSP via DOM clobbering

05 June 2023

Bypassing CSP via DOM clobbering

Ambushed by AngularJS: a hidden CSP bypass in Piwik PRO

28 April 2023

Ambushed by AngularJS: a hidden CSP bypass in Piwik PRO

Stealing passwords from infosec Mastodon - without bypassing CSP

15 November 2022

Stealing passwords from infosec Mastodon - without bypassing CSP
