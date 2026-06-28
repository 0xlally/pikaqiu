# DOM Invader and the case of direct eval vs indirect eval

Source: https://portswigger.net/blog/dom-invader-and-the-case-of-direct-eval-vs-indirect-eval
Fetched: 2026-06-28T09:15:14.460946+00:00

DOM Invader and the case of direct eval vs indirect eval

Gareth Heyes |

Monday, 25 September 2023 at 14:00 UTC

DOM Invader

JavaScript

What is DOM Invader?

DOM Invader is a browser extension that makes it easy to find DOM based XSS by instrumenting various JavaScript functions. You can find out more about DOM Invader here:

Introducing DOM Invader

How to enable DOM Invader

Direct eval vs indirect eval

You might have encountered a situation where a site will throw an exception from the eval function when DOM Invader is enabled, but not when DOM Invader is disabled. Why is that? To understand what's going on, we first need to know the difference between a direct and an indirect call to eval. This post is going to summarise and simplify the definition of direct/indirect calls to eval. If you are interested in more technical details then I recommend the post by

kangax

.

Direct eval call

If you read the JavaScript specification, it states that:

A direct call to the eval function is one that is expressed as a CallExpression that meets the following two conditions:

The Reference that is the result of evaluating the MemberExpression in the CallExpression has an environment record as its base value and its reference name is "eval".

The result of calling the abstract operation GetValue with that Reference as the argument is the standard builtin function defined in 15.1.2.1.

In other words a direct call is when the function that is called is named eval and, when the result evaluates to the eval function. When this function is executed directly, something quite special happens - the locally scoped variables where the function is executed are then evaluated by eval and are available when it's called:

function x(){

let myLocalVariable = 1337;

eval("console.log(myLocalVariable)");//1337

}

x()

When the string is evaluated, myLocalVariable is passed to the console.log() function and the correct value is then sent to the console. So now you know what a direct call to eval is and why it's special, but what about indirect calls to eval?

Indirect eval call

An indirect call is the opposite of a direct call so it means when the reference to the eval function is not named eval. Let's run the code again but with an indirect eval():

function x(){

let myLocalVariable = 1337;

xeval("console.log(myLocalVariable)");

//exception myLocalVariable is undefined

}

xeval=eval;

x()

Even though all we've done is use a reference to eval, "myLocalVariable" is now undefined - this is what you might encounter on some applications. Locally scoped variables are now unavailable but what about the global scope? If we do another test we can see how direct/indirect calls handle global variables:

window.myVariable = 1;

function x(){

let myVariable = 2;

eval("console.log(myVariable)");//2

}

x()

In the preceding example - because we are using a direct call to eval - the local variable is used instead of the global variable and the console prints 2. If we do the same with an indirect call, we see different results:

window.myVariable = 1;

function x(){

let myVariable = 2;

xeval("console.log(myVariable)");//1

}

xeval=eval;

x()

As the locally scoped variable is unavailable to the indirect call the global variable is used instead, so the value sent to the console is 1. This is why some sites break when DOM Invader is enabled because the eval() function is instrumented. It therefore becomes an indirect eval and if the site has any locally scoped variables that are needed by the eval() call then an exception will be thrown.

How to fix it

To fix this problem you can prevent DOM Invader from instrumenting the eval() function, this will prevent you from finding vulnerabilities in eval calls but enable you to restore the eval to its previous state. See our documentation on how to do this:

Customizing sources and sinks

DOM Invader

JavaScript

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
