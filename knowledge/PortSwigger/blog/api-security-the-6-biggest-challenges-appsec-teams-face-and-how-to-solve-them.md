# API Security: The 6 biggest challenges AppSec teams face, and how to solve them.

Source: https://portswigger.net/blog/api-security-the-6-biggest-challenges-appsec-teams-face-and-how-to-solve-them
Fetched: 2026-06-28T09:15:06.886655+00:00

API Security: The 6 biggest challenges AppSec teams face, and how to solve them.

Rob Samuels |

Tuesday, 24 September 2024 at 10:01 UTC

AppSec teams face a wide range of challenges when securing their API estate against attack threats. In our recent webinar, which demonstrated the enhanced API scanning features in Burp Suite Enterprise Edition, we asked our attendees to describe their biggest API security pain points.

These pain points come from AppSec and penetration testing professionals across a range of sectors and roles. In this blog, we’ll share these challenges - and what you can do to solve them.

What are the biggest API security challenges faced by AppSec teams?

We’ve categorised the challenges into six key themes:

Lack of visibility over API attack surface.

Automation and scaling of API testing.

Consistent process and compliance.

Knowledge and skills gaps.

Limitations of current testing and tools.

Resource and time to perform tests.

Let’s go through each theme, and explore some of the specific issues raised.

Lack of visibility over API attack surface

AppSec professionals face numerous pains around a lack of API visibility - with a common challenge being the discoverability of API endpoints.

Others mentioned lacking a comprehensive view of what APIs they have (and therefore need to test) - a real concern when trying to secure APIs from a wide range of changing threats.

How can you solve these challenges?

For teams lacking visibility of their API estate, Burp Suite Enterprise Edition can detect API traffic and audit it automatically as part of a standard scan.

Burp Suite Enterprise Edition is also able to identify any APIs you may be hosting that are left accessible to attackers.

These features should help reduce concerns around a lack of visibility of your API attack surface.

Automation and scaling of API testing

Another major challenge is the ability to automate testing, with many organisations remaining dependent on manual testing. This led to concerns about scalability - with 19.5% of the AppSec professionals we spoke to already managing an estate of more than 500 APIs.

As this number continues to grow, automation becomes increasingly vital in API security.

How can you solve these challenges?

Burp Suite Enterprise Edition is designed to automate your scanning, allowing you to check the results at your convenience.

You can choose API-specific scans to scan your APIs on their own, or scan them as part of your regular scans.

This is done by providing an existing URL, or uploading an OpenAPI (OAS) definition file directly into Burp Suite Enterprise Edition.

These API-only scans can be automated, enabling faster, scalable scanning of APIs.

See how Burp Suite Enterprise Edition can help you scale your API testing. Click here to request a free, fully-featured trial.

Consistent process and compliance

As well as technical challenges around API security, maintaining efficient processes - and the consistent documentation of changes being made - also emerged as a major challenge.

A number of AppSec managers noted a lack of maturity in their DevSecOps, leading to inefficiencies in their work. There were also challenges noted around the collaboration between Security and Development teams, and the impact this has on maintaining APIs.

How can you solve these challenges?

CI-driven scanning enables standardised procedures to be created for your SDLC, enabling consistency in API development and management.

Burp Suite Enterprise Edition also enhances collaboration between developers and AppSec teams, by streaming results from the development pipeline into the tool.

Finally, using a DAST scanner like Burp Suite Enterprise Edition helps ensure compliance with a number of relevant regulations, such as FedRAMP.

Knowledge and skills gaps

One of the biggest themes was concern around skills and knowledge gaps within the organisation. Many noted they faced challenges with understanding how to configure endpoints, and sharing knowledge with new employees and across project teams.

There was also concern about having the right skill sets within their teams, and keeping up with the frequency of changes within API security.

How can you solve these challenges?

While software can’t fill knowledge gaps, Burp Suite Enterprise Edition provides remediation advice for the API vulnerabilities it finds.

The platform also links to learning materials and additional resources, helping your team to learn how to fix & also manually detect these vulnerabilities.

Utilising automated scans may also help save time for your team that can be re-invested in training, up-skilling and knowledge sharing.

Limitations of current testing and tools

In addition to knowledge gaps within their teams, some AppSec managers also noted a number of limitations they face with their current testing and tools.

This includes challenges with authenticated scanning, the quality of payloads being used, and not being able to test APIs in depth.

There was a general perception that many of the tools available are not good enough to scan APIs effectively for vulnerabilities, with the complexity of API parameters meaning most DAST tools can’t simulate them.

How can you solve these challenges?

While API scanning capability has been in Burp Suite Enterprise Edition for some time, you can now upload OpenAPI definition files directly.

Further updates will allow for the support of SOAP APIs as well, increasing the capability of the scanner to handle a wider range of definitions.

When scanning standalone APIs, you can give Burp Suite Enterprise Edition the credentials needed to authenticate itself, allowing you to automate the scanning of APIs that require auth.

Resource and time to perform tests

Finally, many AppSec and pentesting teams struggle for time and resources to perform the level of testing required to secure their APIs effectively. This means that tests lack detail, and the remediation of issues was slow.

How can you solve these challenges?

As mentioned above, automating and scheduling API scans can help you save time.

Using Burp Suite Enterprise Edition in this way can help you catch low-hanging fruit, meaning your pentesters can spend their time elsewhere.

Secure your APIs with automated, scheduled DAST

These key pain points illustrate the challenge AppSec teams face - not only for the present, but the future too. When teams are struggling to cope with securing current API estates, the challenges around scaling as this grows becomes unfathomable.

Automated DAST scanning is an essential tool in easing this burden, saving time in the short-term and enabling the process and maturity required to scale.

Find out how Burp Suite Enterprise Edition can help solve your API security challenges. Click here to request a free, fully-featured trial in less than 2-minutes.

Rob Samuels

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
