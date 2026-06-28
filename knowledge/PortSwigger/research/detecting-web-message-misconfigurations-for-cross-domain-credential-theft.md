# Detecting web message misconfigurations for cross-domain credential theft

Source: https://portswigger.net/research/detecting-web-message-misconfigurations-for-cross-domain-credential-theft
Fetched: 2026-06-28T09:17:24.060052+00:00

Detecting web message misconfigurations for cross-domain credential theft

Gareth Heyes

Researcher

@garethheyes

Published: Wednesday, 9 November 2022 at 14:13 UTC

Updated: Wednesday, 9 November 2022 at 14:13 UTC

We released a new version of Burp recently on the Early Adopter channel that updates DOM Invader to help find cross-domain secrets. In this post we are going to show you how to use DOM Invader to detect URL tokens in misconfigured cross-domain web messages.

We noticed an excellent post by Frans Rosén on exploiting OAuth-Flows, and immediately started thinking about how to automate detection of such vulnerabilities. The main problem with auditing web messages is that it's a laborious task - they aren't sent over the wire, and you have to use the JavaScript debugger and add breakpoints and manually edit the message data. So we decided to make things easy by updating DOM Invader to inspect the message data, and notify you if a message contains data from the URL and is being sent to a different origin. This isn't foolproof, of course, and requires manual inspection to see if it is possible to embed the iframe and use this secret information in some way.

To start detecting cross-domain leaks, we need to enable the new option in DOM Invader. To do this, simply enable post message interception and click Detect cross-domain leaks:

Putting it to the test

We've prepared some test cases that can demonstrate this issue. Please visit the cross-domain secrets test case to try out this feature. When you have loaded the test case you should see some messages, and you'll notice that DOM Invader has found a "low" issue. If you click the message with a blue exclamation mark, you'll be able to see the full detail of the message:

In the message data above you should see a URL, along with a GET parameter called secret with a value of "supersecret". This test case demonstrates that you could embed the URL as an iframe, and then steal the "supersecret" value with a message event listener. To exploit the test case, you need to create a web message event listener that will read the data and use an iframe and point it to the target URL:

<script>

window.addEventListener('message',function(e){

console.log(e.data);//this should contain "supersecret"

})

</script>

<iframe src="https://subdomain1.portswigger-labs.net/dom-invader/testcases/postmessage-cross-domain-secrets/external.html"></iframe>

Summary

This post demonstrates how to use DOM Invader's new cross-domain leak feature to find secrets inside web messages. We've shown you how to enable the feature and find a vulnerable web message with just a couple of clicks. We'd love to hear of any findings you've got with this new feature, let us know and we'll RT the best blog posts.

DOM Invader

Credential Theft

Cross Domain

Back to all articles

Related Research

Widespread prototype pollution gadgets

22 June 2022

Widespread prototype pollution gadgets
