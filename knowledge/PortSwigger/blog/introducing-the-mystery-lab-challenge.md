# Introducing the mystery lab challenge

Source: https://portswigger.net/blog/introducing-the-mystery-lab-challenge
Fetched: 2026-06-28T09:15:18.442412+00:00

Introducing the mystery lab challenge

Emma Stocks |

Friday, 11 March 2022 at 14:30 UTC

For anyone who's used the Web Security Academy before, you'll be pretty familiar with the format. For those of you who haven't had the pleasure, the process goes a little bit like this:

Select a set of learning materials based on a topic - for example, SSRF.

Read through the learning materials, and build up your knowledge of the vulnerability

At various stages throughout the learning materials, you'll encounter a lab (a deliberately vulnerable website). The lab, provided with a clear objective, enables you to test the skills you've just learned.

If your desired outcome is purely about building up your knowledge of a specific vulnerability, and how to find and exploit it, then the labs within learning materials are exactly what you need. However, as we all know, this isn't exactly how things play out in the wild.

With that in mind, we decided it was time to add an element of recon to the academy. In the real world, the term recon often refers to finding target websites in the first place. However, as that particular piece of the puzzle is provided for you, the mystery lab challenge is more about attempting "in-application" recon.

This new feature gives academy users the chance to find and exploit vulnerabilities by generating a random lab to test their skills - have a go at the mystery lab challenge now...

Understanding the objective

In both the Web Security Academy, and out in the wild, the objective can often look like this: hunt down and exploit any and all vulnerabilities present. In the Web Security Academy, you already know what you're looking for and are often given multiple clues as to the steps you'll need to take to uncover and exploit the vulnerability.

For anyone already bug bounty hunting or pentesting in the real world, you'll be well versed on the requirements for recon. If you've only practiced these skills in a secure environment, like the Web Security Academy, you may have less experience with this crucial skill.

Looking at an academy lab on SSRF - for example, "SSRF with filter bypass via open redirection vulnerability" - you can see that the name of the lab has already told us what the vulnerability class is, and how to overcome any obstacles to exploitation you encounter.

By comparison, a pentester may be given a job whereby they're tasked with uncovering all vulnerabilities - or uncovering only high-impact, unauthenticated issues. Other than knowing the impact, they're given no additional information - they need to rely on their own knowledge, and apply the correct frameworks, in order to solve the objective.

Therefore, to enable the Web Security Academy to better prepare its users for hunting and testing in the wild, we decided we needed to take the challenge one step further. In order to more closely imitate a real-world situation, we've launched a brand new feature on the Web Security Academy: the mystery lab challenge.

What's the mystery lab challenge?

As the name probably suggests, this new feature gives academy users the chance to find and exploit vulnerabilities by generating a random lab to test their skills. The mystery lab challenge has three basic settings, which are as follows:

Select the level of lab you want to try and solve, but leave the topic random.

Select both the level of the lab and the topic you want, then randomly generate one of the labs within that topic.

Leave both the lab level and the topic unspecified, and spin-up a completely random lab from anywhere within the academy.

When your mystery lab first appears, the objective will be completely hidden - naturally this presents the most difficult version of the challenge. You can choose to display the objective if you need a bit of direction, and if you're really struggling then you can also fully de-anonymize the lab too.

The idea behind this new feature is that by taking away some of the context that the labs provide you with, we're able to introduce an element of recon to your academy experience. Why not take it for a spin, and try your hand at the mystery lab challenge?

Emma Stocks

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
