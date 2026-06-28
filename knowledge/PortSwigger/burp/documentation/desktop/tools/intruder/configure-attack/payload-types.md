# Burp Intruder payload types

Source: https://portswigger.net/burp/documentation/desktop/tools/intruder/configure-attack/payload-types
Fetched: 2026-06-28T09:16:04.318693+00:00

Support Center

Documentation

Desktop editions

Tools

Intruder

Configure attack

Payload types

ProfessionalCommunity Edition

Burp Intruder payload types

Last updated:

June 18, 2026

Read time:

15 Minutes

You can set the type of payload that you want to inject into the base request. Burp Intruder provides a range of options for auto-generating different types of payload, or you can use a simple wordlist.

To select a payload type, choose an option from the Payload type drop-down menu in the Payloads side panel. You can open or close the side panel by clicking the Payloads tab.

Related pages

Professional You can use predefined payload lists with many of the payload types. For more information, see Predefined payload lists.

Payload configuration

You can customize each payload type in the Payload configuration field. Many payload types include the following basic configuration options:

Paste - Insert a list from your clipboard.

Load - Load a list from a file.

Remove - Delete the highlighted item.

Clear - Delete all items in the list.

Deduplicate - Remove duplicate entries from your list. This increases the efficiency of your attacks by reducing the

number of requests that are sent.

Add - Enter a new item.

Add from list - Add a predefined payload list.

Simple list

This enables you to configure a simple list of strings that are used as payloads.

Runtime file

This enables you to configure a file from which to read payload strings at runtime.

You can use this payload type when a very large list of payloads is needed, to avoid holding the entire list in memory. One payload is read from each line of the file, hence payloads may not contain newline characters.

Custom iterator

This enables you to generate payloads using permutations of characters or other items according to a given template.

You can define up to eight different positions in the template, and set each position with a list of items. You can use a separator between any positions. For example, you could set up an attack to iterate through all possible permutations of the template AA/11, with the first two positions cycling through A - Z, and the second two positions cycling through 0 - 9. This could be useful if, for example, a payroll application identifies individuals using a number of the form AA/11.

There are various ways to edit the list items:

To remove configuration from all positions of the custom iterator, click Clear all.

To select a preconfigured setup for the custom iterator, click on the Preset schemes drop-down menu and select a scheme. The scheme can then be modified. You can choose from:

Directories / file . extensions - Generate URLs.

Two-digit hex - Generate hexadecimal numbers.

Passwords + digit - Generate an extended wordlist for password guessing attacks.

Character substitution

This enables you to apply character substitutions to each item in a list of strings.

You can use character substitution in password guessing attacks, for generating common variations on dictionary words.

The subsequent attack uses all permutations of substituted characters for each list item in turn. For example, for the substitutions e > 3 and t > 7, the item "peter" will generate the following payloads:

peter

p3ter

pe7er

p37er

pet3r

p3t3r

pe73r

p373r

Case modification

This enables you to apply case modifications to each item in a list of strings.

You can use case modification in password guessing attacks, for generating case variations on dictionary words.

The subsequent attack adjusts the case of characters within each item in turn. Duplicate payloads are discarded. You can select from a range of case modification options:

No change - No modification.

To lower case - All letters are converted to lower case.

To upper case - All letters are converted to upper case.

To Propername - The first letter is converted to upper case, and subsequent letters are converted to lower case.

To ProperName - The first letter is converted to upper case, and subsequent letters are not changed.

For example, if all modification options are selected, the item "Peter Wiener" will generate the following payloads:

Peter Wiener

peter wiener

PETER WIENER

Peter wiener

Recursive grep

This enables you to extract text from the response to the previous request, and use it as the payload for the current request.

You can use this payload type when you need to work recursively to extract useful data or deliver an exploit. For example, to extract the contents of a database via SQL injection by recursively injecting queries of the form:

UNION SELECT name FROM sysobjects WHERE name > 'a'

The server's error message discloses the name of the first database object:

Syntax error converting the varchar value 'accounts' to a column of data type int.

The query is then repeated using "accounts" to identify the next object. This task can be easily automated using recursive grep payloads to quickly list all objects within the database.

The following settings must be configured:

Initial payload for first request - Enter an initial payload. This is used to generate the first request and response.

Extract grep item - Select an extract grep item. This is used to extract an interesting part of the previous response, which is then used to derive further payloads. For instructions on how to define an extract grep item, see Burp Intruder attack settings.

Stop if duplicate payload found - Stop the attack when the same payload is derived twice in succession. This normally indicates that the exercise is complete.

Note

Attacks using the recursive grep payload type must use a resource pool with a max concurrent request of 1. For more information on resource pools, see Intruder resource pools.

Illegal Unicode

This enables you to generate payloads from a list of items by replacing a specified character with illegal Unicode-encodings of another character.

You can use this payload type to attempt to bypass filters designed to block certain characters. For example, defenses against file path traversal attacks which match on expected encodings of the ../ and ..\ sequences.

The available settings are described below:

Overlong UTF-8 encodings

You can specify whether overlong encoding is used, and set a maximum length of up to 6 bytes.

This allows you to represent basic ASCII characters (0x00 - 0x7F) in the Unicode scheme. They are usually correctly represented using a single byte.

Illegal UTF-8 continuation bytes

Do illegal UTF-8 - Generate three additional encodings for each continuation byte in turn, when the maximum overlong UTF-8 length is set to two bytes or more.

Three illegal variants of each continuation byte are possible, with the binary forms 00xxxxxx, 01xxxxxx and 11xxxxxx. This is because, when a character is encoded with more than one byte, the bytes following the first take the binary form 10xxxxxx, to designate that they are continuation bytes. However, the most significant bits of the first byte also identify how many continuation bytes will follow, so Unicode decoding routines may ignore the first two bits of continuation bytes.

Maximize permutations in multi-byte encodings - Modify more than one continuation byte simultaneously, when you have selected Do illegal UTF-8 and a maximum overlong UTF length of three bytes or more. This generates all permutations of illegal variants for continuation bytes. You can use this to attempt to circumvent advanced pattern-matching controls, by generating a much larger number of different illegal encodings.

Illegal hex characters

These settings control how the generated byte sequences are represented using hexadecimal notation:

Do illegal hex - When the list of illegally-encoded items has been generated using overlong encodings and illegal variants of continuation bytes (if selected), it is possible to modify the hexadecimal encoding of the resulting byte sequences to confuse certain pattern-matching controls. Hex encoding uses the characters A - F to represent the decimal values 10 - 15. However, some hex decoders interpret, for example, G as decimal 16 and H as decimal 17. So 0x1G may be interpreted as decimal 32. Further, if illegal hex characters are used in the first position of a two digit hex code, then the resulting decoding overflows the maximum value of a single byte, and in this situation some hex decoders only use the 8 least significant bits of the resulting number. So 0xG1 may be decoded as decimal 257, which is then interpreted as decimal 1. Each legal two-digit hex code has between 4 and 6 corresponding illegal hex representations which are interpreted as that same hex code if decoded as described above. If the Do illegal hex setting is selected, then Burp will generate all possible illegal hex encodings of each byte in the list of illegally-encoded items.

Maximize permutations in multi-byte encodings - Modify more than one byte simultaneously, when you have selected Do illegal hex, and a maximum overlong UTF-8 length of two bytes or more. This generates all permutations of illegal hex for all bytes. You can use this to attempt to circumvent advanced pattern-matching controls, by generating a much larger number of different illegal encodings.

Hex formatting

These settings control the appearance of hex-encoded payloads:

Use lower case alpha characters - Specify whether lower or upper case alphabet characters are used in hex codes.

Add % prefix before each byte - Insert the % character before each two-digit hex code, to effectively URL-encode the generated payloads.

Total encodings

This setting enables you to:

View a best estimate for the number of encodings, based on the rest of the configuration.

Specify a ceiling on the number of illegal encodings that will be generated.

This can be useful if large overlong encodings are being used or maximum permutations have been selected, as these settings may generate huge numbers of illegal encodings.

Match / replace in list items

These settings control the replacement of characters within list items:

Match character - Specify the character that will be replaced within each list item. Use a dummy character such as * in your list items, to indicate where replacements should occur.

Replace with encodings of - Specify the character for which illegal encodings will be derived, to replace the original match character within each list item. This setting can be specified using the ASCII character itself, or the two-digit hex code for the character. This is useful for specifying non-printable ASCII characters, such as null.

Character blocks

This enables you to generate payloads based on blocks of a specified character or string.

You can use this payload type to:

Detect buffer overflow and other boundary condition vulnerabilities in software running in a native (unmanaged) context.

Exploit some logic flaws where input of a particular length bypasses input filters or triggers an unexpected code path.

The following settings are available:

Base string - The input string, from which the character blocks will be generated..

Min length - The base string is multiplied by this number to generate the smallest block.

Max length - The base string is multiplied by this number to generate the largest block.

Step - The increment in the length of each character block.

Numbers

This enables you to generate numeric payloads within a given range and in a specified format.

Number range

You can configure various aspects of the number range:

Type - Specify whether numbers are generated sequentially, or at random.

From - Specify the first number that is generated sequentially. Otherwise, the smallest number that may be randomly generated.

To - Specify the last number that is generated sequentially, or nearest lower increment of the step value. Otherwise, the largest number that may be randomly generated.

Step - Specify the increment between sequentially generated successive numbers. The value may be negative, in which case the numbers generated will step downwards.

How many - The number of payloads that will be randomly generated. Note that duplicate payloads may be generated.

Note

If you need to cycle through a range of numbers containing many total digits (more than approximately 12), then it is more reliable to use your payload markers to highlight a sub-portion of the larger number within the attack template, and generate numeric payloads containing correspondingly fewer digits.

This is because Burp uses double-precision floating point numbers for both the number range configuration and the internal state of the payload generator at runtime. Some loss of precision is to be expected when dealing with very large numbers or very precise fractional numbers.

Number format

You can also configure various aspects of the number format:

Base - Specify whether numbers are generated in decimal or hexadecimal form.

Min integer digits - Set the minimum number of integer digits each number will have. Numbers with fewer integer digits are padded with zeros on the left hand side.

Max integer digits - Set the maximum number of integer digits each number will have. Numbers with more integer digits are truncated, losing their most significant integer digits.

Min fraction digits - Set the minimum number of fraction digits (after the decimal point) each number will have. Numbers with fewer fraction digits are padded with zeros on the right hand side. Only available when generating decimal numbers.

Max fraction digits - Set the maximum number of fraction digits (after the decimal point) each number will have. Numbers with more fraction digits are truncated, losing their least significant fraction digits. Only available when generating decimal numbers.

To indicate that no minimum or maximum size should be enforced, leave any of the digit settings blank.

As you edit the number format, example numbers with the minimum and maximum number of digits are shown.

Dates

This enables you to generate date payloads within a given range and in a specified format.

You can use this payload type for:

Data mining, for example, trawling an order book for entries placed on different days.

Brute forcing, for example, guessing the date of birth component of a user's credentials.

The following settings are available:

From - Set the first (and earliest) date that will be generated.

To - Set the value of the last (and latest) date that will be generated (or the nearest lower increment of the step value).

Step - Set the increment between successive dates, in days, weeks, months or years. It must be a positive value.

Format - Set the format in which the dates should be represented. Several predefined date formats can be selected, or a custom format can be entered. The examples below illustrate the syntax that can be used to specify custom date formats.

E

Sat

EEEE

Saturday

d

7

dd

07

M

6

MM

06

MMM

Jun

MMMM

June

yy

03

yyyy

2003

/ . :

/ . :

Brute forcer

This enables you to generate payloads of specified lengths that contain all permutations of a specified character set.

The following settings are available:

Character set - Specify the set of characters to be used in the payloads. Note that the total number of payloads increases exponentially with the size of this set.

Min length - Set the length of the shortest payload.

Max length - Set the length of the longest payload.

Null payloads

This enables you to generate payloads whose value is an empty string. You can use this to repeatedly issue the base request unmodified - you don't need to configure payload positions.

You can use this payload type for a variety of attacks, for example:

Harvesting cookies for sequencing analysis.

Application-layer denial-of-service attacks where requests are repeatedly sent which initiate high-workload tasks on the server.

Keeping alive a session token that is being used in other intermittent tests.

You can generate a specified number of null payloads, or continue indefinitely.

Character frobber

This enables you to modify the value of each character position of an input. The input could be the base value of each payload position, or a specified string. The attack cycles through each item in turn, one character at a time, incrementing the ASCII code of that character by one.

You can use this payload type to test which parameter values, or parts of values, have an effect on the application's response. For example, you can use it to test which parts of a session token track session state. If you modify the value of an individual character within the token, and your request is still processed within your session, then it is likely that this character is not used to track your session.

Bit flipper

This enables you to modify the value of each bit position of an input. The input could be the base value of each payload position, or a specified string. It cycles through each item, one character at a time, flipping each specified bit in turn.

The following settings are available:

Operate on - Specify whether to operate on the base value of the payload position, or on another string.

Format of original data -Specify whether the generator should operate on the literal value of the original data, or treat it as ASCII hex (explained further below).

Select bits to flip - Specify which bits in each byte should be flipped, through from the least significant bit (0000000X) through to the most significant bit (X0000000).

For example, if the base value is "ab" then operating on the literal string and flipping all bits will result in the following payloads:

`b

cb

eb

ib

qb

Ab

!b

áb

ac

a`

af

aj

ar

aB

a"

aâ

Whereas treating "ab" as an ASCII hex string and flipping all bits will result in the following payloads:

aa

a9

af

a3

bb

8b

eb

2b

You can use the Bit flipper in similar situations to the Character frobber, but where you need finer-grained control. For example, if session tokens or other parameter values contain meaningful data encrypted with a block cipher in CBC mode, it may be possible to change parts of the decrypted data systematically by modifying bits within the preceding cipher block. You can use this payload type to determine the effects of modifying individual bits within the encrypted value.

Username generator

This enables you to derive potential usernames from a list of names or email addresses, using various common schemes.

This payload type is useful if you are targeting a particular human user, and you do not know the username or email address scheme in use within an application.

For example, supplying the name "peter wiener" results in up to 115 possible usernames:

peterweiner

peter.wiener

wienerpeter

wiener.peter

peter

wiener

peterw

peter.w

wpeter

w.peter

pwiener

p.wiener

wienerp

wiener.p

...

You can configure a maximum number of payloads to generate per item in the list.

ECB block shuffler

This enables you to shuffle blocks of ciphertext in ECB-encrypted data, to modify the decrypted cleartext and potentially interfere with application logic.

Because ECB ciphers encrypt each block of plaintext independently of others, identical blocks of plaintext encrypt into identical blocks of ciphertext (provided the same key is used), and vice versa. Hence, it is possible to shuffle blocks within a large piece of ciphertext with the effect of shuffling the corresponding blocks of decrypted plaintext. In some data (such as a structured session token with fields for username, user ID, role, and a timestamp) it may be possible to meaningfully alter the content of the decrypted data so as to interfere with application processing, and carry out unauthorized actions.

The following settings are available:

Encrypted data to shuffle - Select whether to operate on the base value of the payload position, or on another string.

Format of original data - Select whether the generator should operate on the literal value of the original data, or should treat it as ASCII hex (see the Bit

flipper payload type for more details).

Block size - Set the size of the encrypted blocks in bytes. In most cases, the blocks are 8 or 16 bytes in size. If you are unsure, run the attack multiple times using each block size that might be in use.

Additional encrypted strings - Supply a list of encrypted strings that use the same cipher and key, to provide additional blocks for shuffling into the encrypted data. Because successful attacks of this type often require a considerable degree of luck, in terms of finding a block with a suitable plaintext value that can be shuffled into the correct point in the structure, the odds of success are frequently improved by obtaining a large sample of strings that have been encrypted by the same application function. For example, if you are attacking a session token using this payload type, it would be beneficial to harvest a large number of other session tokens from the application, to provide additional blocks of ciphertext.

Extension-generated

This enables you to invoke a Burp extension to generate payloads.

Click Select generator ... to select an extension-provided payload generator from the list. The extension must be registered as an Intruder payload generator.

Copy other payload

This enables you to copy the value of the current payload to another payload position.

This payload type can be useful in various situations, for example:

When two different parameters must always have the same value in order to hit a target code path (for example, fields for new and confirm passwords), and you want to use the cluster bomb attack type to manipulate other parameters at the same time.

When one parameter value in the request contains a checksum of another parameter value, which is normally computed by a client-side script based on user input.

Note

This payload type enables you to copy the literal value of the payload, but you can also systematically derive the current payload from the value of a payload at another position. To do this, define an appropriate

payload processing rule.

Collaborator payloads

This generates and injects Burp Collaborator payloads. Each Collaborator payload includes a unique identifier that is a subdomain of the Collaborator server's domain. When certain vulnerabilities occur, the target application may use the injected payload to interact with the Collaborator server.

Select Include Collaborator server location to include the full Collaborator server address in your payloads. If this is not selected, only the Collaborator identifier is included.

If you use this payload type, you can view the details of any interactions with the Collaborator server in the attack results window.

Note

Interactions are not shown in the Collaborator tab. To identify any deferred interactions with the Collaborator server, save the attack and monitor the

Event log on the Dashboard.
