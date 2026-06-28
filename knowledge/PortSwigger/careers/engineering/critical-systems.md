# Critical Systems Engineering Team

Source: https://portswigger.net/careers/engineering/critical-systems
Fetched: 2026-06-28T09:17:00.129222+00:00

Critical Systems Engineering Team

"We work on the tools and systems that all Swiggers use internally to allow them to be as productive as possible in their roles"

Our internal tools are just as important to the company as our external products, and we work hard to provide innovative solutions to problems where off the shelf products simply would not work. We are

also consumers of Burp, utilizing the entire suite to ensure our web-based solutions are as secure as possible.

Leom B, Engineering Manager, Critical Systems

Key functionality

Our system consists of a variety of services, such as our own customer happiness and relationship management system, finance reporting and integration with external systems, business data and dashboards, licensing, etc.

The website is our main digital presence and allows visitors to learn more about who we are, our products, and purchase them. End users can also manage their licenses, contact our support team via the forum, or read the extensive documentation about Burp Suite. Our products are however not everything at PortSwigger. If you are interested in web security, you will find invaluable posts from our talented research team, as well as an ever-growing free learning center, the Web Security Academy.

We like to create the best solution for our needs which often means thinking outside the box and coming up with novel solutions.

Problem space

At PortSwigger, we like to create the best solution for our needs which often means thinking outside the box and coming up with novel solutions. Our software engineers are crafters and builders of truly scalable products.

Some of our services are directly called from Burp instances, so performance at scale is a key requirement of the solutions we deliver.

As the team covers a wide and diverse range of services, no single requirement is the same. We strive to design solutions that address the business need and use the right technology to fit the job, rather than forcing

a requirement fit in to an existing pattern.

Technologies

Our critical systems are running on AWS infrastructure, mainly written in C#, with the addition of JavaScript to enhance the front-end experience. Experience in these specific languages isn't required - we leverage agentic coding and look for engineers who can work effectively across our codebases.

Our tooling includes Jetbrains Rider, xUnit, git, NuGet, TeamCity, Docker, and various AWS services.

What we've been working on

The critical systems team have been working on improving how we collaborate with our customers - this means enabling our internal teams to connect, monitor and keep in

touch with customers as easily as possible.

Whilst our solutions act as the bridge between teams, they also provide some real technical challenges - this mainly stems from the ongoing requirement to maintain an

environment that is both secure and scalable. You'd be surprised at how complicated sending emails in the correct order at pace can be, or searching to return the

information someone wants to see - even just surfacing linked information in an easy way for us to quickly respond to customers has its own challenges.

Our recent projects include:

Using AWS Step Functions to call time-delayed update actions via AWS Lambdas to a .NET Web API endpoint. This project included foresight to being able to

improve these actions in the future with machine learning.

Using .NET background queues with auto-scaling AWS ECS Fargate instances and AuroraDB to create a "send once" system that is designed for high load. The emails

sent from this are constructed using a limited markdown set and templating, with the front end written using JavaScript ES6.

The team also looks after the public facing side of the website and our in-house CMS. This system allows the internal content team to write pages for the website as if they were writing static HTML pages. These pages are contained in a separate source control repository with its own release process.

Content is validated to catch early mistakes such as missing closing tags, missing links, or duplicated headings. The import process is a simple drag and drop of static assets which are then parsed, reduced to their constituent components, and served as dynamic content. Packages are versioned for rollback capability across environments, enabling releases without rebuilding the core site.

Meet the Swiggers

We are a diverse group of people with a wide range of interests and backgrounds. What Swiggers have in common is that they all love their work and are exceptionally good at what they do.

Leom B, Engineering Manager

Mike S, Software Engineer

Mohamed H, Software Engineer

Meet the Swiggers

What we look for

Read more

Rewards

Read more

Application Process

Read more
