# Harvesting useful data

Source: https://portswigger.net/burp/documentation/desktop/tools/intruder/uses/harvesting
Fetched: 2026-06-28T09:16:05.135065+00:00

Support Center

Documentation

Desktop editions

Tools

Intruder

Uses

Harvesting data

ProfessionalCommunity Edition

Harvesting useful data

Last updated:

June 18, 2026

Read time:

2 Minutes

You can use Burp Intruder to extract interesting data from an attack. This information enables you to focus on the most critical items, and can feed into future attacks.

Step 1: Find a request

Find a request that contains an identifier in a parameter, and that has a response with interesting data about the identifier.

Step 2: Set a payload position

Configure a single payload position at the parameter's value.

Step 3: Set a payload type

Use a suitable payload type to generate potential identifiers to test, using the correct format or scheme.

Step 4: Set an extract grep

Configure the Grep - extract settings to retrieve relevant data from each response. For more information on these settings, see Burp Intruder attack settings.

Step 5: Analyze the results

Sort the attack results by the extract grep expressions to identify any interesting information that has been extracted.

Professional To copy and paste the data for further analysis, control-click the header.

Use cases

You can configure your attack to harvest a wide range of useful data, for example:

Extract password hint - Insert a list of common usernames into an application's forgotten password function. Configure an extract grep item to retrieve the password hint for each user. You can then scan these to identify ones that are easily guessed.

Identify page title tags - Use the numbers payload type to cycle through page ID numbers. Configure an extract grep item to retrieve the HTML title tag for each page. You can then scan these to identify interesting pages.

Identify user roles - Insert a list of known usernames into an application's user profile page. Configure an extract grep item to retrieve the role for each user. You can then identify administrative accounts for further attacks.
