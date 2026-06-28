# Can you hit a moving target?

Source: https://portswigger.net/blog/can-you-hit-a-moving-target
Fetched: 2026-06-28T09:15:12.121952+00:00

Can you hit a moving target?

Dafydd Stuttard |

Wednesday, 30 April 2008 at 21:45 UTC

Authentication

snake oil

Despite slanderous reports to the contrary, I remained sober at Infosec last week long enough to hear a number of skilled sales professionals peddling their wares. In amongst the vulnerability scanners that can find all known and unknown bugs, and the identity management solutions that will put hackers out of business, was an unbreakable authentication mechanism - "unbreakable" because it employs a device that changes the user's password every 60 seconds.

Can you guess a password that changes every 60 seconds?

Some would suppose that you cannot, or at least that you would be highly unlikely to do so. The intuition here is that each time a password is generated, you will only have a few chances to guess it before it changes. If you don't guess it in that time (which is very unlikely), you are back to square one. The situation, it seems, stands in stark contrast to that of a static password, where you can continue guessing indefinitely until you are successful.

This intuition, however, is mistaken, and employing a rapidly changing password in itself does not add much to the security of an authentication mechanism. To see why, let's compare two mechanisms that are equivalent in all other respects.

Suppose that a "changing password" mechanism employs a device that generates six-digit decimal numbers for passwords, which is fairly typical. To keep things simple, let's also suppose that an attacker only has time to make a single guess at each password before it changes.

In the equivalent "static password" mechanism, let's suppose that each user has a six-digit decimal number as a password, and that this never changes.

First, our attacker targets the static password mechanism. There are 1,000,000 possible passwords, so his first guess has a one in 1,000,000 chance of success - very unlikely. Assuming this guess is wrong, he has eliminated one possible password, so his next guess has a one in 999,999 chance of success. And so on. After 500,000 unsuccessful guesses, the attacker has eliminated half of the possible passwords, and so his next guess has a one in 500,000 chance of success - still very unlikely. But, significantly, at the outset of the exercise, the attacker may expect that, on average, he will have guessed the correct password by this point. If there are 1,000,000 possible passwords, and you try half of them, you have a 50% chance of success. Half the time, you will have guessed the password by this point - the other half, you will need to continue guessing.

Next, our attacker targets the changing password mechanism. Again, there are 1,000,000 possible passwords, so his first guess has a one in 1,000,000 chance of success. Assuming this guess is wrong, he tries again. But because the password is regenerated, he has not eliminated any outcomes for the second guess, so his next guess still has a one in 1,000,000 chance of success, and this remains the same no matter how many unsuccessful guesses he makes. He appears to have very little chance of guessing the password - hence the intuition.

However, as we saw in the case of the static password, after 500,000 unsuccessful guesses the attacker still has only a one in 500,000 chance of success in his next guess; nevertheless, at the outset of the exercise he may expect to have guessed the correct password by this point. So we may ask: what is the corresponding point at which the attacker targeting the changing password mechanism may expect to succeed?

Each time the attacker tries to guess a changing password, he has a 999,999 out of 1,000,000 chance of guessing incorrectly. So, the probability that he will fail to have guessed the password after one attempt is 0.999999. The probability that he will have failed after two attempts is 0.999999 * 0.999999. And so on. At the outset of the exercise, the probability that the attacker will have failed after N attempts is 0.999999 ^ N (where ^ means "to the power of").

So in a head-to-head challenge, what is the probability that the attacker targeting the changing password mechanism will have failed after 500,000 attempts? It is 0.999999 ^ 500,000, which is 0.606. That's right, there is nearly a 40% chance that the password will have been guessed by this point. With a bit of maths, we can work out that at the outset the attacker may expect that, on average, he will have guessed the correct password after 693,147 guesses - this is the point at which 0.999999 ^ N falls below 0.5.

Clearly, the changing password mechanism fared better, on average, than the static password mechanism - but by how much? In our scenario, the dynamic password takes on average 39% more attempts to guess than the static password - a relatively modest difference, of the same order of magnitude, and nothing like enough to justify the "unbreakable" intuition, or the likely expense of the password-generating device.

Now, in the real world there would of course be more factors in play than in my simplified scenario. Users may choose alphanumeric passwords with a larger range of possible values; but they may choose them non-randomly. They may write down their passwords; equally, they may leave their device lying around. Either mechanism may implement defences to frustrate brute force attacks. I don't want to suggest that password-generating devices are pointless - in many situations they can play a beneficial role in conjunction with other controls like conventional passwords, biometrics and account lockout. But if you hear the claim "It changes so it can't be broken", think "snake oil" and head for the bar.

Authentication

snake oil

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
