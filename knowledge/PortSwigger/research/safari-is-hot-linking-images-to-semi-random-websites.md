# Safari is hot-linking images to semi-random websites

Source: https://portswigger.net/research/safari-is-hot-linking-images-to-semi-random-websites
Fetched: 2026-06-28T09:17:28.983502+00:00

Safari is hot-linking images to semi-random websites

Gareth Heyes

Researcher

@garethheyes

Published: Monday, 31 October 2022 at 14:58 UTC

Updated: Friday, 3 May 2024 at 08:12 UTC

Every image is potentially a URL on Safari, thanks to over-enthusiastic OCR (Optical Character Recognition). This means you can link any image to an external website - and Safari might already be sending your users to unintended destinations.

This all started with the mysterious arrival of 'zon.com' on our company homepage. Ric (one of our designers) noticed some suspicious behaviour on our website. He came over to us, loaded our homepage on Safari and hovered over the Amazon logo. To our shock, it showed a link to "Zon.com". His first questions to us - "Have we been hacked? Why on earth is this URL showing on our homepage?!"

After some investigation with dev tools we didn't find anything out of the ordinary. So I loaded up Photoshop and made an image that had amazon.com in it. I loaded up Safari and hovered over the image, then a "quick look" menu popped up and gave a link to amazon.com!

This is a Safari feature, it attempts to parse URLs in images. What was happening was because the Amazon logo had an arrow underneath, it was breaking the OCR - this then resulted in the URL being parsed as Zon.com. This is complete madness. Any image you upload to any website can now embed a URL on Safari!

Naturally, we then started investigating what kind of URLs it would recognise. Normally I'd fuzz the URLs but this was quite difficult because you had to hover over the image and click a menu, which made fuzzing awkward. So, I decided to use Photoshop and do some manual testing. The first thing I tried was to see if protocols were recognised - it seemed to allow http and https, but not javascript or file. I then tested to see if it would allow query string parameters. Of course it did. So you could embed a XSS payload inside an image, and Safari would happily parse it and allow you to click it. Although JavaScript URLs didn't work, I started to look for ways to bypass this restriction.

The first thing I did was to try and make the JavaScript URL look like a protocol:

javascript://alert(1).com

This was parsed and the quick look menu showed, but didn't allow you to click the URL. I then tried to make the JS URL look more like a regular URL:

http://javascript://hackvertor.co.uk

This also failed, but then I tried this:

http://javascript:1337//location.href=123

That seemed to be clickable but I couldn't find the server message, and the URL bar was showing the JavaScript URL. What was happening? Safari was visiting a HTTP URL, but stripping the protocol which left the JavaScript protocol. That means when you refresh, the JavaScript URL will be activated. After many more attempts I optimised the payload:

When you hover over the above image, Safari will allow you to click it in the quick look menu. When you've clicked the link you get a server error message, but hitting refresh will execute the JavaScript in the context of "safari-resource". There is a caveat however - you need to enable JavaScript in the "Smart search field" in the developer menu. Caveat aside though, this is still  one crazy feature as I'm pretty sure you don't want any image to be able to embed JavaScript URLs or link to random websites!

Anyway, I'm off to register Zon.com.

Hot-linking

Safari

Back to all articles
