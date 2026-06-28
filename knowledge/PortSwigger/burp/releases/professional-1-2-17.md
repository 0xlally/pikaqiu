# Professional 1.2.17

Source: https://portswigger.net/burp/releases/professional-1-2-17
Fetched: 2026-06-28T09:16:22.807781+00:00

Burp Scanner now allows reporting of issues in XML format, to enable easy integration with other tools. To create an XML report, simply select the issues you wish to report, and choose XML within the reporting wizard:

The XML has a flat structure, and contains a list of issues, with meta-information about issue type, URL, etc., reported within each issue element. The (internal) DTD looks like this:

<!DOCTYPE issues [

<!ELEMENT issues (issue*)>

<!ATTLIST issues burpVersion CDATA "">

<!ATTLIST issues exportTime CDATA "">

<!ELEMENT issue (serialNumber, type, name, host, path, location, severity, confidence, issueBackground?, remediationBackground?, issueDetail?, remediationDetail?, requestresponse*)>

<!ELEMENT serialNumber (#PCDATA)>

<!ELEMENT type (#PCDATA)>

<!ELEMENT name (#PCDATA)>

<!ELEMENT host (#PCDATA)>

<!ELEMENT path (#PCDATA)>

<!ELEMENT location (#PCDATA)>

<!ELEMENT severity (#PCDATA)>

<!ELEMENT confidence (#PCDATA)>

<!ELEMENT issueBackground (#PCDATA)>

<!ELEMENT remediationBackground (#PCDATA)>

<!ELEMENT issueDetail (#PCDATA)>

<!ELEMENT remediationDetail (#PCDATA)>

<!ELEMENT requestresponse (request?, response?)>

<!ELEMENT request (#PCDATA)>

<!ELEMENT response (#PCDATA)>

]>
