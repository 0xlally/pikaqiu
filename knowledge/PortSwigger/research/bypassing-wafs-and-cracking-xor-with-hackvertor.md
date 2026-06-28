# Bypassing WAFs and cracking XOR with Hackvertor

Source: https://portswigger.net/research/bypassing-wafs-and-cracking-xor-with-hackvertor
Fetched: 2026-06-28T09:17:21.838098+00:00

Bypassing WAFs and cracking XOR with Hackvertor

Gareth Heyes

Researcher

@garethheyes

Published: Tuesday, 9 October 2018 at 14:53 UTC

Updated: Monday, 2 October 2023 at 14:38 UTC

You might not be aware of the Hackvertor extension I've been working on lately. It features tag based conversion that is far more powerful than the inbuilt decoder in Burp. The idea behind tag based conversion is that the tag transforms its contents then passes the conversion the next outer tag, which allows you to perform multiple levels of encoding easily.

For example, to encode a string to base64 you simply use the base64 tag:

<@base64_0>test<@/base64_0>

You can do multiple levels of encoding too, for instance let's say you wanted to convert a string to hex and then base64 encode it, you would first use the hex tag and then the base64 tag:

<@base64_1><@hex_0(" ")>test<@/hex_0><@/base64_1>

The hex tag has a separator argument that separates each hex string -  "test" will be passed to the tag function along with a space as a separator.

Using Hackvertor

When the extension loads it will create a new Tab in Burp called Hackvertor. In the tab there is an input box and an output box. You enter the text you want to convert in the input box and select it then click on a tag Hackvertor automatically runs convert and the conversion appears in the output box, there is a convert button for convenience in case you want to run the conversion again. There are tag categories such as Encode, Decode etc. that let you easily find the tag you're looking for. Hackvertor also has repeater style tabs that allow you to run multiple versions of the tool.

Bypassing the Cloudflare WAF

Recently I made Hackvertor tags available in actual requests in tools like repeater, you can simply right click in a repeater request and select the Hackvertor menu to add tags inside the request and before the request is sent it will automatically run conversions. You can also use them in Intruder too by first defining them in repeater and then sending them to Intruder, this is so powerful because you can use multiple levels of encoding using the placeholders. You can even use them in the proxy but this is turned off by default. If you want to turn that on you can select the Hackvertor menu in the main Burp menu and click "Allow tags in Proxy".

Now I'll show you how to use tags in the repeater to bypass the Cloudflare WAF. Send the following url to repeater: hxxps://wafproxy.net/xss/xss.php?x=

Then after the equals enter the following code:

<img/src/onerror=alert(1)>

Select the alert(1) in the repeater request then with the Hackvertor BApp enabled right click on the selected text and click Hackvertor then XSS and then throw_eval. This will add the tag to the request and if you hit go you'll see the response contains:

<img/src/onerror=window.onerror=eval;throw'=alert\x281\x29'>

If you want to check it actually works you just need to right click on the request editor and select Hackvertor from the context menu and Copy URL, this will then produce a URL after all tags have been converted. If you use Burp's copy URL command then this will only copy the URL with the tags in it.

Decoding rotN

It all started with a question from my daughter. I was wearing a BSides Manchester t-shirt from 2016 and it had some binary on the front of it and she asked "Daddy what do all those numbers mean?". I told her it was binary and asked if she wanted to decode it. We then started typing binary into Hackvertor, I noticed once the binary was decoded it was a base64 encoded string, then it looked like a rot encoded string. We bruteforced the rot encoded string and decoded the message but it got me thinking, what if Hackvertor could automatically decode a rot encoded string.

It would have to identify English like words from random gibberish. I started to create an is_like_english tag, at first I thought you could use bigrams and trigrams just look for common letters that follow them to determine English like words but it wasn't as simple as I thought. Then after Googling around I found a pretty awesome site. They used quadgrams a sequence of four letters and their frequency in the English language. The site also had some simple python code that generated a score based on analysis of the words and the quadgrams. I rewrote the code in Java and implemented it in Hackvertor.

The next step was to improve the auto decoder. The auto decoder is a tag that automatically tries to determine how a string is encoded and decodes it multiple times. I added a simple regex that looks for on or more a-z characters followed by spaces, commas or hyphens. Then looped 25 times to brute force the rot encoded string and got a score from each one, I calculated the average of each one and if the best score was greater than the average plus twenty it would automatically decode the rot encoded string. I won't tell you what the binary decoded to I'll let you find out for yourself. Here is a picture of the t-shirt modeled by Santi.

<@auto_decode_0>01010111 01101101 00110101 01101000 01100011 01001000 01010110 01111001 01011010 01101101 01100100 01111001 01011010 01010011 01000010 01000111 01100101 01101101 00110101 00110101 01100101 01010011 00110001 01000111 01100011 01000111 00110101 00110101 01100011 01101001 01000010 01010011 01100001 00110010 01001110 01111001 01011010 01011000 01011010 00110110 01100011 01101101 01000110 01101110 01100010 01101110 01101011 01100111 01010111 01101101 00110101 01110111 01100100 01011000 01011010 01101000 01100011 01100111 00111101 00111101<@/auto_decode_0>

James also had a speaker shirt with a different message so I entered into Hackvertor to see if it would auto decode the message. It worked, to see for yourself paste the following into the input box.

<@auto_decode_10>01011010 01101110 01100001 01110000 01110101 01110010 01100110 01100111 01110010 01100101 00101100 00100000 01100110 01100010 00100000 01111010 01101000 01110000 01110101 00100000 01100111 01100010 00100000 01101110 01100001 01100110 01101010 01110010 01100101 00100000 01110011 01100010 01100101<@/auto_decode_10>

Needless to say, if the automatic rotN cracking pwns any production code we will be greatly amused.

Decrypting XOR repeating key encryption

I was going to finish the blog post there but then James challenged me to decode repeating XOR encryption. Using the absolutely excellent cryptography site Practical cryptography I learned all about XOR and frequency analysis. The first step is to determine the key length. You can do this using frequency analysis for each key candidate, I used 30 as the maximum key length guesses. I stored each character in a frequency table and incremented them each time they occur in the ciphertext. When you have all the frequencies you can then you can then calculate the index of coincidence (or hamming distance) for each of the columns and frequencies. Once you have the index of coincidence for each key candidate I then got the top 7 and normalized the IC by dividing by the key length candidate then sorted the top 7 by the IC and returned the top one as the guessed key.

I spent a lot of time to try and improve the accuracy of the key guess and rewrote the code a lot of times. The trusted signal blog stated you can improve the accuracy of determining the key length by using the greatest common denominator between the top 5-6 candidates but in my tests I couldn't improve the accuracy. Anyway once you have the key length you simply loop through the ciphertext and each character and xor it and assign it a score based on the character result. I based most of the code on a cool python utility by Alexey Hellman.

Finally I reused my is_like_english function to determine the score of the text if the conversion has been successful or not. This was working for small pieces of text but failed with larger ones and this is because the more text you have the lower ngram score you get, so I changed the fixed value to a percentage of difference between the average and this works regardless of the ciphertext length. For very small pieces of ciphertext the XOR decryption will fail, I think this because there isn't enough ciphertext to perform frequency analysis to correctly determine the key length and score for each character decrypted. If you think of a way to improve this then please submit a pull request.

To demonstrate the auto decoding I've done an XOR with a key and then hex encoded it. When you enter the input into the input box watch as Hackvertor will auto decode the hex, guess the key length and then decrypt the XOR encryption automatically and even provide you with the correct tags to reproduce the encoding.

<@auto_decode_8>1C090C1E05041C101C523D296324212F000D020C04061D001C216F36383668231619064521010606376F3724732E080D0F561617171A003B3B3A6B3630110C18031717074F1037292C39366808174C0545061B00523E2E372E7D68231A4B03161B1A0852313A373F3A26064E0E120217541C1133212D223D2F41170E150D1C1B031D35366F6B2A27144308170B521D0B173C3B2A2D2A68150B0E5613170616523E2E372E203C41151E1A0B17060E103B232A3F3A2D124D4B391000541D17212A22393020041118560300111E07372137272A68140D08191317064F10202E2D2F732604144B00101E1A0A00332D2A273A3C1843081A0401070A01723B2B2A276823161906451B074F063A2A632D3A3A12174B020A52060A023D3D3765<@/auto_decode_8>

Repeated XOR is genuinely used from time to time, so hopefully this feature will help prevent some applications from getting away with looks-legit encryption.

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
