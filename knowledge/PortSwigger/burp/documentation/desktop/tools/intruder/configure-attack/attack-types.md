# Burp Intruder attack types

Source: https://portswigger.net/burp/documentation/desktop/tools/intruder/configure-attack/attack-types
Fetched: 2026-06-28T09:16:04.027385+00:00

Support Center

Documentation

Desktop editions

Tools

Intruder

Configure attack

Attack types

ProfessionalCommunity Edition

Burp Intruder attack types

Last updated:

June 18, 2026

Read time:

3 Minutes

To determine the way in which payloads are assigned to payload positions, you can specify an attack type. Attack types enable you to configure whether:

Payloads are taken from a single set, or multiple sets (up to 20).

Payloads are assigned to payload positions in turn, or simultaneously.

To select an attack type, click on the drop-down menu above the message editor.

Sniper attack

This attack places each payload into each payload position in turn. It uses a single payload set.

The total number of requests generated in the attack is the product of the number of positions and the number of payloads in the payload set.

The Sniper attack is useful for fuzzing a number of request parameters individually for common vulnerabilities.

Battering ram attack

This attack places the same payload into all of the defined payload positions simultaneously. It uses a single payload set.

The total number of requests generated in the attack is the number of payloads in the payload set.

The Battering ram attack is useful where an attack requires the same input to be inserted in multiple places within the request. For example, a username within a cookie and a body parameter.

Pitchfork attack

This attack iterates through a different payload set for each defined position. Payloads are placed into each position simultaneously. For example, the first three requests would be:

Request one:

Position 1 = First payload from Set 1.

Position 2 = First payload from Set 2.

Request two:

Position 1 = Second payload from Set 1.

Position 2 = Second payload from Set 2.

Request three:

Position 1 = Third payload from Set 1.

Position 2 = Third payload from Set 2.

The total number of requests generated in the attack is the number of payloads in the smallest payload set.

The Pitchfork attack is useful where an attack requires different but related input to be inserted in multiple places within the request. For example, to place a username in one parameter, and a known ID number corresponding to that username in another parameter.

Cluster bomb attack

This attack iterates through a different payload set for each defined position. Payloads are placed from each set in turn, so that all payload combinations are tested. For example, the first three requests would be:

Request one:

Position 1 = First payload from Set 1.

Position 2 = First payload from Set 2.

Request two:

Position 1 = First payload from Set 1.

Position 2 = Second payload from Set 2.

Request three:

Position 1 = First payload from Set 1.

Position 2 = Third payload from Set 2.

The total number of requests generated in the attack is the product of the number of payloads in all defined payload sets - this may be extremely large.

The Cluster bomb attack is useful where an attack requires unrelated or unknown input to be inserted in multiple places within the request. For example, when guessing both a username and password.

For a tutorial that uses a Cluster bomb attack, see Brute-forcing a login mechanism using Burp Intruder.
