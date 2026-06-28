# From curiosity to critical impact: A pentester's perspective on Burp AI

Source: https://portswigger.net/customer-stories/cristi-vlad-burp-ai
Fetched: 2026-06-28T09:17:02.407284+00:00

From curiosity to critical impact: A pentester's perspective on Burp AI

We caught up with Cristi Vlad to discuss his early

experiences with Burp AI and get his take on how AI

could be transformative for penetration testing in years

to come.

In this story

IntroductionHands-on at heartDiscovering Burp AICollaboration, not automationMore bandwidth, better focus, bigger winsAddressing the skepticsNo more near missesBurp AI's unique advantagesPrivacy and trustExperience Burp AI for yourself

No other tool is capable of providing this

sort of granular, organized context to the

AI.

Cristi Vlad, Pentester and bug bounty

hunter

Modern web apps are sprawling and

increasingly complex, comprising numerous

different technologies, frameworks, and

microservices. Even for the most seasoned

pentesters, it's a constant balancing act

between digging deeper and ensuring you've

covered the full scope.

Cristi Vlad, a penetration tester and bug

bounty hunter based in Romania, has spent

the last seven years honing his craft.

Originally trained as a civil engineer, he

made a career pivot after discovering the

thrill of hacking through platforms like

VulnHub, HackTheBox, and of course, the Web Security Academy. Today, he runs his own consultancy,

delivering high-impact pentests for clients

around the globe.

Like any experienced pentester, Cristi has

long relied on Burp Suite Professional as his go-to tool for web app and API

security testing. Recently, he started using

Burp AI to enhance his workflow, and the

results have been transformative. Rather

than automating his work or replacing his

expertise, Burp AI

has become a true collaborative assistant,

helping Cristi think more broadly, work more

efficiently, and even helping him discover

critical security vulnerabilities.

Hands-on at heart

Cristi often tackles short, high-intensity

pentests. In his typical workflow, he relies

heavily on his hard-earned skills and a

level of intuition that only comes from

experience.

"I obviously conduct my pentests according

to the OWASP framework or whatever my

client's requirements are," he explains,

"I'm at the point now where I have an

intuitive feeling about where I need to

focus my time. That only comes from 'doing

reps', so to speak."

I have an intuitive feeling about where I

need to focus my time. That only comes from

'doing reps'.

"I usually start out trying to get a feel

for the app while proxying everything

through Burp. At the same time, I'm trying

to think of any unintended uses for the

functionality I discover, or how I might

make the app behave in unintended ways. I

suppose that's fundamentally what pentesting

is about."

"In Burp itself, I spend most of my time

between the Proxy history and Repeater,

tampering with different inputs to see how

the app responds. If I see something and

think it might be exploitable, I like to

just test it out on the spot."

But this presents a familiar challenge.

With so many potential leads to follow in a

narrow time frame, comprehensively testing

complex modern apps is increasingly

unfeasible through manual methods

alone.

Pentesting can be a bit of a mess at times,

and I often end up exploring multiple leads at

once.

"Pentesting can be a bit of a mess at times,"

he admits, "I often end up exploring multiple

leads at once."

Discovering Burp AI

Cristi first heard about Burp AI after

seeing a post by PortSwigger researcher, James Kettle. His interest was piqued, but like many in

the field, he's wary of gimmicky AI features

offering hollow promises that they can

automate what he enjoys doing.

I don't like the idea of something that tries

to magically do everything for me. I think a

lot of pentesters feel the same.

"I don't like the idea of something that

tries to magically do everything for me, and

I think a lot of pentesters and security

researchers feel the same," he explains, "I

get a lot of satisfaction from applying my

skills creatively and coming up with

something interesting. There's a fine line

between collaborating with AI and it just

serving you everything on a silver platter.

It's a kind of philosophical question

really."

Skeptical but curious, he decided to trial

the Explore issue

feature on a real engagement. It wasn’t long

before it paid off.

During a routine scan, Burp flagged a

potential Host-header injection

vulnerability, so Cristi let Burp AI explore

the issue further. While the AI was running

its analysis, he manually sent the request

to Repeater and began his own investigation,

modifying headers and observing

responses.

At the same time, his scan identified a

potential username enumeration

issue in a password reset flow. Cristi's

experience and intuition allowed him to

quickly connect the dots: he combined

insights from the AI investigation with his

manual findings.

AI helped me think outside my normal

methodology [...] It brought things to my

attention I might have missed.

"I thought I'd try and combine the two

bugs,"

he explains. When he tried the Host-header

injection with the password reset

functionality, the result was a critical

account takeover via password reset poisoning. "When I saw the password reset link

pointing at my Burp Collaborator

URL, I knew it was a done deal."​

This wasn’t just a minor bug. It was a

vulnerability that, in a bug bounty program,

could have earned Cristi a substantial

payout. While he's quick to note that AI

didn’t find the issue on its own, he credits

it with helping him reach the conclusion

faster and more confidently.

"AI helped me think outside my normal

methodology," he says, "It brought things to

my attention I might have missed."

Collaboration, not automation

Cristi doesn’t see Burp AI as a tool that

takes over his work. Instead, he sees it as a

collaboration tool that creates mental space

for creative problem-solving.

It actually feels like a collaboration [...]

It gave me the headspace to think

laterally.

“It actually feels like a collaboration

with the AI,” he says, “I can be in Repeater testing all sorts of

things, while Burp AI is following up on

other leads in the background. It gave me

the headspace to think laterally and connect

the dots between two separate issues. That's

exactly how I want it."

This philosophy aligns perfectly with PortSwigger’s vision for AI. As Dafydd Stuttard, Burp Suite’s creator,

puts it: "This isn’t a revolution that eliminates

pentesters; it’s an evolution that empowers

them."

Burp AI doesn’t automate you out of the

loop; it gives you more bandwidth to do what

you’re best at.

More bandwidth, better focus

Thanks to Burp AI, Cristi could:

Maintain full control

over his pentest, while offloading

background tasks to AI.

Stay focused

on the highest-value activities that

required his human expertise, letting Burp

AI pick up the slack and follow other leads

on his behalf.

Expand his situational awareness, leading to a critical vulnerability that

might otherwise have been missed.

The collaborative approach also reinforced

Cristi's enjoyment of testing. "I like that these are AI enhancements to

support my workflow, not automate it

away," he noted.

I like that these are AI enhancements to

support my workflow, not automate it

away.

He emphasized that the careful design of

Burp AI, respecting user control, privacy,

and supplementing, rather than disrupting,

his manual workflow, was crucial to earning

his trust.

Cristi's experience highlights

PortSwigger's vision for Burp AI: augmenting

professional testers, not replacing them.

Like power tools for carpenters, Burp AI is

designed to let skilled security researchers

do more, think faster, and achieve greater

results, while keeping the human expert

firmly in the driver's seat.

Addressing the skeptics

Cristi is candid about the skepticism he

sees in the industry. Some pentesters worry

about AI replacing them, or at least

diluting their value. But he doesn't see

this as a real concern.

"I don't think the technology is capable of

fully automating pentesting yet, but it has

huge potential."

I'm really pleased that you're implementing

Burp AI as a helpful assistant designed to

support me with the things I'm already

doing.

"I'm really pleased with how you're

approaching it in Burp Suite, by

implementing Burp AI as a helpful assistant

designed to support me with the things I'm

already doing."

Some simply dismiss AI features as gimmicks

outright, insisting their own knowledge and

experience are already vastly superior to

anything AI is capable of. But Cristi

encourages them to try Burp AI with an open

mind.

"When you have a fixed methodology or a

workflow, the human tendency is to stick to

it because it's comfortable. But I think

that's to your own detriment," he explains,

"I think as these features mature, they'll

help people break that cycle and think a bit

more outside of their comfort zone."

No more near misses

Cristi describes how, like many pentesters,

he often wonders about vulnerabilities he may

have missed out on or overlooked in the past.

He's excited to see how Burp AI can help him

avoid these cases going forward.

It's invaluable because nobody knows

everything. It's delusional to think you do,

no matter how much experience you have.

"I like the fact that AI could bring to my

attention additional attack vectors or issues

that I might've missed otherwise due to not

being as familiar with that particular

vulnerability class or technology. That's

invaluable because nobody knows everything.

It's delusional to think you do, no matter how

much experience you have."

Burp AI's unique advantages

He also points out that integrating AI

directly into Burp Suite has some unique

advantages."Even if you have an advanced model, you

also need to provide it with the relevant

context."

No other tool is capable of providing this

sort of granular, organized context to the

AI.

"Given that Burp Suite is a sort of 'X-ray'

for studying an application, no other tool is

capable of providing this sort of granular,

organized context to the AI."

Privacy and trust

While naturally careful with his clients'

sensitive data, he doesn't have an issue

with Burp AI relying on third-party

models.

"PortSwigger has zero-retention agreements

with all of the model providers, so I'm not

concerned about that side of things. And

besides, you're constantly interacting with

sensitive data and functionality during a

pentest, regardless of whether you're using

AI features or not. Being mindful about what

you're doing and what the implications might

be is just part of being a pentester; it's

not a new issue that's been introduced by AI

specifically."

Experience Burp AI for yourself

Cristi’s story isn’t unique. It’s just the

beginning of what’s possible when AI and

human expertise work together. If you’re

ready to spend less time on tedious

validation and more time on creative

hacking, give Burp AI a try.

Every Burp Suite Professional user gets

10,000 free AI credits to experiment with.

No gimmicks. No nonsense. Just practical,

privacy-respecting assistance that fits

seamlessly into your existing

workflow.

Upgrade to the latest version of Burp Suite

Professional and start exploring with Burp

AI today.

UPDATE NOW
