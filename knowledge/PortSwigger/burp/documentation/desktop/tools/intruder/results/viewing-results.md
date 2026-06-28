# Viewing attack results

Source: https://portswigger.net/burp/documentation/desktop/tools/intruder/results/viewing-results
Fetched: 2026-06-28T09:16:05.025389+00:00

Support Center

Documentation

Desktop editions

Tools

Intruder

Results

Viewing results

ProfessionalCommunity Edition

Viewing attack results

Last updated:

June 18, 2026

Read time:

2 Minutes

You can view details of every request and response issued in the attack in the results window. Results are displayed in a table in the Results tab.

As you review your results, you can view and edit key details of the attack in the configuration side panel. You can check payload positions in the Positions tab.

Related pages

For more information on adjusting the attack configuration while the attack is running, or after the attack has finished, see Editing attacks.

The following information is available in the results table:

Request - The request index number. If the attack was configured to make an unmodified baseline request, this appears as item number 0 in the table.

Position - The position number for the current payload (for Sniper attacks with more than one payload position).

Payload - The payload(s) used in the request.

Status code - The HTTP status code.

Time of day - The time of day the request was made.

Response received - The time taken to begin receiving a response (in milliseconds).

Response completed - The time taken for the response to complete (in milliseconds).

Error - Whether a network error occurred when issuing the request.

Timeout - Whether a timeout occurred when waiting for or processing the response.

Length - The length of the response in bytes.

Cookies - Any cookies received in the response.

Comment - Any user-applied comment.

The following details are also available if the appropriate settings are configured:

The results of any match grep items.

The data extracted from any extract grep items.

Whether or not the payload was echoed in the response, if payload grep was configured.

Redirects followed - The number of redirections that were followed.

Interactions - The number of interactions made with the Collaborator server as a result of the Collaborator payloads. This is only present for an attack that uses the Collaborator payloads payload type.

You can customize and sort the table, and copy column data to your clipboard. For more information, see Customizing Burp's tables.

Related pages

For more information on how to refine your configuration and restart the attack after viewing the initial results, see

Editing attacks.

For more information on redirections and the grep configuration settings, see Burp Intruder

settings.

Payload types - Collaborator payloads.

Viewing a request

Select any item in the table to view the request and response.

If an attack is configured to follow redirections, Burp also displays all intermediate responses and requests.

If the attack resulted in an interaction with the Collaborator server, Burp displays the interaction details. This is only relevant for an attack that uses the

Collaborator payloads payload type.

Double-click an item to open the request and response in a new window.

Related pages

Burp Intruder has a range of functions to help you analyze the results, for more information see Analyzing

attack results.
