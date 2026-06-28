# Freddy, Deserialization Bug Finder

Source: https://portswigger.net/bappstore/ae1cce0c6d6c47528b4af35faebc3ab3
Fetched: 2026-06-28T09:14:55.782728+00:00

Support Center

BApp Store

Freddy, Deserialization Bug Finder

Professional

Freddy, Deserialization Bug Finder

Download BApp

Helps with detecting and exploiting serialization libraries/APIs.

This useful extension was originally developed by Nick Bloor (@nickstadb) for NCC Group and is mainly based on the work of Alvaro Munoz and Oleksandr Mirosh,

Friday the 13th: JSON Attacks which they presented at Black Hat USA 2017 and Def Con 25.

In their work they reviewed a range of JSON and XML serialization libraries for Java and .NET and found that many of them support serialization of arbitrary runtime objects and

as a result are vulnerable in the same way as many serialization technologies are - snippets of code (POP gadgets) that execute during or soon after deserialization can be

controlled using the properties of the serialized objects, often opening up the potential for arbitrary code or command execution.

Further modules supporting more formats including YAML and AMF are also included, based on the paper

Java Unmarshaller Security - Turning your data into code execution

and tool marshalsec by Moritz Bechler.

Freddy Features:

Passive Scanning - Freddy can passively detect the use of potentially dangerous serialization libraries and APIs by watching for type specifiers or other signatures in HTTP requests and by monitoring HTTP responses for exceptions issued by the target libraries. For example the library FastJson uses a JSON field $types to specify the type of the serialized object.

Active Scanning - Freddy includes active scanning functionality which attempts to both detect and, where possible, exploit affected libraries.

Active scanning attempts to detect the use of vulnerable libraries using three methods:

Exception Based - In exception-based active scanning, Freddy inserts data into the HTTP request that should trigger a known target-specific exception or error message. If this error message is observed in the application's response then an issue is raised.

Time Based - In some cases time-based payloads can be used for detection because operating system command execution is triggered during deserialization and this action

blocks execution until the OS command has finished executing. Freddy uses payloads containing ping [-n|-c] 21 127.0.0.1 in order to induce a time delay in these cases.

Collaborator Based - Collaborator-based payloads work either by issuing a nslookup command to resolve the Burp Suite Collaborator-generated domain name, or by attempting

to load remote classes from the domain name into a Java application. Freddy checks for new Collaborator issues every 60 seconds and marks them in the issues list with RCE (Collaborator).

The following targets are currently supported:

Java

BlazeDS AMF 0 (detection, RCE)

BlazeDS AMF 3 (detection, RCE)

BlazeDS AMF X (detection, RCE)

Burlap (detection, RCE)

Castor (detection, RCE)

FlexJson (detection)

Genson (detection)

Hessian (detection, RCE)

Jackson (detection, RCE)

JSON-IO (detection, RCE)

JYAML (detection, RCE)

Kryo (detection, RCE)

Kryo using StdInstantiatorStrategy (detection, RCE)

ObjectInputStream (detection, RCE)

Red5 AMF 0 (detection, RCE)

Red5 AMF 3 (detection, RCE)

SnakeYAML (detection, RCE)

XStream (detection, RCE)

XmlDecoder (detection, RCE)

YAMLBeans (detection, RCE)

.NET

BinaryFormatter (detection, RCE)

DataContractSerializer (detection, RCE)

DataContractJsonSerializer (detection, RCE)

FastJson (detection, RCE)

FsPickler JSON support (detection)

FsPickler XML support (detection)

JavascriptSerializer (detection, RCE)

Json.Net (detection, RCE)

LosFormatter (detection, RCE) - Note not a module itself, supported through ObjectStateFormatter

NetDataContractSerializer (detection, RCE)

ObjectStateFormatter (detection, RCE)

SoapFormatter (detection, RCE)

Sweet.Jayson (detection)

XmlSerializer (detection, RCE)

Author

Author

NCC Group

Version

Version

2.2.4

Rating

Rating

Popularity

Popularity

Last updated

Last updated

02 April 2020

Estimated system impact

Estimated system impact

Overall impact:

Medium

Memory

Medium

CPU

Low

General

Low

Scanner

Medium

You can install BApps directly within Burp, via the BApp Store feature in the Burp Extender tool. You can also download them from here, for offline installation into Burp.

You can view the source code for all BApp Store extensions on our

GitHub page.

Follow

@BApp_Store on Twitter to receive notifications of all BApp releases and updates.

Please note that extensions are written by third party users of Burp, and PortSwigger Web Security makes no warranty about their quality or usefulness for any particular purpose.

Go back to

BappStore

Note:

Please note that extensions are written by third party users of Burp, and PortSwigger Web Security makes no warranty about their quality or usefulness for any particular purpose.
