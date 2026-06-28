# Finding client-side prototype pollution with DOM Invader

Source: https://portswigger.net/blog/finding-client-side-prototype-pollution-with-dom-invader
Fetched: 2026-06-28T09:15:15.668417+00:00

Finding client-side prototype pollution with DOM Invader

Gareth Heyes |

Monday, 20 June 2022 at 12:37 UTC

DOM Invader

DOM

Client-side prototype pollution

XSS

Cross Site Scripting

Last year we made it significantly easier to find DOM XSS, when we introduced a brand new tool called DOM Invader. This year, we've improved DOM Invader to make finding CSPP (client-side prototype pollution) as easy as a couple of clicks. If you want to investigate, find, and fix client-side prototype pollution vulnerabilities then you really should read on - to discover how DOM Invader makes your life easier. We've also created another YouTube video to help you use the new features:

What is prototype pollution?

We hope to release some client-side prototype pollution labs on our Web Security Academy in a few months demonstrating the issue but for now here's what you need to know.

Prototype pollution is a vulnerability that occurs when you merge an object with a user controlled JSON object. It can also occur as a result of an object generated from query/hash parameters, when the merge operation does not sanitize the keys. This enables an attacker to use property keys like __proto__ , which then allows them to create arbitrary assignments to the Object.prototype (or other global prototypes). When this happens, it's referred to as a prototype pollution source. The following sample code demonstrates this:

params.replace(/\+/g, ' ').split('&').forEach(function(v){

var param = v.split( '=' ),

key = decodeURIComponent( param[0] ),

val,

cur = obj,

I = 0,

//…

obj[key]=val;

//…

let url = new URL(location);

let params = url.searchParams;

deparam(params.toString())

In order to exploit prototype pollution you need a source and a gadget. A prototype pollution gadget occurs when a site uses a property in a dangerous way without filtering. For example a site might do the following:

let myObject = {};

if(myObject.html) {

document.getElementById('myElement').innerHTML = myObject.html;

}

At first glance it might look like there isn't a problem here. The object doesn't contain any properties, but the JavaScript engine will look at the Object.prototype for the "html" property if it doesn't exist on the current object. This then leads to a prototype pollution gadget called "html". Let's see what happens when we modify the Object.prototype:

<div id="myElement"></div>

<script>Object.prototype.html="<img src onerror=alert(1)>";</script>

<script>

let myObject = {};

if(myObject.html) {

document.getElementById('myElement').innerHTML = myObject.html;

}

</script>

This results in the Object.prototype.html property being used, instead of the "html" property of the "myObject" object. A developer will assume that such properties are not user controlled and thus leads to XSS.

How do I discover client-side prototype pollution sources?

If you want DOM Invader to find prototype pollution sources you have to switch on the prototype pollution option.

When you have switched it on, browse to a site that you wish to test. You can use one of our test cases if you want to see how it works. DOM Invader will attempt to test the query string, hash, and JSON objects sent using a web message, and report if it was successful.

In this case DOM Invader has found two prototype pollution sources that both occur within the query string - indicated by "in search". You can use the "Test" button to manually verify the source, or you can use the "Scan for gadgets" button to discover gadgets automatically. If you choose the latter, DOM Invader will open a new window and show a progress bar. Once it's finished scanning, it will show you the results in the augmented DOM:

In the example above, DOM Invader has discovered a gadget called "html", which ends up in an innerHTML sink. You'll notice that a green "Exploit" button has appeared - this will combine the source discovered with the gadget and automatically create a prototype pollution exploit.

If you'd like to try DOM Invader out with a real CSPP vulnerability, we've hidden one in our Gin & Juice Shop; see if you can exploit it!

Finding prototype pollution on real world sites

As always at PortSwigger, we use our tools to find real world vulnerabilities - whilst doing that we encountered many problems that we could solve by improving DOM Invader. The first thing that became apparent when gadget scanning was that we would get a lot of noise from non-interesting sinks. To solve this, we decided to only show interesting sinks by default. If you're not happy with the default, you can change which sources/sinks are shown if you so wish.

We wanted to automate the discovery of prototype pollution sources and we found the best way to do that was to use Puppeteer. We had a problem though, how to get the vulnerabilities out of DOM Invader? We could use Puppeteer to traverse the DOM like we've done for our automated tests but that would be slow and cumbersome.

So we decided to add callbacks in DOM Invader. Callbacks enable you to run JavaScript when a source, sink or message has been found, this makes life easier for logging vulnerabilities. If you open the configuration cog again as before you'll notice each sub tab has a callback configuration button. This callback will allow you to call some custom JavaScript every time an item has been found, and data will be passed to the callback that you can use:

Using these callbacks is really powerful, you can use navigator.sendBeacon or fetch to send this data to an endpoint that logs the data. You can return true or false if you want DOM Invader to show the data - this can be really useful if there's a noisy site and you want to know what data hits a specific sink. Callbacks are disabled by default which is why they are shown greyed out - once you edit one and click save it becomes active. You can use the reset button to deactivate the callback function and revert it to its default state.

I created a source callback:

function(sourceDetails, sources) {

let data = JSON.stringify(sourceDetails);

let url = 'http://localhost:8000/log.php';

fetch(url, {__proto__:null, method: "post", keepalive: true, body: data});

return true;//return true to log source

}

This sent the data to a PHP script which logged the data. I then began testing them for gadgets. You can scan for gadgets independently even if the site has no known prototype pollution source. To do this you need to switch the mode in the prototype pollution settings cog:

You'll notice DOM Invader tries to choose the optimal settings for gadget scanning - for example, it will remove CSP response headers - you can override these defaults if you so wish. Using these techniques I discovered multiple sites that were vulnerable to client-side prototype pollution including a well known car manufacturer, a well known game site, a major Wordpress domain and others.

Credits and thanks

As always James Kettle has been super helpful with the design of DOM Invader and made the excellent suggestion of having a "Scan for gadgets" button thanks James. Thanks to Nolan Ward for the excellent graphics and video editing. There has been some excellent research into client-side prototype pollution that I found really helpful. Thanks to Sergey Bobrov, Mohan Sri Rama Krishna P, Terjanq, Beomjin Lee, Masato Kinugawa, Nikita Stupin, Rahul Maini, Harsh Jaiswal, Mikhail Egorov, Melar Dev, Michał Bentkowski, Filedescriptor, Olivier, William Bowling, Ian Bouchard for sharing their excellent tools and research.

Obtaining the new version of DOM Invader

To get the new version of DOM Invader simply update your version of Burp Suite Professional or Burp Suite Community Edition to 2022.6 on the Early Adopter channel to start using it.

DOM Invader

DOM

Client-side prototype pollution

XSS

Cross Site Scripting

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
