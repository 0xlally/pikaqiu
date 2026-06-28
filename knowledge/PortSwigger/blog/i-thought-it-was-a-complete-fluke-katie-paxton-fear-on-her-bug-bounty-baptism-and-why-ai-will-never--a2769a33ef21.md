# ‘I thought it was a complete fluke’ – Katie Paxton-Fear on her bug bounty baptism and why AI will never fully replace security researchers

Source: https://portswigger.net/blog/i-thought-it-was-a-complete-fluke-katie-paxton-fear-on-her-bug-bounty-baptism-and-why-ai-will-never-fully-replace-security-researchers
Fetched: 2026-06-28T09:15:17.569219+00:00

‘I thought it was a complete fluke’ – Katie Paxton-Fear on her bug bounty baptism and why AI will never fully replace security researchers

Adam Bannister |

Friday, 11 September 2020 at 14:02 UTC

The YouTube cybersecurity educator on her journey into bug hunting and the future of machine learning

When Katie Paxton-Fear discovered two vulnerabilites on the day she was introduced to bug bounty hunting, she assumed it was a fluke.

But the UK-based science graduate soon realized that her inquisitive nature and transferrable skills in data science and software engineering meant it wasn’t a one-off.

Now a part-time bug bounty hunter, Paxton-Fear (@InsiderPhD) is also working towards a PhD in defense and security, works as a university lecturer, and provides free education tools on her popular YouTube channel aimed at inexperienced bug bounty hunters.

Speaking to The Daily Swig, Paxton-Fear discusses machine learning, AI, and her vision for finessing traditional bug hunting techniques with data science.

When did you first become interested in cybersecurity?

I got into security almost by mistake. I always wanted to do a PhD and to be an academic. In my last year of university I could have chosen a security course, but I did something else because I thought it would be too hard.

I then worked for a company in Manchester doing data science, looking at sales figures. Then when I was applying for a PhD there were two options: data science plus security and data science plus music, and I thought security sounded more interesting.

And how did you get into bug hunting?

One of my friends just happened to be a bug hunter and they invited me to a mentoring thing run by HackerOne. [At first] I said I wasn’t interested, but peer pressure [eventually] worked.

I remember being on the train to London [en route to the event] and thinking: “I’m not going to find a bug, but I’ll have a good time and learn about a part of security that I’m not familiar with.” And of course, I found my first, then my second bug.

Read more of the latest bug bounty news

I was so shocked – my background was very much in data science and software engineering. I’d always been interested in computers and how they work, but never security.

I thought it was a complete fluke. Then I was invited to Vegas and found two more bugs, and I realized, hang on – I might actually be rather good at this.

Where do you think your talent for findings bugs comes from?

I think my experience in software engineering led to those first bugs being quite straightforward for me. I was thinking: “If I was a developer, how would I build this?” It gives me ‘x-ray vision’, which builds up that intuition that there might be a security vulnerability there.

It’s a problem-solving thing, like being Sherlock Holmes, and I’m naturally quite an inquisitive person. I like solving puzzles.

RELATED Mail.ru’s Vladimir Dubrovin: Why bug bounties should be ‘part and parcel’ of the security process

Are there certain types of bugs that you’re particularly interested in, good at discovering, or both?

Business logic errors are my favorite bugs. One bug I found allowed you to lengthen or shorten the length of an airplane runway. By making a runway a lot shorter, you could cause a lot of deaths because a Boeing 747 can’t slow down in time.

It was actually quite a simple bug technically, but when you add in the context and impact it’s really interesting.

What factors influence your choice of bug bounty programs?

I like to work with companies that are interested in what hackers are doing, who will answer your questions quickly, and if you don’t quite explain something, they won’t try and shut you down; they’ll [politely] ask for more information. I like having that back and forth relationship – sort of being part of that security team.

I also love API hacking. I think APIs are great places to find vulnerabilities.

Have you encountered any major problems when disclosing security vulnerabilities?

Every single company I’ve worked with has being super professional, at least from my experience with HackerOne. I’ve felt really supported, and of course you can speak to the triage [staff], especially at the HackerOne live events.

What inspired you to set up your YouTube channel, which is approaching 16k subscribers at the time of writing?

I went to a HackerOne live event in Vegas as a mentee and ended up showing other mentees how to use Burp [Suite]. I then realized there was a gap in bug hunting in that you have beginners [courses in] how to install Burp, and you have the advanced stuff – “here’s how I found an RCE and made $300,000 with Google, Amazon, or Tesla”.

But for the middle ground – people looking for their first bug – it didn’t feel like there were a lot of resources. I wanted to fill that gap. I [make videos about] what I’m interested in and the secrets that I think will really help people in the same position that I was [when I started out bug hunting] in 2019.

I’ve got followers who are way better bug hunters than me now, so I feel quite proud of the community I’ve built.

RECOMMENDED Bug bounty leader Clément Domingo on chaining vulnerabilities for maximum impact

You presented at #Levelup0x07 about the ramifications of using AI and machine learning in infosec. How do you see this technology supporting bug hunters as it evolves?

AI is basically a computer program that can think like a human, but sometimes humans don’t really think very deeply. If we’re hungry, it’s not a very complex decision. And likewise, some AI systems are very simple.

But we also have really complex thoughts and we can identify images, [which AI can replicate through] image recognition systems, and there’s a broad variety in between.

We won’t see AI replacing bug hunting because it requires a really large amount of data from bug hunters and no one’s going to give that data.

We are seeing a trend towards automation and people building up these automated pipelines, and that might be considered simple AI, but fundamentally, you can never replace that human creativity. You still need a human at the end of the pipeline [to decide whether something’s worth investigating or not].

And how do you see AI fitting into the never-ending battle between cybercriminals and security teams?

What we should be most concerned about is not whether bug hunters and malicious actors are using AI to find vulnerabilities, but the AI systems that have already been deployed and not been tested on platforms like HackerOne.

I think we’ll see more attackers trying to target those systems. As a community I think we need to start encouraging data scientists, AI engineers, and machine learning engineers to become hackers themselves and start hacking these AI systems.

What’s your career plan over the next few years?

I have a job as a lecturer, and in the UK that means doing research as well as teaching. So I now have the ability to study whichever field of security research I want. It felt really exciting and terrifying to be told “just go wild”.

I really want to make some strong contributions to security research, especially in using existing data collected by bug hunters and augmenting [research] approaches with more data science. It’s getting those visualizations and understanding what those next steps might be – cleaning up data, labeling it… A lot of stages have to happen before we have fully automated bug hunting machines.

And I’ll always be hacking, finding bugs, and making YouTube videos that offer free technical knowledge because a lot of people can’t afford or get access to university-level courses.

READ MORE Meet the bug bounty platform putting community into crowdsourced security

Adam Bannister

@Ad_Nauseum74

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
