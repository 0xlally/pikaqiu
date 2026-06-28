# Make Burp Suite your own: high-powered extensibility to customize and enhance your testing. 🛠️

Source: https://portswigger.net/blog/make-burp-suite-your-own-high-powered-extensibility-to-customize-and-enhance-your-testing
Fetched: 2026-06-28T09:15:19.344829+00:00

Make Burp Suite your own: high-powered extensibility to customize and enhance your testing. 🛠️

Amelia Coen |

Friday, 10 January 2025 at 15:53 UTC

Extensibility in Burp Suite is about giving you and your team the power to customize, enhance, and extend Burp Suite to match your testing needs and objectives.

This comprises a powerful suite of tools and frameworks that allow you to extend Burp Suite’s capabilities, enabling tailored workflows and solutions for any testing scenario.

Whether it’s precise power-ups with Bambdas, custom scan checks with BChecks, or adding your own tools and functionality with Extensions, Burp Suite can adapt to individuals and organizations alike.

Power up your testing with Bambdas

Bambdas are easy-to-write code snippets designed to seamlessly extend Burp Suite’s capabilities for precise, modular enhancements.

If you’re looking to fine-tune specific parts of your workflow without friction, Bambdas are the perfect way to quickly personalize Burp Suite to meet your needs or share enhancements across your team.

Here’s some examples of Bambdas that you can use in Burp…

Detect403Forbidden.bambda by ctflearner

/**

* Bambda Script to Detect "403 Forbidden" in HTTP Response

* @author ctflearner

* This script identifies if the HTTP response status code is 403 (Forbidden).

* It ensures there is a response and checks if the status code indicates access is denied.

**/

return requestResponse.hasResponse() && requestResponse.response().statusCode() == 403;

Use this Bambda to filter for a specific response code in the HTTP Proxy history.

IncorrectContentLength.bambda by ps-porpoise

/**

* Finds responses whose body length do not match their stated Content-Length header.

*

* @author albinowax

**/

if (!requestResponse.hasResponse() || requestResponse.request().method().equals("HEAD")) {

return false;

}

int realContentLength = requestResponse.response().body().length();

int declaredContentLength =

Integer.parseInt(requestResponse.response().headerValue("Content-Length"));

return declaredContentLength != realContentLength;

Use this Bambda to filter for a discrepancy between the stated Content-Length of a response and the actual content length of the response in the HTTP Proxy history.

How do I create a Bambda?

If you’re using Burp Suite Professional or Burp Suite Community Edition, you can currently create your own Bambda to add custom filters to tables in the following places:

Proxy HTTP history

Proxy WebSockets history

Logger view

Logger capture

Site map

In Burp Suite Professional, you can also use Bambdas to:

Add custom columns in the Proxy History table

Create custom match and replace rules in the Proxy

Save your Bambda as a JSON file to make it easier for you to migrate your configuration to other projects. You can also share it with the Burp community, by adding it to the ever-growing Bambdas repository on GitHub.

Read more about how to create your first Bambda.

What’s new with Bambdas?

Filtering site maps with Bambdas

Be hyper-specific with the sites you want to filter within the sitemap table with a Bambda, giving you a high-level view within just a few clicks.

Bambda match and replace

Personalize the expressions you want to auto-modify in match and replace by writing your own Bambda. This will allow you to tailor your use of match and replace to fit your personal workflow or tech stack.

Match and replace Bambdas have access to a significant portion of the Montoya API to use, meaning your match and replace rules can become even more powerful. This includes the ability to perform analysis and initiate requests to other tools in Burp.>

Here’s a couple of example Bambdas you can use within match and replace…

Replace placeholder with random value

if (!(requestResponse.request().contains("randomplz", true))) {

return requestResponse.request();

}

var arr = requestResponse.request().toString().replace("randomplz", utilities().randomUtils().randomString(8));

return HttpRequest.httpRequest(requestResponse.httpService(), arr);

Request signature

var signature =

HexFormat.of().formatHex(utilities().cryptoUtils().generateDigest(requestResponse.request().body(), DigestAlgorithm.SHA_256).getBytes());

return requestResponse.request().withAddedHeader("Content-Sha256", signature);

Bambda output console

Gain increased visibility and debug your Bambda by using the new Bambda output console to track exactly what your Bambda is doing during execution.

Coming soon…

Bambda library

It’ll be easier than ever to access your favorite Bambdas with the personal Bambda library. You’ll no longer need to import your Bambdas to each project file you open - instead, simply save them to your own Bambda library in Burp.

With the Bambda library, it’ll be easy to manage your Bambdas and quickly share them with team mates, boosting collaboration and allowing you to tailor your Bambda usage to your own testing goals.

Tailor automation with BChecks

Custom Scan Checks (BChecks) are an intuitive mechanism to create and use tailored checks that expand Burp Suite’s scanning coverage using an easy-to-learn, purpose-built language.

If you or your organization are seeking to standardize your scanning practices, Custom Scan Checks will allow you to automate the detection of niche vulnerabilities and scale these customizations across your portfolio for consistent results.

Where can I use Custom Scan Checks?

Custom Scan Checks are available in both Burp Suite Professional and Burp Suite Enterprise Edition.

Write your own Custom Scan Checks - tailored specifically to your own application - in Burp Suite Professional, or select a community-made BCheck from the BCheck library, and import them directly into Burp Suite Enterprise Edition.

Explore the growing library of community-created BChecks to see how others are enhancing their security testing workflows.

Extend Burp, your way

Extensions are hyper-flexible, user-made tools that allow you and your teams to extend Burp Suite in countless ways. This includes…

Handling complex authentication requirements

Encoding, decoding, encrypting and decrypting traffic

User interface and workflow enhancements

Integrating with third-party tooling

The capabilities of extensions in Burp are vast and can provide a very high degree of power and customization to your workflow.

Use extensions to add or share additional functionality beyond what’s available out of the box, and continuously enhance Burp Suite to match evolving testing needs and leverage a vibrant ecosystem of shared tools.

What are BApps?

Created by a thriving community of Burp users with 10+ years of knowledge and experience, you can find a library of over 300 PortSwigger-approved extensions for Burp Suite in the BApp Store.

Not sure where to start? Here are a few of our top picks this month…

ActiveScan++ by James Kettle

Extend Burp Suite's active and passive scanning capabilities, with minimal network overhead, with this old favourite that has recently been updated. ActiveScan++ is now compatible with both Burp Suite Professional and Burp Suite Enterprise Edition.

JWT Editor by Dolph Flynn and Fraser Winterborn

Want to manipulate JSON Web Tokens (JWTs) within messages inside Burp and facilitate common attacks?

JWT Editor provides automatic detection and in-line editing of JWTs within HTTP requests/responses and web socket messages, signing and encrypting of tokens and automation of several well-known attacks against JWT implementations.

Autorize by Barak Tawily

Simplify your hunt for broken access controls by automating the process of testing requests with different privilege levels.

Explore all community-created extensions in the BApp Store.

How can I create my own extension?

Can’t find an existing BApp to achieve what you want? Write your own extensions for Burp Suite in Java using our Montoya API.

Learn more about how to create your own extension.

Have an extension you’re proud of and want to share with the world? Submit your extension to the BApp store, and help a community of 80,000+ testers benefit from your work.

You can read more about the submission criteria to ensure your extension meets the necessary requirements for the BApp store.

Harness the power to customize, enhance and extend Burp

With Bambdas, BChecks and Extensions, you’ll find a plethora of ways to personalize Burp Suite’s functionality to achieve your specific goal.

Using Burp’s extensibility to supercharge your testing?

Let us know how you’ve been extending Burp on X, Blue Sky, or LinkedIn.

Want to share your extensions with the wider Burp community?

Join the PortSwigger Discord and take part in conversation over on the dedicated #bambdas, #bchecks, and #extensions channels to share your own uses of extensibility, and pick up tips from the community.

Amelia Coen

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
