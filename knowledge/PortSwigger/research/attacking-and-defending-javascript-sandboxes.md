# Attacking and defending JavaScript sandboxes

Source: https://portswigger.net/research/attacking-and-defending-javascript-sandboxes
Fetched: 2026-06-28T09:17:20.967785+00:00

Attacking and defending JavaScript sandboxes

Gareth Heyes

Researcher

@garethheyes

Published: Wednesday, 15 July 2020 at 13:12 UTC

Updated: Thursday, 16 July 2020 at 10:39 UTC

Attacking sandboxes

When I found the Safari Unicode issue earlier I started to look at current JavaScript sandboxes and found a few different ones that used a proxy. A proxy is a special object that allows you to intercept operations on the target object such as get/set/function call operations. A proxy should be an ideal candidate for creating a sandbox since you can use it to intercept any property access on the object but it's never that simple; there are a few issues that you need to overcome.

A well known JavaScript dev created a simple JavaScript sandbox in a gist a few years ago. It had a few flaws. First, because there was no syntax checking at all you could inject a closing curly brace to break out of the "with" statement and inject any code you like:

sandboxJS("}eval('alert(1337)');{");

There was no protection against overwriting prototypes either so you could modify key functions like indexOf and make them return true for the allow list. The first execution of the sandbox would modify indexOf and the second execution would allow you to use any code:

sandboxJS("[].constructor.prototype.indexOf=x=>1");

sandboxJS("eval('top.alert(1337)')");

It didn't protect the Function constructor from being accessed either, which enabled an attack used on the AngularJS sandbox many times. That would allow you to use primitives to get the Function constructor and execute any code you like:

sandboxJS("''.sub.constructor('eval(alert(1337))')()");

I also found another sandbox using the "with" statement that was made a few years ago but this had similar problems as the one above. There was no syntax checking so you could again solve it by breaking out of the "with" statement:

test('}}eval("alert(1337)");{+function(){');

Using generators could also bypass the sandbox. When you create a generator function it has its own constructor that is different than the Function constructor and JavaScript offers no way to modify or delete this constructor and so you can bypass this sandbox using generators:

test('(function*(){}).constructor("eval('alert(1337)')")().next()');

Sandbox defence

We wondered if it was possible to create a more resilient proxy-based sandbox. First we created a checkSyntax function that simply uses the Function constructor to generate a function of the code without executing it. This prevents attacks such as breaking out of the "with" statement:

function checkSyntax(code) {

Function(code);

}

Then we freeze all global prototypes such as the String prototype. This prevents them from being modified and stops attacks such as the indexOf attack mentioned earlier:

if(!Object.isFrozen(String.prototype)) {

Function.prototype.constructor = null;

Object.freeze(String.prototype);

Object.freeze(Number.prototype);

Object.freeze(Array.prototype);

Object.freeze(Symbol.prototype);

Object.freeze(Math.prototype);

Object.freeze(Function.prototype);

Object.freeze(RegExp.prototype);

}

After that we create two proxies: a catchAllProxy which is in an outer "with" statement and a handler that returns true to capture every property and either return undefined or a global such as "window". Then we have an inner proxy inside another with statement, this proxy is our global object and contains all of the allowed properties. The reason we do this is to allow operators such as the "in" operator to work on the global object (inner proxy) and to capture any other property requested that doesn't match the allow list with the outer proxy:

var output = Function('proxy', 'catchAllProxy', `

with(catchAllProxy) {

with(proxy) {

return (function(){

${code};

})();

}

}

`)(proxy, catchAllProxy);

The allow list object is used to specify which objects/functions you wish the sandbox to allow. I used a suffix of __$ to make sure only these properties are allowed:

var allowList = {

__proto__: null,

console__$:console,

alert__$: function(){

alert("Sandboxed alert:"+arguments[0]);

},

String__$: String,

Number__$: Number,

Array__$: Array,

Symbol__$: Symbol,

Math__$: Math,

RegExp__$: RegExp,

Object__$: Object,

eval__$: function(code){

return NiceScript.run("return "+code);

}

};

Another problem that often occurs with JavaScript sandboxes is a leaking window. We've encountered that in the past with AngularJS with the __lookupGetter__ function. Even though you have a proxy intercepting every possible property you can still use functions to get a reference to the window object. You can do this because by default JavaScript falls back to the window object when using "this" in a function that's not creating an object. For example:

function x() {return this;}

x().alert(1)

This can be prevented by using the "use strict" directive. In this mode among other things JavaScript won't fallback to the "window" object and instead will use undefined. This plugs the security hole:

var output = Function('proxy', 'catchAllProxy', `

with(catchAllProxy) {

with(proxy) {

return (function(){

"use strict";

${code};

})();

}

}

`)(proxy, catchAllProxy);

Two problems remained: Generator functions and the dynamic import statement. Unfortunately there is no way to prevent the dynamic import statement being called. This is because it's not a user definable function and therefore you cannot overwrite it or intercept it. The solution we came up with is to look for the import via a regex:

if(/\bimport\s*(?:[(]|\/[*]|\/\/|<!--)/.test(code)) {

throw new Error("Dynamic imports are blocked");

}

Obviously not ideal but there are plans to prevent this being called with strings so until then we are left with this patch. Then we have the function generator problem, there appears to be no way to overwrite the function generator constructor and there is no global FunctionGenerator function. However, we can overwrite the function generator methods and prevent them from being called. This obviously disables generators but does prevent the code from being executed:

Object.getPrototypeOf(function*(){}).constructor.prototype.prototype.return = null;

Object.getPrototypeOf(function*(){}).constructor.prototype.prototype.throw = null;

Object.getPrototypeOf(function*(){}).constructor.prototype.prototype.next = null;

Object.freeze((function*(){}).constructor.prototype.prototype);

We hope you enjoyed this post, it's great to look at JavaScript sandboxing within JavaScript because you can learn more about the language and see the current limitations of what's possible. We'd love to see a way to customise the dynamic import statement, not only for sandboxing but also dynamic analysis as there is currently no way to do this in any JavaScript engine. We know that JavaScript sandboxing is very difficult and we expect our sandbox to be broken, some have even called it a fool's errand. However we feel it's worth looking at from both an attack and defence perspective if we want to improve security. If you want to play with this sandbox and even break it which would be great then please try it below:

Nice Script sandboxing demo

The source code is also available on GitHub if you want to contribute:

Nice Script source code

Update...

The great Michał Bentkowski bypassed nice script using aysnc functions/generators. Thankfully he provided a very cool patch that will protect against async constructor attacks but will allow generators to be used too. The first attack used async functions & generators. I protected against constructor attacks by assigning null to the Function constructor but async functions have their own Function constructor. Here are the attacks:

(async function(){}).constructor('alert(1)')();

(async function*(){}).constructor('alert(2)')().next();

So the first vector is an async function and uses the async constructor. The second one is a async generator function. The sandbox prevented generator methods next(),throw(),return() from being called. However because this is a async generator it too gets a different Function constructor bypassing the sandbox.

He broke the sandbox again but this time with dynamic imports. I had to patch dynamic imports with a regex. The regex looks for the import command followed by zero or more spaces and then either "(", "/*", "<!--" or "//" but I forgot about --> which is a valid single line comment in JavaScript. The exploit was:

import

-->

('data:text/javascript,alert(1)')

Antony Garand found I forgot to freeze BigInt. I've now patched this. Thanks to Terjanq for spotting a typo with RegExp that would lead to being able to modify the RegExp object.

Can you break it?

Back to all articles

Related Research

05 February 2026

06 January 2026

The Fragile Lock:

Novel Bypasses For SAML Authentication

10 December 2025

The Fragile Lock:

Novel Bypasses For SAML Authentication

Introducing HTTP Anomaly Rank

11 November 2025

Introducing HTTP Anomaly Rank
