# Find GraphQL API vulnerabilities, with Burp Suite Professional

Source: https://portswigger.net/blog/find-graphql-api-vulnerabilities-with-burp-suite-professional
Fetched: 2026-06-28T09:15:14.991648+00:00

Find GraphQL API vulnerabilities, with Burp Suite Professional

Gareth Heyes |

Tuesday, 4 July 2023 at 13:00 UTC

GraphQL

Burp Suite

scanning

As a penetration tester, you need your tools to find the latest vulnerabilities. GraphQL APIs are widely used on today’s websites, and expose attack surface for a wide range of security issues.

Burp Scanner’s new GraphQL checks will automatically report many instances of GraphQL vulnerabilities on your penetration tests. Get the latest version of Burp Suite Professional, and start finding these issues today.

GraphQL scan checks

We added support for GraphQL in Burp Suite to enable you to detect known endpoints, find hidden endpoints, detect when introspection or suggestions are enabled, and report when an endpoint does not validate the content type.

Finding known endpoints

It can be tedious to manually trawl through a web site to determine the GraphQL endpoint. We've made this easier by getting Burp Scanner to do the work for you. We've defined some passive and active scan checks to find known endpoints automatically, allowing you to focus on finding the vulnerabilities.

Finding hidden endpoints

Sometimes a developer will deploy a GraphQL endpoint without using it on the site - for example, if it was accidentally deployed to production. Burp Suite will look for common endpoints and find hidden GraphQL deployments even without the site using it. These endpoints could be a valuable resource for a tester, as it's likely a vulnerability will be found if it's an accidental deployment.

Detecting introspection

Introspection allows you to run a query on the actual schema to see what queries it supports. It's often turned off in production because a site might not want to expose the inner workings of its API to the world. Burp will detect if introspection is enabled - although this isn't a vulnerability in itself, it could be useful for a tester to aid testing the site and useful for a developer to remind them to turn it off in production.

Detecting suggestions

Some GraphQL servers like Apollo will make suggestions when you make an invalid query, to help you construct a valid one. This can be used by a tester to discover the underlying schema by using a dictionary of words and the suggestion response as an oracle, even when introspection is disabled. A tool such as clairvoyance can be used to construct a valid schema from a dictionary. Burp will enable you to find endpoints that have suggestions enabled and report them.

Invalidated content type

Most GraphQL endpoints use a POST method with an application/json content type. If the content type is validated correctly, then a browser can't make this request without using CORS as it will be unable to send the correct content type. This makes the endpoint secure against CSRF. However, if a site does not validate the content type and does not implement some form of CSRF token, it could be possible to abuse the GraphQL endpoint by forging requests provided mitigations like SameSite cookies can be bypassed or neutralized because of the SameSite None flag. Burp will report if it's possible to forge the request to the endpoint using a GET request or application/x-www-form-urlencoded POST request.

Try it out for yourself

If you want to learn more about GraphQL - including an overview of how it works, discovery and exploitation techniques, and how GraphQL vulnerabilities can lead to information disclosure and CSRF -  take a look at the Web Security Academy. We've prepared thorough learning materials and interactive labs where you can practise your skills - go check them out!

GraphQL

Burp Suite

scanning

Gareth Heyes

@garethheyes

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
