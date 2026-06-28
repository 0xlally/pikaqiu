# Preventing prototype pollution vulnerabilities

Source: https://portswigger.net/web-security/prototype-pollution/preventing
Fetched: 2026-06-28T09:17:58.653085+00:00

Web Security Academy

Prototype pollution

Preventing

Preventing prototype pollution vulnerabilities

We recommend patching any prototype pollution vulnerabilities you identify in your websites, regardless of whether these are coupled with exploitable gadgets. Even if you're confident that you haven't missed any, there's no guarantee that future updates to your own code or any libraries you use won't introduce new gadgets, paving the way for viable exploits.

In this section, we'll provide some high-level advice on some of the measures you can take to protect your own websites from the threats we've covered in our labs. We'll also cover some common pitfalls to avoid.

Sanitizing property keys

One of the more obvious ways to prevent prototype pollution vulnerabilities is to sanitize property keys before merging them into existing objects. This way, you can prevent an attacker from injecting keys such as __proto__, which reference the object's prototype.

Using an allowlist of permitted keys is the most effective way to do this. However, as this is not feasible in many cases, it's common to use a blocklist instead, removing any potentially dangerous strings from user input.

Although this is a quick fix to implement, truly robust blocklisting is inherently tricky, as demonstrated by sites that successfully block __proto__, but fail to account for an attacker polluting an object's prototype via its constructor. Likewise, weak implementations can also be bypassed using simple obfuscation techniques. For this reason, we only recommend this as a stopgap rather than a long-term solution.

Preventing changes to prototype objects

A more robust approach to preventing prototype pollution vulnerabilities is to prevent prototype objects from being changed at all.

Invoking the Object.freeze() method on an object ensures that its properties and their values can no longer be modified, and no new properties can be added. As prototypes are just objects themselves, you can use this method to proactively cut off any potential sources:

Object.freeze(Object.prototype);

The Object.seal() method is similar, but still allows changes to the values of existing properties. This may be a good compromise if you're unable to use Object.freeze() for any reason.

Preventing an object from inheriting properties

While you can use Object.freeze() to block potential prototype pollution sources, you can also take measures to eliminate gadgets. This way, even if an attacker identifies a prototype pollution vulnerability, it is likely to be unexploitable.

By default, all objects inherit from the global Object.prototype either directly or indirectly via the prototype chain. However, you can also manually set an object's prototype by creating it using the Object.create() method. Not only does this let you assign any object you like as the new object's prototype, you can also create the object with a null prototype, which ensures that it won't inherit any properties at all.

let myObject = Object.create(null);

Object.getPrototypeOf(myObject); // null

Using safer alternatives where possible

Another robust defense against prototype pollution is to use objects that provide built-in protection. For example, when defining an options object, you could use a Map instead. Although a map can still inherit malicious properties, they have a built-in get() method that only returns properties that are defined directly on the map itself:

Object.prototype.evil = 'polluted';

let options = new Map();

options.set('transport_url', 'https://normal-website.com');

options.evil; // 'polluted'

options.get('evil'); // undefined

options.get('transport_url'); // 'https://normal-website.com'

A Set is another alternative if you're just storing values rather than key:value pairs. Just like maps, sets provide built-in methods that only return properties that were defined directly on the object itself:

Object.prototype.evil = 'polluted';

let options = new Set();

options.add('safe');

options.evil; // 'polluted';

option.has('evil'); // false

options.has('safe'); // true

Find prototype pollution vulnerabilities using Burp Suite

Try for free
