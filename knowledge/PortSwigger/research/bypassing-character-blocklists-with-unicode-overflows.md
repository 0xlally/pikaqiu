# Bypassing character blocklists with unicode overflows

Source: https://portswigger.net/research/bypassing-character-blocklists-with-unicode-overflows
Fetched: 2026-06-28T09:17:21.257604+00:00

Bypassing character blocklists with unicode overflows

Gareth Heyes

Researcher

@garethheyes

Published: Tuesday, 28 January 2025 at 13:58 UTC

Updated: Wednesday, 29 January 2025 at 08:10 UTC

Unicode codepoint truncation - also called a Unicode overflow attack - happens when a server tries to store a Unicode character in a single byte. Because the maximum value of a byte is 255, an overflow can be crafted to produce a specific ASCII character.

Here are a couple of examples that end with 0x41 which represents A:

0x4e41 0x4f41 0x5041 0x5141

If you perform a modulus operation on the code points above you'll see they produce the character "A":

String.fromCodePoint(0x4e41 % 256, 0x4f41 % 256, 0x5041 % 256, 0x5141 % 256) // AAAA

It's not only bytes that have this problem, JavaScript itself has a codepoint overflow in the fromCharCode() method. This method allows you to generate a character between 0-0xffff but if you go above this range it will be overflowed and produce a character by the overflow amount.

String.fromCharCode(0x10000 + 0x31, 0x10000 + 0x33, 0x10000 + 0x33, 0x10000 + 0x37)

//1337

The above code uses the hex value 0x10000 which is one above the maximum codepoint supported by the fromCharCode() method. Then I add an overflow to it, in this case the hex for each codepoint of 1337. Then when the overflow occurs it produces 1337.

This is being actively used by bug bounty hunters and was brought to our attention by Ryan Barnett. For everyone's convenience we've added these truncation attacks to ActiveScan++, thanks to Ryan for the PR and we've created a Hackvertor tag to help reproduce the characters. Big thanks to my colleague Zak who I investigated this with. We've also updated the Shazzer unicode table to display potential unicode truncation characters.

micropost

Unicode

Back to all articles
