# Enumerating identifiers

Source: https://portswigger.net/burp/documentation/desktop/tools/intruder/uses/enumerating
Fetched: 2026-06-28T09:16:05.232351+00:00

Support Center

Documentation

Desktop editions

Tools

Intruder

Uses

Enumerating identifiers

ProfessionalCommunity Edition

Enumerating identifiers

Last updated:

June 18, 2026

Read time:

2 Minutes

Web applications often use identifiers to refer to items of data or resources, such as:

Usernames and passwords.

Document IDs.

Account numbers.

You can use Burp Intruder to enumerate valid or interesting identifiers from a large number of potential items.

Step 1: Find a request

Find a request that contains an identifier in a parameter, and that has a response with interesting data about the identifier.

Step 2: Set a payload position

Configure a single payload position at the parameter's value.

Step 3: Set a payload type

Use a suitable payload type to generate potential identifiers to test, using the correct format or scheme. Start the attack.

Step 4: Analyze the results

Sort the attack results based on various attributes to identify any anomalous results. This will allow you to infer valid identifiers. For example, a valid identifier may return a different HTTP status code.

Note

If a valid identifier returns a response containing a specific expression, you can define a match grep item to identify responses that contain this expression. For example, you could search for phrases such as "password incorrect" or "login successful" to locate successful logins. For more information, see Burp Intruder attack settings.

Use cases

You can configure your attack to enumerate a huge variety of identifiers, for example:

Enumerate usernames - Use the username generator payload type to insert a long list of possible usernames

into an application's login failure message.

Enumerate passwords - Use the simple list payload type to insert a set of common passwords into an application's

login failure message, alongside known valid usernames.

Enumerate order IDs - Use the custom iterator payload type to cycle through potential order IDs in a known format.

You can then use these to view order details.

Enumerate session tokens - Use the bit flipper payload type to systematically modify a token that has been encrypted using a CBC cipher, to try to meaningfully tamper with its decrypted value.

Related pages

For more information on the payload types listed above, see Payload types.

For a basic tutorial that demonstrates how to enumerate login details, see Getting started with Burp Intruder.

For a more advanced tutorial, see Enumerating subdomains using Burp Intruder.

For a tutorial that requires you to use a cluster bomb attack type to simultaneously enumerate username and password details, see Brute-forcing a login

mechanism using Burp Intruder.
