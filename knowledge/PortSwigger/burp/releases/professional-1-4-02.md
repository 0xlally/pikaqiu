# Professional 1.4.02

Source: https://portswigger.net/burp/releases/professional-1-4-02
Fetched: 2026-06-28T09:16:23.893695+00:00

As well as fixing a number of bugs, this release adds a range of cool new features.

1. Burp now supports streaming HTTP responses, and handles these in a way that lets you and the application continue working. Streaming responses are often used for functions like continuously updating price data in trading applications. Typically, some client side script code makes a request, and the server keeps the response stream open, pushing further data in real time as this becomes available. Because intercepting proxies use a store-and-forward model, they can break these applications - the proxy waits indefinitely for the streaming response to finish, and none of it is ever forwarded to the client.

Burp now lets you specify which URLs return streaming responses. The Proxy tool will pass these responses straight through to the client as data is received. The Repeater tool will update the response panel in real time as data is received. Other Burp tools will ignore streaming responses and will close the connections (which is no worse than the way they are handled in prior versions of Burp). Here is the new configuration (under options / HTTP / streaming responses):

In order to view the contents of streaming responses within the Proxy history and Repeater response panel, you will need to check the "store streaming responses" option.

In order to make the responses more human-readable, you can also check the "strip chunked encoding metadata" option, although removing this metadata may break the client-side application, depending on how it is implemented.

Streaming responses are often compressed using gzip encoding - you can configure Burp to decompress this content via the normal options in the Proxy and Repeater configuration.

The new support for streaming responses is also useful for handling responses that are not strictly streaming but nevertheless very large (such as some Flash objects), in order to bypass the store-and-forward proxy model and improve Burp's performance.

2. Burp Intruder has a new ECB Block Shuffler payload type. This is designed for testing ECB-encrypted tokens and other data, to check their vulnerability to block shuffling attacks. Because ECB ciphers always encrypt the same block of plaintext to the same block of ciphertext, it is possible to meaningfully modify the plaintext in a structure by duplicating and shuffling the blocks of ciphertext. Depending on the contents of the structure, and the application's handling of the modified data, it may be possible to interfere with application logic - for example, switching the user ID field in a structured session token, changing an encrypted price, etc.

The configuration for the new payload type looks like this:

You can tell Burp whether to shuffle blocks in the base value for the payload position, or in a supplied string, and you can configure whether the ciphertext is encoded as ASCII hex (which is typically the case) and configure the block size (normally 8 or 16 bytes). You can handle complications like Base64-encoding via the usual payload post-processing rules.

If you aren't sure what exactly the item you are targeting contains, you can try various different settings, since this is not normally a lengthy attack to run.

There is often a large element of luck involved when blindly shuffling blocks in ECB-encrypted data structures, and success often depends upon happening to find a block of ciphertext whose decrypted plaintext contains the right meaningful data when inserted into the structure (such as a number that could be a valid user ID or price). You can dramatically increase the likelihood of success by providing Burp with a large sample of other data that is encrypted using the same cipher and key. For example, in the case of session tokens, you can harvest a large number of valid tokens using Burp Intruder or Sequencer, and configure these in the ECB block shuffling payload, under "obtain additional blocks from these encrypted strings". Burp will then take all of the unique ciphertext blocks that you have provided, and use these when shuffling blocks in the original data. In practice, if you can find suitable additional encrypted data, this method proves highly effective when targeting vulnerable applications.

I've also blogged about an example of using the new ECB block shuffler to compromise sessions in a vulnerable application.

3. Burp has a new UI component to aid configuration in situations where you need to specify interesting parts of HTTP responses. This is an improved version of the configuration used in earlier versions of Burp Sequencer. The new Sequencer configuration for defining a custom token location looks like this:

The easiest way to use this configuration is to select the relevant item within the response. As you make your selection, Burp will automatically show in the top panel various configuration options which specify this item in the current response. If required, you can modify this configuration manually to ensure that it will work across multiple responses. You can also refetch the current response to test that your configuration is specifying the correct item.

Various methods are available of specifying the item's location, including fixed offset and length, literal expressions which precede and delimit the item, or a regex group. (Obviously, the more powerful of these options impose a greater processing overhead at runtime.) There is help available within the UI dialog regarding the appropriate syntax to use with each option.

4. Burp Intruder now has improved extract grep functionality, which makes use of the new response selection configuration:

The new functionality lets you define each extract grep location using the same fine-grained settings as already described for tokens in Sequencer, and each extract grep item is defined independently of the others. This lets you use different options (for delimiter, regex, case sensitivity, etc.) for each item to be extracted, removing an annoying limitation on the prior version of Intruder. You can also specify an overall length limit, to avoid consuming unnecessary memory in the event of misconfiguration or unexpected responses.

Two nice features of the extract grep functionality are:

If you specify identical successive extract grep items (using the copy button), then Burp will search each response from the end of the previous match. In this way, you can easily extract multiple similar data fields from each response with an easy configuration. For example, if responses contain lots of interesting data within an HTML table, you can define multiple successive extract grep items using the regex <td>(.*?)</td> in order to extract the contents of successive cells within the table.

Often, when browsing through the results of an Intruder attack, you will notice some responses with anomalous content, such as an error message, that does not appear within the original base response. If you want to extract a specific string from these responses you can use the context menu within the Intruder results table and choose the "define extract grep from response" option. This will show the extract grep configuration dialog with the specific response you have selected, allowing you to quickly define an extract grep item that will work for responses of this type:

5. A much-requested feature has been added to session-handling macros - the ability to define custom parameter locations within macro responses. In today's Ajax-heavy applications, items such as anti-CSRF tokens are often transmitted to the client within JavaScript or JSON structures; client-side code then processes the item and sends it within the relevant parameter in subsequent requests. Burp previously only identified parameters appearing within HTML forms, URL query strings and other conventional locations, and so could not cope with these kind of tokens.

In the new release, you can configure arbitrary named parameter locations within a macro response, using the same response extraction UI already described. For example, this allows you to specify that a particular JavaScript string contains a parameter with a specific name. When updating parameters in subsequent requests, Burp will update any parameter with that name using the value extracted from the configured location in the prior response:

Some users have identified a further requirement within the macro parameter handling - the ability to deal with and update ephemerally-named parameters, which some applications are using for anti-CSRF defenses. In these applications, the name of the anti-CSRF parameter changes with each request, and Burp is not currently able to automatically update this parameter name via session handling rules. We hope to have a solution for this situation in a future release.
