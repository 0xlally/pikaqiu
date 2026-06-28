# Unearthing Z͌̈́̾a͊̈́l͊̿g̏̉͆o̾̚̚S̝̬ͅc̬r̯̼͇ͅi̼͖̜̭͔p̲̘̘̹͖t̠͖̟̹͓͇ͅ with visual fuzzing

Source: https://portswigger.net/research/unearthing-zalgoscript-with-visual-fuzzing
Fetched: 2026-06-28T09:17:31.718609+00:00

Unearthing Z͌̈́̾a͊̈́l͊̿g̏̉͆o̾̚̚S̝̬ͅc̬r̯̼͇ͅi̼͖̜̭͔p̲̘̘̹͖t̠͖̟̹͓͇ͅ with visual fuzzing

Gareth Heyes

Researcher

@garethheyes

Published: Wednesday, 7 March 2018 at 15:46 UTC

Updated: Wednesday, 2 June 2021 at 13:11 UTC

This is valid JavaScript on Edge:

̀̀̀̀̀́́́́́̂̂̂̂̂̃̃̃̃̃̄̄̄̄̄̅̅̅̅̅̆̆̆̆̆̇̇̇̇̇̈̈̈̈̈̉̉̉̉̉̊̊̊̊̊ͅͅͅͅͅͅͅͅͅͅͅalert(̋̋̋̋̋̌̌̌̌̌̍̍̍̍̍̎̎̎̎̎̏̏̏̏̏ͅͅͅͅͅ1̐̐̐̐̐̑̑̑̑̑̒̒̒̒̒̓̓̓̓̓̔̔̔̔̔ͅͅͅͅͅ)̡̡̡̡̡̢̢̢̢̢̛̛̛̛̛̖̖̖̖̖̗̗̗̗̗̘̘̘̘̘̙̙̙̙̙̜̜̜̜̜̝̝̝̝̝̞̞̞̞̞̟̟̟̟̟̠̠̠̠̠̣̕̕̕̕̕̚̚̚̚̚ͅͅͅͅͅͅͅͅͅͅͅͅͅͅͅ

How did we get here?

When twitter increased their tweet character limit 140 to 280 I thought it might be fun to see what unicode characters could be used with the new limit. I tweeted some interesting characters that caused rendering errors in Twitter. This is known as Zalgo. It got me thinking about how to automatically identify these characters. You can’t use the DOM to see if certain characters behave strangely, I needed a screenshot to see what the browser sees. I first started off with JavaScript and canvas to take a screenshot but the picture generated did not match the actual display rendered in the browser. I needed another approach. Headless Chrome was the answer! I used puppeteer which is a NodeJS module that lets you control headless Chrome and take screenshots.

Generating the characters

To generate Zalgo you can either repeat single characters or combine two characters and repeat the second one. The following code points generate visual defects when repeated on their own, they are mostly unicode combining characters:

834, 1425, 1427, 1430, 1434, 1435, 1442, 1443, 1444, 1445, 1446, 1447, 1450, 1453, 1557, 1623, 1626, 3633, 3636, 3637, 3638, 3639, 3640, 3641, 3642, 3655, 3656, 3657, 3658, 3659, 3660, 3661, 3662

For example the following JavaScript will generate visual defects using one of the characters above.

<script>document.write(String.fromCharCode(834).repeat(20))</script>

This looks like: ͂͂͂͂͂͂͂͂͂͂͂͂͂͂͂͂͂͂͂͂

What's interesting is that multiple characters can combine and produce different effects. Take the characters 311 and 844 - when combined using the same technique as above they go upwards:

<script> document.write(String.fromCharCode(311)+String.fromCharCode(844).repeat(20)) </script>

This looks like: ķ͌͌͌͌͌͌͌͌͌͌͌͌͌͌͌͌͌͌͌͌

Building the fuzzer

The fuzzer is quite simple. First off we need a webpage to actually render the characters, and some CSS to make it extremely wide so legitimate characters will simply go to the right of the screen and I can therefore check the areas to the left, top and bottom of the rendered page and I center the fuzz div element on the page.

Here is a screenshot of characters “a” and “b” rendered in the fuzzer.To help visualize what the fuzzer does here is a screenshot of the regions it checks.

Here is a screenshot with the characters ķ and ͂ which are code points 311 and 834. They cause an interesting defect that the fuzzer logs because it appears in the upper region.

<style>

.parent {

position: absolute;

height: 50%;

width: 50%;

top: 50%;

-webkit-transform: translateY(-50%);

-moz-transform: translateY(-50%);

-ms-transform: translateY(-50%);

-o-transform: translateY(-50%);

transform: translateY(-50%);

}

.fuzz {

height: 300px;

width:5000px;

position: relative;

left:50%;

top: 50%;

transform: translateY(-50%);

}

</style>

</head>

<body>

<div class="parent">

<div class="fuzz" id="test"></div>

</div>

<script>

var chars = location.search.slice(1).split(',');

if(chars.length > 1) {

document.getElementById('test').innerHTML = String.fromCharCode(chars[0])+String.fromCharCode(chars[1]).repeat(100);

} else {

document.getElementById('test').innerHTML = String.fromCharCode(chars[0]).repeat(100);

}

</script>

The JavaScript simply reads one or two character numbers from the query string and outputs them using innerHTML and String.fromCharCode. This is executed client side of course.

Then in NodeJS I use the libraries png and puppeteer.

const PNGReader = require('png.js');

const puppeteer = require('puppeteer');

Then I have two functions that check if a pixel is white and if it’s within the region I want e.g. top, left or bottom.

function isWhite(pixel) {

if(pixel[0] === 255 && pixel[1] === 255 && pixel[2] === 255) {

return true;

} else {

return false;

}

}

function isInRange(x,y) {

if(y <= 120) {

return true;

}

if(y >= 220) {

return true;

}

if(x <= 180) {

return true;

}

return false;

}

The fuzz browser function is asynchronous and takes the screenshot and using the png library to read the png file. It outputs interesting characters (defined by the pixel is not white and appears in the regions top, left or bottom) to the console and also a chars.txt text file.

async function fuzzBrowser(writeStream, page, chr1, chr2) {

if(typeof chr2 !== 'undefined') {

await page.goto('http://localhost/visualfuzzer/index.php?'+chr1+','+chr2);

} else {

await page.goto('http://localhost/visualfuzzer/index.php?'+chr1);

}

await page.screenshot({clip:{x:0,y:0,width: 400,height: 300}}).then((buf)=>{

var reader = new PNGReader(buf);

reader.parse(function(err, png){

if(err) throw err;

outerLoop:for(let x=0;x<400;x++) {

for(let y=0;y<300;y++) {

if(!isWhite(png.getPixel(x,y)) && isInRange(x,y)) {

if(typeof chr2 !== 'undefined') {

writeStream.write(chr1+','+chr2+'\n');

console.log('Interesting chars: '+chr1+','+chr2);

} else {

writeStream.write(chr1+'\n');

console.log('Interesting char: '+chr1);

}

break outerLoop;

}

}

}

});

});

}

I then have an asynchronous anonymous function that loops through the target characters and calls the fuzzBrowser function. When testing for multiple characters I exclude the single characters that cause side effects.

(async () => {

const browser = await puppeteer.launch();

const page = await browser.newPage();

const singleChars = {834:1,1425:1,1427:1,1430:1,1434:1,1435:1,1442:1,1443:1,1444:1,1445:1,1446:1,1447:1,

1450:1,1453:1,1557:1,1623:1,1626:1,3633:1,3636:1,3637:1,3638:1,3639:1,3640:1,3641:1,

3642:1,3655:1,3656:1,3657:1,3658:1,3659:1,3660:1,3661:1,3662:1};

const fs = require('fs');

let writeStream = fs.createWriteStream('logs.txt', {flags: 'a'});

for(let i=768;i<=879;i++) {

for(let j=768;j<=879;j++) {

if(singleChars[i] || singleChars[j]) {

continue;

}

process.stdout.write("Fuzzing chars "+i+","+j+" \r");

await fuzzBrowser(writeStream, page, i, j).catch(err=>{

console.log("Failed fuzzing browser:"+err);

});

}

}

await browser.close();

await writeStream.end();

})();

ZalgoScript

A while ago I found an interesting bug on Edge. Basically Edge is treating characters as whitespace that it shouldn’t. It appears to be unicode combining characters that exhibit this behaviour. What if we combine this bug with Zalgo? We then have ZalgoScript! I first generated a list of characters that Edge treats as whitespace (of which there are a lot, check the github issue for the list). I decided to fuzz the characters 768-879 (the fuzzer code includes that range by default), the fuzzer logged that character 837 along with any character within the 768-879 range produced side effects. This is cool; I could loop through this list and combine characters to produce Zalgo that was also valid JavaScript.

a= [];

for(i=768;i<=858;i++){

a.push(String.fromCharCode(837)+String.fromCharCode(i).repeat(5));

}

a[10]+='alert('

a[15]+='1';

a[20]+=')';

input.value=a.join('')

eval(a.join(''));

And that’s how we ended up with ̀̀̀̀̀́́́́́̂̂̂̂̂̃̃̃̃̃̄̄̄̄̄̅̅̅̅̅̆̆̆̆̆̇̇̇̇̇̈̈̈̈̈̉̉̉̉̉̊̊̊̊̊ͅͅͅͅͅͅͅͅͅͅͅalert(̋̋̋̋̋̌̌̌̌̌̍̍̍̍̍̎̎̎̎̎̏̏̏̏̏ͅͅͅͅͅ1̐̐̐̐̐̑̑̑̑̑̒̒̒̒̒̓̓̓̓̓̔̔̔̔̔ͅͅͅͅͅ)̡̡̡̡̡̢̢̢̢̢̛̛̛̛̛̖̖̖̖̖̗̗̗̗̗̘̘̘̘̘̙̙̙̙̙̜̜̜̜̜̝̝̝̝̝̞̞̞̞̞̟̟̟̟̟̠̠̠̠̠̣̕̕̕̕̕̚̚̚̚̚ͅͅͅͅͅͅͅͅͅͅͅͅͅͅͅ

Source code for Visual Fuzzer

If you liked this, you may also be interested in non-alphanumeric JavaScript.

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
