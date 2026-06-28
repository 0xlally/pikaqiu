# HTTP/2 basics for Burp users

Source: https://portswigger.net/burp/documentation/desktop/http2/http2-basics-for-burp-users
Fetched: 2026-06-28T09:15:51.104230+00:00

Support Center

Documentation

Desktop editions

HTTP/2

HTTP/2 basics for Burp users

ProfessionalCommunity Edition

HTTP/2 basics for Burp users

Last updated:

June 18, 2026

Read time:

3 Minutes

In this section, we'll provide a brief overview of some of the fundamentals of HTTP/2. We'll focus exclusively on the parts that are relevant to Burp. A basic understanding of these background concepts will help you get the most out of Burp's one-of-a-kind features for working with HTTP/2-exclusive attack vectors.

Binary protocol

As an HTTP/1 request is a single, text-based entity, servers have to use string operations to identify and extract the data they need based on a series of special delimiter characters. For example, each header is separated by a newline, while the name and value are separated by a colon.

Although Burp displays HTTP/2 requests in two different, human-readable forms, under the hood, they actually use a binary format. This means that servers can read the data from the request based on predetermined offsets. In other words, the point where each piece of information starts and ends is clearly defined, so there's no need for delimiter characters.

As a result, newlines, colons, and the like have no special meaning within an HTTP/2 request and can be injected in ways that are not possible in HTTP/1. For example, HTTP/2 header names and values are technically able to hold newline characters. Although this is officially prohibited according to the specification, by working with the Inspector, you can take advantage of the fact that some servers tolerate this anyway. This is the foundation for a number of HTTP/2-exclusive attacks and some of our latest research.

Frames

On the wire, HTTP/2 messages are sent as one or more separate "frames". The headers frame is equivalent to the request line and headers section of an HTTP/1 request. This may be followed by a number of data frames that contain the message body data.

For simplicity, we don't display the individual frames of HTTP/2 messages in Burp. We combine them to form a single request or response for you to work with.

Message length

Each frame of an HTTP/2 message is preceded by an explicit length field that tells the server how many bytes to read in. Therefore, servers can easily work out the overall length of the message by simply calculating the sum of its frame lengths.

This is far simpler and more robust than the Content-Length or Transfer-Encoding mechanism used in HTTP/1.

Header capitalization

In HTTP/1, header names are typically case insensitive. In HTTP/2, sending uppercase letters in a header name is technically possible, but it may lead to the request being rejected by the server as this does not conform to the HTTP/2 specification.

Pseudo-headers

In HTTP/2, a series of "pseudo-headers" is used to send key information about the message. Most notably, several pseudo-headers effectively replace the HTTP/1 request line and status line.

In total, there are five pseudo-headers:

:method - The HTTP method of the request, such as GET or POST.

:path - The request path. Note that this includes the query string.

:authority - Roughly equivalent to the Host header in HTTP/1.

:scheme - The request scheme, typically http or https. Note that there is no equivalent in HTTP/1.

:status - The response status code.

According to the specification, all pseudo-headers should be sent before any ordinary headers. Burp sends these pseudo-headers in a fixed order unless you manually override this in the Inspector.

When referring to pseudo-headers, it's common practice to prefix their names with a colon to help differentiate them from normal headers. Note that this is just one way of presenting this information in a human-readable format. On the wire, these names are just binary bytes and don't actually contain a colon.
