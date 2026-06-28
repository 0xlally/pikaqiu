# Introducing DOM Invader: DOM XSS just got a whole lot easier to find

Source: https://portswigger.net/blog/introducing-dom-invader
Fetched: 2026-06-28T09:15:18.416335+00:00

Introducing DOM Invader: DOM XSS just got a whole lot easier to find

Gareth Heyes |

Wednesday, 30 June 2021 at 16:47 UTC

XSS

DOM

Hacking Tools

Of the three main types of XSS, DOM-based XSS is by far the most difficult to find and exploit. But we come bearing good news! PortSwigger just released a new tool for Burp Suite Professional and Burp Suite Community Edition that's going to make testing for DOM XSS much easier - and we think you're going to like it. Meet: DOM Invader.

We've created a YouTube video to show you how to use DOM Invader and solve an Academy lab:

Background

Most modern sites use multiple JavaScript libraries - and have many lines of complex, minified code. This makes testing for DOM XSS a real headache. PortSwigger Research has specifically developed DOM Invader to make this process much easier.

"The Augmented DOM allows you to find DOM XSS as if it were reflected XSS."

Through its Augmented DOM, DOM Invader will provide you with a convenient tree view of all of your target's sources and sinks. This greatly simplifies the task of hunting for DOM XSS, and will be big news for the bug bounty hunting and pentest communities.

So, without further ado, let's take a closer look at DOM Invader and what it can do:

DOM Invader's Augmented DOM provides a convenient tree view of an application's sources and sinks.

How to get started with DOM Invader

DOM Invader is a completely new Burp Suite tool, implemented as an extension in the embedded browser. Simply update your version of Burp Suite Professional or Burp Suite Community Edition to 2021.7 on the Early Adopter channel to start using it. View the latest release notes.

By default, DOM Invader is turned off (because it alters site behavior). Turn it on by clicking the icon in the top right hand corner of Burp Suite's embedded browser.

DOM Invader lives in Burp Suite's embedded browser.

DOM Invader instruments your target's DOM, intercepting any JavaScript sources and sinks it might come across, and organizing them ready for you to play with. A "source" could be any JavaScript object that allows user-controlled input (for example: location.search), while a "sink" is any function or setter that allows JavaScript/HTML execution. One notorious example of a sink is the eval function.

"Helpfully, DOM Invader orders sinks so that the most interesting ones appear first."

With DOM Invader, we're going to be working a lot with canaries. A canary is a unique string that's used to see where your user input is reflected inside a sink. By default, DOM Invader uses a random canary, but you can customize this value to whatever you like.

How DOM Invader works

We're not going to go into a full demo of how to use DOM Invader here (please see the documentation for that), but as a broad overview, you're going to be spending a lot of your time using the tool in the Augmented DOM. The Augmented DOM will show you all the sources and sinks contained within your target, and allows you to find DOM XSS as if it were reflected XSS - by inspecting the value sent to the sink.

Essentially, you'll load up the site you want to test, and insert your canary into a query parameter or other such source. Opening DevTools in Burp Suite's embedded browser, you'll be able to click on a new "Augmented DOM" tab - which will show you any sources and sinks containing the canary value - as well as a tree view of all the sources and sinks available. Helpfully, DOM Invader orders sinks so that the most interesting ones appear first.

DOM Invader will order lists of sinks with the most interesting ones appearing first.

When you find an interesting sink, DOM Invader will allow you to see the value contained in it, as well as a stack trace. It'll even highlight your canary for you. At this point, you might like to add some extra characters to your canary in the URL parameter or another source. You can then check the canary value in the Augmented DOM to see if those characters have been correctly encoded.

Canaries are automatically highlighted by DOM Invader.

Other useful features include the ability to search values sent to a sink, as well as automatically injecting canaries into URL parameters and form elements.

View the full documentation for DOM Invader.

Web messages in DOM Invader

When testing sites, we've always found it cumbersome to test for web-message vulnerabilities. Sure, you can add event listeners and breakpoints in Chrome - but there's no easy way to edit them without going to the effort of writing some JavaScript code. PortSwigger could hardly let this situation stand! So DOM Invader is set up to help you test for web-message vulnerabilities.

"DOM Invader is capable of manipulating web messages and spoofing their origin automatically, if you so wish."

DOM Invader lets you see web messages and easily reissue them in its Postmessage tab. Again, we won't go into full details here (please see the documentation for that), but to access this functionality, just click on DOM Invader's icon in the embedded browser, and turn on "Postmessage interception".

Through the Postmessage tab, you'll be able to see a bunch of useful information about any web messages your target sends. This includes their type (e.g. JSON string/JavaScript object), origin, actual data sent, and the location in the code where they occur (the Stack Trace).

You can then click through to open a web message, where you can manipulate the data sent. You can also have DOM Invader spoof the origin of a web message, simply by clicking the "Spoof origin" check box. Pretty cool, right?

If you find a vulnerable event listener and you've successfully crafted an exploit in the data box, then you can generate a proof of concept at the touch of a button. Simply click the "Build PoC" button, and your PoC will be copied to the clipboard.

DOM Invader is capable of manipulating web messages and spoofing their origin automatically, if you so wish. DOM Invader also attempts to grade the severity and confidence of messages it sees based on several factors - including if the message data was found in a sink and what type of sink it was. When messages are manipulated, DOM Invader will attempt to do a follow up with more interesting characters. If this is successful it will upgrade the severity and confidence based on the follow up characters that were found unencoded in the sink.

List of sources and sinks

Whilst developing DOM Invader we quite naturally needed a list of sources and sinks so we decided to produce one and put it into DOM Invader. We decided to release this list and terminology as it was trivial to extract from the source anyway. This will be included in the XSS cheat sheet when it's updated - but for now the current list will be added to this post. We use the sink ranking terminology in order to decide which sink is more important than others. The lower the value, the more important the sink is.

Sources

const sourcesList = [

"location",

"location.href",

"location.hash",

"location.search",

"location.pathname",

"document.URL",

"window.name",

"document.referrer",

"document.documentURI",

"document.baseURI",

"document.cookie"

];

Sinks

const sinkRanking = {

"jQuery.globalEval":1,

"eval":2,

"Function":3,

"execScript":4,

"setTimeout":5,

"setInterval":6,

"setImmediate":7,

"msSetImmediate":7,

"script.src":8,

"script.textContent":9,

"script.text":10,

"script.innerText":11,

"script.innerHTML":12,

"script.appendChild":13,

"script.append":14,

"document.write": 15,

"document.writeln": 16,

"jQuery":17,

"jQuery.$":18,

"jQuery.constructor":19,

"jQuery.parseHTML":20,

"jQuery.has":20,

"jQuery.init":20,

"jQuery.index":20,

"jQuery.add": 20,

"jQuery.append": 20,

"jQuery.appendTo": 20,

"jQuery.after": 20,

"jQuery.insertAfter": 20,

"jQuery.before": 20,

"jQuery.insertBefore": 20,

"jQuery.html": 20,

"jQuery.prepend": 20,

"jQuery.prependTo": 20,

"jQuery.replaceWith": 20,

"jQuery.replaceAll": 20,

"jQuery.wrap": 20,

"jQuery.wrapAll": 20,

"jQuery.wrapInner": 20,

"jQuery.prop.innerHTML": 20,

"jQuery.prop.outerHTML": 20,

"element.innerHTML":21,

"element.outerHTML":22,

"element.insertAdjacentHTML":23,

"iframe.srcdoc": 24,

"location.href":25,

"location.replace":26,

"location.assign":27,

"location":28,

"window.open":29,

"iframe.src":30,

"javascriptURL":31,

"jQuery.attr.onclick":32,

"jQuery.attr.onmouseover":32,

"jQuery.attr.onmousedown":32,

"jQuery.attr.onmouseup":32,

"jQuery.attr.onkeydown":32,

"jQuery.attr.onkeypress":32,

"jQuery.attr.onkeyup":32,

"element.setAttribute.onclick":33,

"element.setAttribute.onmouseover":33,

"element.setAttribute.onmousedown":33,

"element.setAttribute.onmouseup":33,

"element.setAttribute.onkeydown":33,

"element.setAttribute.onkeypress":33,

"element.setAttribute.onkeyup":33,

"createContextualFragment":34,

"document.implementation.createHTMLDocument": 35,

"xhr.open":36,

"xhr.send": 36,

"fetch": 36,

"fetch.body": 36,

"xhr.setRequestHeader.name": 37,

"xhr.setRequestHeader.value": 38,

"jQuery.attr.href":39,

"jQuery.attr.src":40,

"jQuery.attr.data":41,

"jQuery.attr.action":42,

"jQuery.attr.formaction":43,

"jQuery.prop.href":44,

"jQuery.prop.src":45,

"jQuery.prop.data":46,

"jQuery.prop.action":47,

"jQuery.prop.formaction":48,

"form.action":49,

"input.formaction":50,

"button.formaction":51,

"button.value": 52,

"element.setAttribute.href":53,

"element.setAttribute.src":54,

"element.setAttribute.data":55,

"element.setAttribute.action":56,

"element.setAttribute.formaction":57,

"webdatabase.executeSql": 58,

"document.domain":59,

"history.pushState":60,

"history.replaceState":61,

"xhr.setRequestHeader":62,

"websocket":63,

"anchor.href":64,

"anchor.target": 65,

"JSON.parse": 66,

"document.cookie":67,

"localStorage.setItem.name": 68,

"localStorage.setItem.value": 69,

"sessionStorage.setItem.name": 70,

"sessionStorage.setItem.value": 71,

"element.outerText": 72,

"element.innerText": 73,

"element.textContent": 74,

"element.style.cssText": 75,

"RegExp":76,

"window.name":77,

"location.pathname": 78,

"location.protocol": 79,

"location.host": 80,

"location.hostname": 81,

"location.hash": 82,

"location.search": 83,

"input.value": 84,

"input.type": 85,

"document.evaluate": 86

};

Team effort

I temporarily joined the PortSwigger Scanner team whilst developing this tool and I worked with so many talented people. It was a real team effort to produce the final product. I'd like to thank James Kettle for coming up with the idea to create an extension and for helping with the initial design. James was inspired by Filedescriptor's (Cure53) similar tool.

I did some refactoring with Patrick Albinson and he proved he is a Gradle god when helping get DOM Invader into Burp. Alex was heavily involved in refactoring and improving DOM Invader so much and made quite brilliant suggestions to move it lightyears ahead of the initial prototype. Paul Wilshaw improved the UI tremendously and made everything look pretty, especially the Postmessage features. Thanks to Nolan Ward for doing the video editing and creating the fantastic animation. Thanks to Matt Atkinson for helping with the copy editing and Nigel Evans for doing a great job with the documentation. Chris Wood really helped organizing UI sessions and finally I'd like to thank James Kettle, Michael Stepankin, Andrzej Matykiewicz and Trikster for being guinea pigs and UX testing the tool.

Eating our own dog food

Hopefully, you're now raring to go and find some DOM XSS with DOM Invader. We think there's plenty out there. In fact, we know there is, because we recently struck gold on a well-known bug bounty program while testing DOM Invader's functionality. Head over to the research channel to read up about the PayPal DOM XSS I found.

To get started with DOM Invader, download the early adopter latest version of Burp Suite Professional/Community Edition and head to the embedded browser.

View the full documentation for DOM Invader.

Don't forget to follow @PortSwiggerRes on Twitter for the latest Burp Suite news and hacking exploits. That includes a writeup of the hack above.

XSS

DOM

Hacking Tools

Gareth Heyes

@garethheyes

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
