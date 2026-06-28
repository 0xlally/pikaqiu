# Introducing Burp Sequencer

Source: https://portswigger.net/blog/introducing-burp-sequencer
Fetched: 2026-06-28T09:15:17.768459+00:00

Introducing Burp Sequencer

Dafydd Stuttard |

Sunday, 21 October 2007 at 14:30 UTC

session tokens

burp

This is a preview of a new addition to the Burp family of tools, which will be included in the next release of Burp Suite arriving later this year.

Burp Sequencer is a tool for evaluating the randomness of session tokens or other data. Think Stompy on steroids, with more tests, quantitative results, graphical reporting, and arbitrary sample sizes.

Burp Sequencer is easy to use. The first step is usually to locate a request within the target application which returns a session token somewhere in the response. You can do this using the "send to sequencer" option within any of the other Burp tools:

[click on any image to enlarge]

The request and response are displayed within Sequencer, allowing you to identify the location of the token you are interested in. Any cookies or form fields within the response are automatically parsed out for you to choose; alternatively, you can select an arbitrary position within the response where the token appears:

Once configured, Burp Sequencer begins acquiring tokens from the application by repeatedly issuing your request and extracting the relevant token from the application's responses:

As soon as 100 tokens have been captured, you can perform an analysis of the tokens, to get an initial rough indication of the quality of their randomness. Obviously, a larger sample size enables a more reliable analysis. The live capture continues until 20,000 tokens have been captured, which is sufficient to perform FIPS-compliant statistical tests.

If you have previously obtained a sample of tokens from the application (or from any other source) you can also load these manually into Burp Sequencer, to perform the same analysis on them:

Burp Sequencer can operate on any sample size between 100 and 20,000. The analysis mainly uses significance-based statistical tests in which the assumption that the tokens are random is tested by computing the probability of the observed results arising if this assumption is true. If the probability falls below a particular level (the "significance level") then the assumption is rejected and the anomalous data is judged to be non-random.

This approach allows Burp Sequencer to give an intuitive overall verdict regarding the quality of randomness of the sample. This summary shows the number of bits of effective entropy within the token for each level of significance:

To gain a deeper understanding of the properties of the sample, to identify the causes of any anomalies, and to assess the possibilities for token prediction, Burp Sequencer lets you drill down into the detail of each character- and bit-level test performed. The following screenshot shows the analysis of character distribution at each position within the token:

The following screenshot shows the results of the FIPS monobit test at each bit position within the token:

There are several other useful functions and configuration options affecting how tokens are captured and processed. Hopefully, Burp Sequencer will prove to be a valuable weapon in the web application hacker's arsenal, and will enable more effective and easier assessment of session token randomness than is possible with other current tools.

session tokens

burp

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
