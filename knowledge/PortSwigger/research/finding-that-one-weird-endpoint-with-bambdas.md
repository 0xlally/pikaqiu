# Finding that one weird endpoint, with Bambdas

Source: https://portswigger.net/research/finding-that-one-weird-endpoint-with-bambdas
Fetched: 2026-06-28T09:17:25.213496+00:00

Finding that one weird endpoint, with Bambdas

James Kettle

Director of Research

@albinowax

Published: Tuesday, 12 December 2023 at 14:11 UTC

Updated: Tuesday, 12 December 2023 at 14:11 UTC

Security research involves a lot of failure. It's a perpetual balancing act between taking small steps with a predictable but boring outcome, and trying out wild concepts that are so crazy they might just work... but probably won't.

At PortSwigger Research, we've observed that making it easy to try out wild ideas is really valuable, because it minimises the cost of failure, encouraging ambitious experiments and leading to exciting discoveries.

We try many of our ideas out by coding custom Burp extensions, and running them on a 20gb project file which contains the homepage of ~every website that we're legally allowed to test. You can find more details on how we generate this project file in Cracking the Lens.

Burp Suite recently launched a powerful new feature called Bambdas that lets users code mini-extensions directly inside the proxy, complete with code-autocomplete, syntax-highlighting and instant evaluation. We quickly found that this made it even easier to mine the project file for vulnerabilities by eliminating the need to use a separate IDE and providing instant feedback.

We quickly ended up with a bunch of Bambdas for spotting HTTP endpoints exhibiting unusual behaviour - here's a few of our favourites which flagged at least one real website:

Large redirect responses

This Bambda will flag redirect responses with a body over 1000 bytes - this can indicate sites that forgot to terminate script execution when the user fails authentication, typically leading to information disclosure:

return requestResponse.hasResponse() &&

requestResponse.response().statusCode() <= 399 &&

requestResponse.response().statusCode() >= 300 &&

requestResponse.response().body().length() > 1000;

Responses with multiple </html> tags

What if a page fails to exit a script at the right point, but isn't serving a redirect response? In some cases this will result in the response containing multiple closing HTML tags. Our initial attempt to find these got a bunch of false positives from JavaScript files so we filtered those out by only showing responses with a HTML content-type. This approach revealed a page that we're pretty sure is meant to be behind authentication, and a completely unexpected source code leak.

return requestResponse.response().statedMimeType() == MimeType.HTML &&

utilities().byteUtils().countMatches(

requestResponse.response().body().getBytes(), "</html>".getBytes()) > 1;

Incorrect content-length

I love to exploit sketchy HTTP middleware and one thing some of the worst middleware does is inject extra content into responses but fail to correct the Content-Length. This one is super easy to detect:

int realContentLength = requestResponse.response().body().length();

int declaredContentLength = Integer.parseInt(

requestResponse.response().headerValue("Content-Length"));

return declaredContentLength != realContentLength;

Malformed HTTP header

Finally, I decided to look for responses containing a space in the header name. I wasn't really looking for anything in particular, and it yielded a bunch of servers running SMTP on port 443!

return requestResponse.response().headers().stream().anyMatch(

e -> e.name().contains(" "));

I'll pass you over to Gareth now for some of his.

Find all JSON endpoints with no or text/html mime type

I absolutely love Bambdas and as James mentioned they provide a quick way to easily test your proxy history and find interesting nuggets that have been missed by standard filtering. When writing a Bambda it's useful to have a question in mind. One of those questions was "What sites are still using an invalid content-type for JSON responses?". Browsers nowadays are pretty strict when it comes to content sniffing however, if a site declares a text/html mime type with JSON data HTML will be rendered of course! I wrote a couple of lines of code and in no time I was finding stuff that I didn't know existed in my massive project file.

if(!requestResponse.hasResponse()) {

return false;

}

var response = requestResponse.response();

if (response.hasHeader("Content-Type")) {

if (!response.headerValue("Content-Type").contains("text/html")) {

return false;

}

}

String body = response.bodyToString().trim();

boolean looksLikeJson = body.startsWith("{") || body.startsWith("[");

if(!looksLikeJson) {

return false;

}

return true;

Find all GraphQL endpoints

Next I need to find a lot of GraphQL endpoints for some testing I was doing. Using traditional filtering you can find common endpoints that for example contain /graphql, but what happens when you want to find endpoints that are not at a common location? This is where Bambdas come in, you can use a couple lines of Java to find parameters named "query" and the value contains a new line. Wham and there are a load of non-standard endpoints for testing!

var req = requestResponse.request();

if(!req.hasParameters()) {

return false;

}

var types = new HttpParameterType[]{

HttpParameterType.JSON, HttpParameterType.BODY, HttpParameterType.URL

};

for(HttpParameterType type: types) {

if(req.hasParameter("query", type)) {

var value = req.parameterValue("query", type);

if(type == HttpParameterType.JSON) {

if(value.contains("\\n")) {

return true;

}

} else {

if(value.toLowerCase().contains("%0a")) {

return true;

}

}

}

}

return false;

Find JSONP for CSP bypass

Let's say you've got XSS but the site is protected by CSP, what you need to do is find scripts on the site that you can control because the CSP allows "same site" script resources. You can easily do this with a Bambda! The next Bambda looks for JSONP endpoints. It first looks for a parameter that looks like a callback with 4 or more characters. Then it searches the response to see if it's reflected with an opening parenthesis. This was surprisingly effective and found lots of JSONP for me!

var req = requestResponse.request();

var res = requestResponse.response();

var paramRegex = Pattern.compile("^[a-zA-Z][.\\w]{4,}$");

if(res == null || res.body().length() == 0) return false;

if(!req.hasParameters()) return false;

var body = res.bodyToString().trim();

var params = req.parameters();

for(var param: params) {

var value = param.value();

if(param.type() != HttpParameterType.URL)continue;

if(paramRegex.matcher(value).find()) {

var start = "(?:^|[^\\w'\".])";

var end = "\\s*[(]";

var callbackRegex = Pattern.compile(start+Pattern.quote(value)+end);

if(callbackRegex.matcher(body).find())return true;

}

}

return false;

Conclusion

All these Bambdas put together represents under an hour of R&D time, enabling some really playful research. We're excited to see what the rest of the community unearths over the coming months, and we're building a curated repo of the best at https://github.com/PortSwigger/bambdas.

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
