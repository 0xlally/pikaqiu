# Algorithm confusion attacks

Source: https://portswigger.net/web-security/jwt/algorithm-confusion
Fetched: 2026-06-28T09:17:52.808418+00:00

Web Security Academy

JWT attacks

Algorithm confusion attacks

Algorithm confusion attacks

Algorithm confusion attacks (also known as key confusion attacks) occur when an attacker is able to force the server to verify the signature of a JSON web token (JWT) using a different algorithm than is intended by the website's developers. If this case isn't handled properly, this may enable attackers to forge valid JWTs containing arbitrary values without needing to know the server's secret signing key.

Symmetric vs asymmetric algorithms

JWTs can be signed using a range of different algorithms. Some of these, such as HS256 (HMAC + SHA-256) use a "symmetric" key. This means that the server uses a single key to both sign and verify the token. Clearly, this needs to be kept secret, just like a password.

Other algorithms, such as RS256 (RSA + SHA-256) use an "asymmetric" key pair. This consists of a private key, which the server uses to sign the token, and a mathematically related public key that can be used to verify the signature.

As the names suggest, the private key must be kept secret, but the public key is often shared so that anybody can verify the signature of tokens issued by the server.

How do algorithm confusion vulnerabilities arise?

Algorithm confusion vulnerabilities typically arise due to flawed implementation of JWT libraries. Although the actual verification process differs depending on the algorithm used, many libraries provide a single, algorithm-agnostic method for verifying signatures. These methods rely on the alg parameter in the token's header to determine the type of verification they should perform.

The following pseudo-code shows a simplified example of what the declaration for this generic verify() method might look like in a JWT library:

function verify(token, secretOrPublicKey){

algorithm = token.getAlgHeader();

if(algorithm == "RS256"){

// Use the provided key as an RSA public key

} else if (algorithm == "HS256"){

// Use the provided key as an HMAC secret key

}

}

Problems arise when website developers who subsequently use this method assume that it will exclusively handle JWTs signed using an asymmetric algorithm like RS256. Due to this flawed assumption, they may always pass a fixed public key to the method as follows:

publicKey = <public-key-of-server>;

token = request.getCookie("session");

verify(token, publicKey);

In this case, if the server receives a token signed using a symmetric algorithm like HS256, the library's generic verify() method will treat the public key as an HMAC secret. This means that an attacker could sign the token using HS256 and the public key, and the server will use the same public key to verify the signature.

Note

The public key you use to sign the token must be absolutely identical to the public key stored on the server. This includes using the same format (such as X.509 PEM) and preserving any non-printing characters like newlines. In practice, you may need to experiment with different formatting in order for this attack to work.

Performing an algorithm confusion attack

An algorithm confusion attack generally involves the following high-level steps:

Obtain the server's public key

Convert the public key to a suitable format

Create a malicious JWT with a modified payload and the alg header set to HS256.

Sign the token with HS256, using the public key as the secret.

In this section, we'll walk through this process in more detail, demonstrating how you can perform this kind of attack using Burp Suite.

Step 1 - Obtain the server's public key

Servers sometimes expose their public keys as JSON Web Key (JWK) objects via a standard endpoint mapped to /jwks.json or /.well-known/jwks.json, for example. These may be stored in an array of JWKs called keys. This is known as a JWK Set.

{

"keys": [

{

"kty": "RSA",

"e": "AQAB",

"kid": "75d0ef47-af89-47a9-9061-7c02a610d5ab",

"n": "o-yy1wpYmffgXBxhAUJzHHocCuJolwDqql75ZWuCQ_cb33K2vh9mk6GPM9gNN4Y_qTVX67WhsN3JvaFYw-fhvsWQ"

},

{

"kty": "RSA",

"e": "AQAB",

"kid": "d8fDFo-fS9-faS14a9-ASf99sa-7c1Ad5abA",

"n": "fc3f-yy1wpYmffgXBxhAUJzHql79gNNQ_cb33HocCuJolwDqmk6GPM4Y_qTVX67WhsN3JvaFYw-dfg6DH-asAScw"

}

]

}

Even if the key isn't exposed publicly, you may be able to extract it from a pair of existing JWTs.

Step 2 - Convert the public key to a suitable format

Although the server may expose their public key in JWK format, when verifying the signature of a token, it will use its own copy of the key from its local filesystem or database. This may be stored in a different format.

In order for the attack to work, the version of the key that you use to sign the JWT must be identical to the server's local copy. In addition to being in the same format, every single byte must match, including any non-printing characters.

For the purpose of this example, let's assume that we need the key in X.509 PEM format. You can convert a JWK to a PEM using the JWT Editor extension in Burp as follows:

With the extension loaded, in Burp's main tab bar, go to the JWT Editor Keys tab.

Click New RSA Key. In the dialog, paste the JWK that you obtained earlier.

Select the PEM radio button and copy the resulting PEM key.

Go to the Decoder tab and Base64-encode the PEM.

Go back to the JWT Editor Keys tab and click New Symmetric Key.

In the dialog, click Generate to generate a new key in JWK format.

Replace the generated value for the k parameter with a Base64-encoded PEM key that you just copied.

Save the key.

Step 3 - Modify your JWT

Once you have the public key in a suitable format, you can modify the JWT however you like. Just make sure that the alg header is set to HS256.

Step 4 - Sign the JWT using the public key

Sign the token using the HS256 algorithm with the RSA public key as the secret.

Deriving public keys from existing tokens

In cases where the public key isn't readily available, you may still be able to test for algorithm confusion by deriving the key from a pair of existing JWTs. This process is relatively simple using tools such as jwt_forgery.py. You can find this, along with several other useful scripts, on the rsa_sign2n GitHub repository.

We have also created a simplified version of this tool, which you can run as a single command:

docker run --rm -it portswigger/sig2n <token1> <token2>

Note

You need the Docker CLI to run either version of the tool. The first time you run this command, it will automatically pull the image from Docker Hub, which may take a few minutes.

This uses the JWTs that you provide to calculate one or more potential values of n. Don't worry too much about what this means - all you need to know is that only one of these matches the value of n used by the server's key. For each potential value, our script outputs:

A Base64-encoded PEM key in both X.509 and PKCS1 format.

A forged JWT signed using each of these keys.

To identify the correct key, use Burp Repeater to send a request containing each of the forged JWTs. Only one of these will be accepted by the server. You can then use the matching key to construct an algorithm confusion attack.

For more information on how this process works, and details of how to use the standard jwt_forgery.py tool, please refer to the documentation provided in the repository.

Read more

For more labs, check out the rest of our topic on JWT attacks.

JWT attacks

Find JWT vulnerabilities using Burp Suite

Try for free
