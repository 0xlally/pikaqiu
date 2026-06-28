# Introducing Bambdas

Source: https://portswigger.net/blog/introducing-bambdas
Fetched: 2026-06-28T09:15:18.035399+00:00

Introducing Bambdas

Emma Stocks |

Tuesday, 14 November 2023 at 08:27 UTC

You've might have heard of Lambdas. But have you heard of Bambdas? They're a unique new way to customize Burp Suite directly from the UI, using only small snippets of Java.

Changing the face of Burp Suite

The introduction of Bambdas exposes some of the core "behind the scenes" functionality of Burp Suite for the very first time. In essence, as the feature is rolled out across various tools within Burp Suite, you'll be able to customize Burp to make it work in exactly the way that you want it to.

The possibilities contained within the Bambdas functionality are theoretically endless. As the feature develops, we believe it'll enable you to replace the age-old frustrated cry of "Why can't Burp do this?" with a shiny new phrase. "I wonder if I can create a Bambda to make this work the way I need it to?".

How to work with Bambdas

The first Bambda we've introduced enables you to write custom filters for the Proxy HTTP history. To help you get to grips with the unique potential of this functionality, we've created some examples to showcase some interesting request and response filters you might want to try.

Find requests with a specific cookie value

//Find requests with a specific cookie value

if (requestResponse.request().hasParameter("foo", HttpParameterType.COOKIE)) {

var cookieValue = requestResponse

.request()

.parameter("foo", HttpParameterType.COOKIE)

.value();

return cookieValue.contains("1337");

}

return false;

Find JSON responses with wrong Content-Type

//Find JSON respones with wrong Content-Type

//The content is probably json but the content type is not application/json

var contentType = requestResponse.response().headerValue("Content-Type");

if (contentType != null && !contentType.contains("application/json")) {

String body = requestResponse.response().bodyToString().trim();

return body.startsWith( "{" ) || body.startsWith( "[" );

}

return false;

Find role within JWT claims

//Find role within JWT claims

var body = requestResponse.response().bodyToString().trim();

if (requestResponse.response().hasHeader("authorization")) {

var authValue = requestResponse.response().headerValue("authorization");

if (authValue.startsWith("Bearer ey")) {

var tokens = authValue.split("\\.");

if (tokens.length == 3) {

var decodedClaims = utilities().base64Utils().decode(tokens[1], Base64DecodingOptions.URL).toString();

return decodedClaims.toLowerCase().contains("role");

}

}

}

return false;

Some helpful Bambdas code snippets

Once you're comfortable with the basics of how Bambdas work, there are a few tricks you might want to utilize to help you get even more value from the functionality. If you're using something a lot, and want to save yourself some time, you can assign it to a variable. For example:

var request = requestResponse.request();

If you want to check if a parameter exists, and if it's value is present, you can request it by name and check it for null instead:

var cookie = request.parameter("foo", HttpParameterType.COOKIE);

So that you can see how these code snippets can be applied, we've recreated the first example on finding requests with a specific cookie value.

Hear from the developers of Bambdas

Sean from the development team is here to introduce you to Bambdas, a unique new way to customize Burp Suite on the fly with small snippets of Java. You'll learn what a Bambda is, why we've built them into Burp Suite, and see a couple of examples of how Bambdas work.

Get started with Bambdas

Make sure that you're on the latest version of Burp Suite Professional or Burp Suite Community Edition. Then go to the Proxy HTTP history filter in Burp, switch to Bambda mode, and write a custom filter using your own code. Want some more guidance? Check out the documentation on filtering the HTTP history with Bambdas.

Emma Stocks

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
