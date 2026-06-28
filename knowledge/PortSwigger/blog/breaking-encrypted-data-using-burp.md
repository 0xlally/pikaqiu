# Breaking encrypted data using Burp

Source: https://portswigger.net/blog/breaking-encrypted-data-using-burp
Fetched: 2026-06-28T09:15:07.970992+00:00

Breaking encrypted data using Burp

Dafydd Stuttard |

Wednesday, 12 October 2011 at 11:05 UTC

Encryption

session tokens

burp intruder

A while ago, Burp Intruder added a bit flipping payload type, suitable for automatic testing for vulnerable CBC-encrypted session tokens and other data. If you aren't familiar with this vulnerability, take a look at The Web App Hacker's Handbook, 2nd Edition, pages 227-233, and also check out this exercise (login required) in the MDSec online training labs.

Burp Intruder now has a further payload type, suitable for automatic testing for vulnerable ECB-encrypted data. The theory behind these vulnerabilities is described on pages 224-226 of WAHH2e. Here, I'll briefly describe an example of the vulnerability, and show how it can be exploited using Burp.

ECB ciphers divide plaintext into equal-sized blocks, and encrypt each block separately using a secret key. As a result, identical blocks of plaintext always encrypt into identical blocks of ciphertext, regardless of their position within the structure. This means that it is possible to meaningfully modify the plaintext in a structure by duplicating and shuffling the blocks of ciphertext. Depending on the contents of the structure, and the application's handling of the modified data, it may be possible to interfere with application logic - for example, switching the user ID field in a structured session token, changing an encrypted price, etc.

Let's look at an example from the MDSec online training labs. Here, the application uses session tokens containing several meaningful components, including a numeric user identifier:

rnd=2458992;app=iTradeEUR_1;uid=218;username=dafydd;time=634430423694715000;

When encrypted, using an ECB cipher, the token becomes:

68BAC980742B9EF80A27CBBBC0618E3876FF3D6C6E6A7B9CB8FCA486F9E11922776F0307329140AA

BD223F003A8309DDB6B970C47BA2E249A0670592D74BCD07D51A3E150EFC2E69885A5C8131E4210F

The individual blocks of plaintext correspond to blocks of ciphertext as follows:

rnd=2458 68BAC980742B9EF8

992;app= 0A27CBBBC0618E38

iTradeEU 76FF3D6C6E6A7B9C

R_1;uid= B8FCA486F9E11922

218;user 776F0307329140AA

name=daf BD223F003A8309DD

ydd;time B6B970C47BA2E249

=6344304 A0670592D74BCD07

23694715 D51A3E150EFC2E69

000;     885A5C8131E4210F

Now, because each block of ciphertext will always decrypt into the same block of plaintext, it is possible to manipulate the sequence of ciphertext blocks, and meaningfully modify the corresponding plaintext. Depending on how the application handles the modified data, this may allow you to switch to a different user or escalate privileges.

For example, if the second block is copied following the fourth block, the resulting sequence of blocks will be:

rnd=2458 68BAC980742B9EF8

992;app= 0A27CBBBC0618E38

iTradeEU 76FF3D6C6E6A7B9C

R_1;uid= B8FCA486F9E11922

992;app= 0A27CBBBC0618E38

218;user 776F0307329140AA

name=daf BD223F003A8309DD

ydd;time B6B970C47BA2E249

=6344304 A0670592D74BCD07

23694715 D51A3E150EFC2E69

000;     885A5C8131E4210F

The decrypted token now contains a modified "uid" value, and also a duplicated "app" value. What happens will depend on how the application processes the decrypted token. If you are lucky, the application will retrieve the "uid" value, ignore the duplicated "app" value, and not check the overall integrity of the whole structure. If the application behaves like this, then it will process the request in the context of user 992, rather than user 218.

Now, it is possible to perform this attack manually, but this involves a lot of effort if you are working blind, without knowledge of the actual contents of the plaintext blocks. The new Burp Intruder payload type helps you to automate the process of finding and exploiting these vulnerabilities, in a much more effective way.

The configuration for the new payload type looks like this:

In the present case, we're going to tell Burp that the token contains 8-byte blocks and is encoded as ASCII hex. If you didn't know or couldn't guess this information, you could try different configurations, as this attack is normally fairly fast to run.

When the attack runs, Burp will split the base value into blocks, and will systematically duplicate and shuffle them, inserting a copy of each block at each block boundary. In some situations, this method alone will be sufficient to find a vulnerability. However, to make your attack more effective, you should also if possible use the further configuration "obtain additional blocks from these encrypted strings", as described below.

There is often a large element of luck involved when blindly shuffling blocks in ECB-encrypted data structures, and success often depends upon happening to find a block of ciphertext whose decrypted plaintext contains the right meaningful data when inserted into the structure (such as a number that could be a valid user ID within a session token). You can dramatically increase the likelihood of success by providing Burp with a large sample of other data that is encrypted using the same cipher and key. In the present example, you can harvest a large number of valid tokens using Burp Intruder or Sequencer, and configure the ECB block shuffler payload to use these tokens to derive additional blocks. Burp will then take all of the unique ciphertext blocks that you have provided, and use these when inserting blocks into the original data. In practice, if you can find suitable additional encrypted data, this method proves highly effective when targeting vulnerable applications.

Having used Burp Sequencer to obtain a large sample of tokens via the main application login, our configuration of the ECB block shuffler now looks like this:

To deliver the attack, we're going to target the user's account page within the application, which displays information about the logged in user (based, of course, on the supplied session token):

In order to identify the user context associated with each attack request, we're going to use the Extract Grep feature to highlight the name of the current user within the account page response:

We then start the attack and review the results. Unsurprisingly, a lot of the requests cause a redirection back to the login, because we have corrupted the format of the token. Many of the requests result in an apparently valid session, but showing "unknown user" - here, we have modified the UID to a value that does not correspond to any actually registered user. But in other requests, we are apparently logged in as a different user, including, as luck would have it, an application administrator:

A successful attack like this still requires a lot of luck, including whether and how the application tolerates modifications to the modified data, the positioning of block boundaries in relation to interesting data, and the ability to find a block containing suitable data for substitution. But the new Intruder payload type takes a lot of the pain out of testing blind for this vulnerability.

Have fun!

Encryption

session tokens

burp intruder

Dafydd Stuttard

@DafyddStuttard

Latest Posts

Burp Extensibility 2026: Awards, Talks, and Highlights

19 June 2026

Burp Extensibility 2026: Awards, Talks, and Highlights

The beast needs a cage: What's next for AppSec post-Mythos

12 May 2026

The beast needs a cage: What's next for AppSec post-Mythos

3 ways custom scan checks turn practitioner knowledge into scalable automation

01 May 2026

3 ways custom scan checks turn practitioner knowledge into scalable automation

Senior pentesters have a deeply refined intuition about what is vulnerable in an environment. The problem? That expertise is often siloed with an individual and trapped in their notes or Python scripts.
