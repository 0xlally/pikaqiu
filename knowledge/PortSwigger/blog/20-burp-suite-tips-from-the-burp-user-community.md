# 20 Burp Suite tips from the Burp user community

Source: https://portswigger.net/blog/20-burp-suite-tips-from-the-burp-user-community
Fetched: 2026-06-28T09:15:05.900717+00:00

20 Burp Suite tips from the Burp user community

Emma Stocks |

Wednesday, 2 June 2021 at 11:23 UTC

The Burp Suite user community can easily be described as passionate, dedicated, and highly invested in the development of our product. That's why we love it when our users take it upon themselves to question each other, and discover new and exciting ways to make Burp Suite work for them.

Long-time Burp Suite Professional user Michael Skelton, better known as @codingo_, ran a fantastically informative Tweet thread asking users for their best tips and tricks. We trawled the results, and wanted to share our favorites with you all.

Time saving tips

One of the greatest superpowers that a pentester, or any kind of infosec professional for that matter, can wield, is the ability to save time. Automating manual processes, creating command repeats, or even just generating default project options - anything that frees up your time to deep-dive the juicy stuff counts as a win in our book.

1. "When you are playing with a parameter in the repeater tab and its value gets reflected in the response, you can enable this toggle when you have to scroll to see what has changed...a true time saver! @sw33tLie

2. "Build a default_project_options.json to avoid repeat the same config over and over. Like the regex on advance scope definition, timeouts, proxy or intercept config, match and replace, history filter or ssl_pass_through. Just set a target and start hunting immediately!" @Six2dez1

3. "From Proxy > HTTP HistoryCtrl + R (Send the request to Repeater)Ctrl + Shift + R (Jump to Repeater)Ctrl + Space (Send the request from Repeater)It saves my mouse time :)Learnt by navigating "User options > Misc > Hotkeys" @rashedul_css

4. "You can change default intruder Payload list. Set your custom one and it will be a time saver." @fuxksniper

5. "In search, tick "negative" matches to filter out all responses/requests that contain strings that you do not want to see - example, "incap_sess". This is a quick way other than using other method." @yappare

Discovery techniques

Naturally, you'll have taken all of the time-saving suggestions above on board, so you'll be needing something to fill up all of that free time - right? Lucky for you, the Burp Suite community is all hands on deck when it comes to discovery. Advice on traffic filtering, post listening, server abnormalities, script creation, collaborator polling, and much much more ...

6. "shout out to @LaNMaSteR53 for showing us this during his training tools/target/site-map/comparing @pirateducky

7. "When using extensions is too much, using the old compare sitemap to test for access control issues && excluding logout/login/delete etc from scope && (cookie jar when it only use cookies || another chained burp to replace required tokens/csrf/header with another user's)." @irsdl

8. "Use Advance scope option to just use the name of the site/company. that way I can filter our traffic + this also helps to see incase there's S3 bucket or any other cloud storage being used under company/domain's name!" @imhaxormad

9. "Starting multiple local proxy listeners on separate ports for various tools. That way you can filter your views by port and see exactly how the tools act and what (undiscovered) abnormalities they might trigger on the server." @rauschecker

10. "Match & replace FALSE2TRUE, most of the times it gives some interesting behaviours :)" @sudhanshur705

11. "Save burp project to file and use gf patterns against it for searching sensitive stuff like keys,tokens,etc. Kind of passive technique for Searching is js files for secrets." @admiralgaust

12. "persistent access to collaborator sessions: https://onsecurity.io/blog/persistent-access-to-burp-suite-sessions-step-by-step-guide/With the "SECRET_KEY", you can create scripts and poll the collaborator and do whatever you want with the results.E.g1.malware->base64(whoami).burpcollaborator.com2.Poll->get the requested subdomain->B64decode"@gweeperx

13. "I admit I use 'copy as curl' for non-pentesting purposes … It’s super helpful to add as a POC for engineers to fix a bug when they don’t have burp." @Blue_CanaryBE

14. "For me Match and Replace function was a gem. I use it for many functionalities ex: Adding Cache poisoning related headers like X-Forwarded-Host: unique_stringAfter that i will look for the unique_string in Logger+ Responses if it is reflecting anywhere" @0xlrfan

15. "add irrelevant-noisy hosts to ssl-passthrough list so the state will be smaller and you don't get distract when looking to the history tab Also you dont have to forward irrelevant requests/responses while intercepting. Especially in mobile app testing" @Mustafaran

Productivity and workflow tips

Being familiar with Burp Suite is one thing, but knowing lightning-fast shortcuts and rapid-fire ways to access the information you need more quickly? That's something we'll never tire of learning about. Our users have covered everything from keyboard shortcuts to naming conventions here, and it's all going to contribute to improving your workflows and getting results faster.

16. "This probably may not be a tip or a trick but I think I learnt this from @InsiderPhD if I'm not wrong. It's basically renaming the repeater tabs in repeater. I do this for each important endpoint I visit and this works wonders when you have so many tabs open." @thebinarybot

17. "There are two previous (<) & next (>) tabs on top of repeater I didn't know that I learned from stok's interview with nahamsec I guess .... :)" @sidparmarr

18. "Always save a copy of the project file in the end with the items in the scope only to reduce the project file size - then 7zip is the best format to compress it heavily." @irsdl

19. "Match and replace with XSS polyglots...add XSS1="'--></style></script><svg oNload=alert()> And everytime that you write XSS1 while browsing it will be replaced. Thanks to @SamuelAnttila!!" @bb0011cc

20. "Sending requests to Burp on my local machine from my VPS via various tools (that have a proxy option) using the "ssh -R 18081:localhost:8081" when logging on.I add a proxy listener for 127.0.0.1:8081 to Burp for this so I can easily filter between local machine and VPS traffic." @xnl_h4ck3r

Anything we've missed?

Huge thanks go out to Michael Skelton for starting this thread off, and of course to all of the incredible members of the Burp Suite community for sharing their tips and tricks. If you have any other advice to share, or any questions you want answered, make sure to post them to our Twitter account using the hashtag BurpSuiteTips. Happy Burping one and all!

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
