# Abusing jQuery for CSS powered timing attacks

Source: https://portswigger.net/research/abusing-jquery-for-css-powered-timing-attacks
Fetched: 2026-06-28T09:17:20.004368+00:00

Abusing jQuery for CSS powered timing attacks

Gareth Heyes

Researcher

@garethheyes

Published: Wednesday, 22 May 2019 at 13:15 UTC

Updated: Wednesday, 29 May 2019 at 12:10 UTC

Arthur Saftnes did some quite awesome research last year on timing attacks with jQuery CSS selectors, in fact it was probably my favourite blog post from last year.

It's a common design pattern for websites to pass location.hash to the jQuery $ function:

$(location.hash);

The hash may be attacker controlled, and this used to cause XSS, but jQuery patched that many years ago. Arthur found that this pattern can still theoretically be exploited using a timing attack. You can repeatedly invoke  jQuery's :has selector and measure the performance impact to infer content from the target page. This turns these situations from unexploitable XSS into reading pretty much any input value.

I decided to follow up on this research to find real world vulnerabilities using this technique. I first modified Burp's dynamic analysis to look for jQuery selectors being executed inside hashchange events, and scanned a bunch of websites. The reason I was looking for hashchange events is a limitation of the attack; in order to measure the performance impact you need to repeatedly change the hash to run a binary search of all possible characters which is only possible when a hashchange event fires. Another limitation of the original technique posted was the fact that you need the site to URL decode the hash as most modern browsers now URL encode it - but I found a way around this.

I found a few bug bounty sites that did use location.hash with the jQuery $ function inside a hashchange event, but most of the sites found didn't really have any interesting data to steal. There was one exception though, Red Hat was using a jQuery selector inside a hashchange event and had account functionality. Looking at the site it didn't have any inputs to steal data from but it did display your full name when logged on. Arthur's original attack used CSS attribute selectors but the full name was not inside any input element so I couldn't use them.

I looked through all the jQuery CSS selectors and found the :contains selector which finds elements that contain the string specified. Unfortunately :contains doesn't allow you to look at the start or end of the string so I needed another way of extracting the value. I thought about using the space as an anchor point to extract the first name but the problem is that on Firefox the space will be URL encoded. Fortunately, backslash isn't URL encoded so I could use CSS hex escapes. At first I tried \20 but this would break the selector because the next character would continue the hex escape, but if I padded the escape with zeros this would ensure the correct CSS escape would be used.  I modified Arthur's code to improve the make_selector function to use spaces:

function make_selector(prefix, characters, firstNameFlag, firstName) {

return characters.split("").map(c => !firstNameFlag ? SLOW_SELECTOR +

SELECTOR_TEMPLATE.replace('{}', c + prefix + '\\000020') : SLOW_SELECTOR +

SELECTOR_TEMPLATE.replace("{}", prefix.replace(/ /, '\\000020') + c))

.join(",");

}

The code above uses the hex encoded space to scan for the name backwards. I use the firstNameFlag to decide if it's the first name or the second name, when the uppercase letter is found of the first name the flag is set and then it starts matching the second name scanning forwards but this time using the first name as the prefix and space.

if(!firstNameFlag && /[A-Z]/.test(name)) {

firstNameFlag = true;

name += ' ';

backtracks = 0;

continue;

}

The other problem I encountered was the fact you can't use a space in the actual selector because it gets URL encoded, and hex escapes won't work here. I spent a lot of time trying to construct a selector that didn't have spaces and still had a measurable performance impact. Finally I came up with the following selector:

const SLOW_SELECTOR="*:has(*:has(*):parent:has(*):parent:has(*):parent:has(*):parent:has(*)):parent:has(";

const SELECTOR_TEMPLATE=".account-user:contains('{}'))";

This causes a performance impact but is much slower than using spaces with the CSS descendant selector. Then my next issue was how to determine that you've reached the end of the name. Like I said before the :contains selector offers no way of looking at the end of the string. So the only way I came up with was to look for 6 backtracks in a row.

The vulnerability has now been fixed but I'll share the original PoC below so you can see the code I used:

Firefox access.redhat.com jQuery selector PoC

I also recorded a video so you can see it in action:

Video tags are not supported by your browser.

XSS

Back to all articles

Related Research

Cookie Chaos: How to bypass __Host and __Secure cookie prefixes

03 September 2025

Cookie Chaos: How to bypass __Host and __Secure cookie prefixes

Stealing HttpOnly cookies with the cookie sandwich technique

22 January 2025

Stealing HttpOnly cookies with the cookie sandwich technique

Bypassing WAFs with the phantom $Version cookie

04 December 2024

Bypassing WAFs with the phantom $Version cookie

Concealing payloads in URL credentials

23 October 2024

Concealing payloads in URL credentials
