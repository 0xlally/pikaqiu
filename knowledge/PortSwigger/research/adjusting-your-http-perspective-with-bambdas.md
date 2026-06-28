# Refining your HTTP perspective, with bambdas

Source: https://portswigger.net/research/adjusting-your-http-perspective-with-bambdas
Fetched: 2026-06-28T09:17:20.097551+00:00

Refining your HTTP perspective, with bambdas

James Kettle

Director of Research

@albinowax

Published: Wednesday, 29 May 2024 at 13:31 UTC

Updated: Wednesday, 29 May 2024 at 15:03 UTC

When you open a HTTP request or response, what do you instinctively look for? Suspicious parameter names? CORS headers? Some clue as to the request's origin or underlying purpose?

A single HTTP message can tell a different story to every viewer, but modern websites send thousands so it's all too easy to overlook something critical. To help, Burp Suite recently added support for custom columns which let you personalize which elements of HTTP requests get surfaced in tables. Here's a simple example which parses the GraphQL operation out of the request body and into a column:

Behind the scenes, these are crafted using code-snippets called bambdas. This feature is almost paralyzingly powerful, so we thought we'd share some of the columns our research team has created. These range from simple but useful to not so simple. Readers already familiar with Java may notice that we haven't bothered avoiding null pointer exceptions - that's because they're handled for us at the row-level, and therefore don't tend to cause issues.

What page did this request originate from?

Understanding the flow of HTTP request sequences is crucial to finding many advanced vulnerabilities, and this makes it slightly easier.

return requestResponse.request().headerValue("Referer");

What webserver did this response come from?

Perhaps I have an WAF bypass or a cache poisoning attack that targets a specific proxy.

return requestResponse.response().headerValue("Server");

What's the HTTP version?

Should I prioritise request smuggling, or race conditions? How long will my 10,000-word directory bruteforce take?

return requestResponse.request().httpVersion();

Who owns the IP address this request is going to?

Maybe I should target their infrastructure instead. Reverse DNS is a wonderful thing.

String ipAddress = requestResponse.httpService().ipAddress();

return java.net.InetAddress.getByName(ipAddress).getCanonicalHostName();

Is this in-scope?

You wouldn't want to accidentally target something out of scope

return requestResponse.request().isInScope();

What's this request's GraphQL operation name?

You can usually tell a request's operation at a glance by looking at the URL, but GraphQL is an inconvenient exception. This script fixes that.

String paramName = "operationName";

if(requestResponse.request().hasParameter(paramName, HttpParameterType.JSON)) {

return requestResponse.request().parameterValue(paramName, HttpParameterType.JSON);

}

String query = requestResponse.request().parameterValue("query", HttpParameterType.JSON);

if(query.contains("{") || query.contains("(")) {

var queryParts = query.split("\\{|\\(");

return queryParts[0];

}

return "";

How does the session cookie look after a base64 decode?

Encoded, signed tokens like JWT are everywhere, and always worth peering into. This script will need to be customised to your target.

if (!requestResponse.hasResponse()) {

return "";

}

var extract = "session";

var response = requestResponse.response();

var optionalCookie = response.cookies().stream().filter(cookie -> cookie.name().equals(extract)).findFirst();

if(optionalCookie.isEmpty()) return "";

var value = optionalCookie.get().value();

var parts = value.split("\\.");

if(parts.length != 3) return "";

var payload = parts[1];

return utilities().base64Utils().decode(payload, Base64DecodingOptions.URL);

Which cookies have SameSite disabled?

When plotting a CSRF or XSS attack, it's useful to know if any cookies have SameSite disabled.

if(requestResponse.response() == null) {

return "";

}

if(!requestResponse.response().hasHeader("Set-Cookie")){

return "";

}

ArrayList<String> cookieNames = new ArrayList<>();

Pattern pattern = Pattern.compile("^ ([^=]+).+; SameSite=None", Pattern.CASE_INSENSITIVE);

List<HttpHeader> headers = requestResponse.response().headers();

for(HttpHeader header : headers) {

Matcher matcher = pattern.matcher(header.value());

while(matcher.find()) {

cookieNames.add(matcher.group(1));

}

}

return String.join(", ", cookieNames);

Does this response have bad CSP?

This custom column Bamda allows you to prioritise testing of vulnerable endpoints that have deployed unsafe CSP directives such as unsafe-inline or unsafe-eval.

if(requestResponse.response() == null) {

return "";

}

if(!requestResponse.response().hasHeader("Content-Security-Policy")) {

return "No CSP";

}

String csp = requestResponse.response().headerValue("Content-Security-Policy");

ArrayList<String> vulnerableDirectives = new ArrayList<>();

String[] directivesToCheck = new String[]{"unsafe-inline", "unsafe-eval"};

for(int i=0;i<directivesToCheck.length;i++) {

if(csp.contains(directivesToCheck[i])) {

vulnerableDirectives.add(directivesToCheck[i]);

}

}

return String.join(", ", vulnerableDirectives);

Prioritization via sorted custom columns

You can sort an entire table via a custom column, which can help prioritise which requests to target. Over time, I think I'll personally end up writing a giant bambda which scores how hackable a request is from 0-100 but for now, here's two simple examples:

How many parameters does this request have?

Sometimes, you just want to find the biggest attack surface as quickly as possible.

return requestResponse.request().parameters().size();

How many occurrences of 'HTTP_' does the response have?

This can indicate an environment variable leak, or be adapted to find various other interesting strings.

if (!requestResponse.hasResponse()) {

return 0;

}

String lookFor = "HTTP_";

return utilities().byteUtils().countMatches(requestResponse.response().body().getBytes(), lookFor.getBytes());

Execute a shell command

Maybe next time

bambdas

Back to all articles
