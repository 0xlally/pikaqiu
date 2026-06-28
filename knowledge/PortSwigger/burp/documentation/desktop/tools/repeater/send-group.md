# Sending grouped HTTP requests

Source: https://portswigger.net/burp/documentation/desktop/tools/repeater/send-group
Fetched: 2026-06-28T09:16:07.916820+00:00

Support Center

Documentation

Desktop editions

Tools

Repeater

Sending grouped HTTP requests

ProfessionalCommunity Edition

Sending grouped HTTP requests

Last updated:

June 18, 2026

Read time:

3 Minutes

Burp Repeater's Group send options feature enables you to send grouped HTTP requests with a single click. You can send requests either in parallel (all at once), or in sequence (one after the other).

To send a group of requests:

Create a Repeater tab group and add the relevant tabs to it. For more information, see Managing tab groups.

Alternatively, you can create a group and duplicate tabs within it. This can be helpful if you're testing for race condition vulnerabilities as it makes the process of creating identical requests much more efficient.

Select one of the tabs in the group.

Click the drop-down arrow by the side of the Send button and select one of the available options:

Send group in sequence (single connection)

Send group in sequence (separate connections)

Send group in parallel

Click Send group. Repeater sends all of the requests from the grouped tabs.

Note

Professional To quickly send identical requests without manually creating and grouping tabs, you can use custom actions. For example, the

Trigger race conditions custom action sends parallel requests with a single click.

For more information about how to use custom actions, see Custom actions.

Sending requests in sequence

You can send requests in sequence using either a single connection or multiple connections.

To cancel the send sequence, click Cancel on one of the group's tabs while the requests are being sent.

Sending over a single connection

If you select Send group in sequence (single connection), Repeater establishes a connection to the target, sends the requests from all of the tabs in the group, and then closes the connection.

Sending requests over a single connection enables you to test for potential client-side desync vectors. It also reduces the "jitter" that can occur when establishing TCP connections. This is useful for timing-based attacks that rely on being able to compare responses with very small differences in timings.

Related pages

For more information on how to test for client-side desync vectors, as well as some deliberately vulnerable labs for you to practice on, see the Browser-powered request smuggling Web Security Academy topic.

Sending over separate connections

If you select Send group in sequence (separate connections), Repeater establishes a connection to the target, sends the request from the first tab, and then closes the connection. It repeats this process for all of the other tabs in the order they are arranged in the group.

Sending requests over separate connections makes it easier to test for vulnerabilities that require a multi-step process.

Send in sequence prerequisites

To send a sequence of requests, the group must meet the following criteria:

There must not be any WebSocket message tabs in the group.

There must not be any empty tabs in the group.

There are also some additional criteria to send over a single connection:

All tabs must have the same target.

All tabs must use the same HTTP version (that is, they must either all use HTTP/1 or all use HTTP/2).

Sending requests in parallel

If you select Send group in parallel, Repeater sends the requests from all of the group's tabs at once. This is useful as a way to identify and exploit race conditions.

More information

For more information on testing for race conditions, see the Race conditions Web Security Academy topic.

Repeater synchronizes parallel requests to ensure that they all arrive in full at the same time. It uses different synchronization techniques depending on the HTTP version used:

When sending over HTTP/1, Repeater uses last-byte synchronization. This is where multiple requests are sent over concurrent connections, but the last byte of each request in the group is withheld. After a short delay, these last bytes are sent down each connection simultaneously.

When sending over HTTP/2+, Repeater sends the group using a single packet attack. This is where multiple requests are sent via a single TCP packet.

When you select a tab containing a response to a parallel request, an indicator in the bottom-right corner displays the order in which that response was received within the group (for example, 1/3, 2/3).

Note

You cannot send macro requests in parallel. This is to prevent macros from interfering with request synchronization.

Send in parallel prerequisites

To send a group of requests in parallel, the group must meet the following criteria:

All requests in the group must use the same host, port, and transport layer protocols.

HTTP/1 keep-alive must not be enabled for the project.

More information

Repeater settings.

Network settings.
