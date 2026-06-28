# Testing for DOM XSS

Source: https://portswigger.net/burp/documentation/desktop/tools/dom-invader/dom-xss
Fetched: 2026-06-28T09:16:03.103861+00:00

Support Center

Documentation

Desktop editions

Tools

DOM Invader

Testing for DOM XSS

ProfessionalCommunity Edition

Testing for DOM XSS

Last updated:

June 18, 2026

Read time:

4 Minutes

Testing for DOM XSS can be tedious as it often involves manually tracking the flow of your input through complex JavaScript, which may stretch to thousands of lines of code. DOM Invader greatly simplifies this process by instantly showing you any sinks that your input flows into, along with the surrounding context.

You can access most of the related features from the extension's DOM view.

Injecting a canary

DOM Invader works by automatically parsing the DOM to look for occurrences of a predefined "canary" string. This is an arbitrary but distinct string of alphanumeric characters that you can inject into different sources to see which sinks they flow into.

You can see the current canary that DOM Invader is tracking in the upper-left corner of the DOM view. Note that you can change the canary to a custom string if you prefer.

To manually inject the canary into a source:

Go to the DOM Invader tab in the browser's DevTools panel.

Make sure that you are in the DOM view.

Click Copy canary. The canary that DOM Invader is tracking is copied to your clipboard.

Paste the canary into any inputs that you want to test. This could be query parameters in the URL, form fields, and so on.

For more information about potential sources, check out our topic on DOM-based vulnerabilities on the Web Security Academy.

Web Security Academy

DOM-based vulnerabilities

Injecting a canary into multiple sources

Although you can manually paste the canary into multiple sources at once, you also have the following options for doing this automatically:

Inject URL params - Automatically injects the canary into every query parameter in the URL, using a separate tab for each parameter.

Inject forms - Automatically injects the canary into any HTML form fields detected on the page. Note that you still need to submit the form manually for the injection to take effect.

Note

Injecting the canary into all URL parameters and form fields at once may prevent the site from working properly. For the best results, we recommend testing one source at a time.

Identifying controllable sinks

After you inject a canary, DOM Invader automatically parses the DOM to identify any sinks in which your canary appears. It then displays these sinks in the DOM view, sorted in order of how interesting they are.

Determining the XSS context

Once you have identified a controllable sink, the next step is to study the context in which your injected payload appears. This includes determining the following information:

Whether you're working with an HTML or JavaScript execution sink.

Whether your input is surrounded by any special characters that you need to break out of. These include quotes, tags, attributes, and so on.

What kind of validation, sanitization, or other processing the website performs on your input before it reaches the sink.

To help you with this, DOM Invader displays the sink's contents, including both your canary and any surrounding characters that you inject as they appear in the DOM. This means you can append special characters to your canary in order to easily see whether they are being escaped or encoded. In the following example, you can see that we're able to successfully inject a variety of useful characters.

You can also see the following details depending on the type of sink DOM Invader has identified:

Outer HTML - The HTML element that surrounds your canary.

Frame path - The frame in which your canary is passed to the sink.

Event - The JavaScript event that occurs when your canary is passed to the sink.

This information enables you to easily see the XSS context and test which characters and events you need to craft an exploit. In the following example, we've successfully broken out of the double-quoted string and surrounding <span> in order to inject our XSS proof-of-concept exploit.

Studying the client-side code

When experimenting with different injections, you might find that your input suddenly stops flowing into the sink. This could be because you can only reach the sink via a specific code path, such as one branch of a conditional statement.

DOM Invader enables you to jump straight to the point in the client-side code where your input is passed to the sink. You can then study the preceding code to identify what conditions your input must meet in order to reach the sink.

To view the relevant line in the code:

Inject a payload that you know will reach the sink.

In DOM Invader's DOM view, click the link in the Stack Trace column. This outputs a stack trace to the browser's console.

In the DevTools panel, switch to the Console tab.

In the stack trace, click the uppermost link (there may only be one). This opens the client-side JavaScript in the Sources tab and focuses on the line where your input is passed to the sink.

Read more

DOM Invader is highly configurable. For more information about DOM Invader's advanced features and how you can fine-tune their behavior for a particular site, see DOM Invader settings.
