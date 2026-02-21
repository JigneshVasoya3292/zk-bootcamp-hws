# private key (number
# public key = private key * G (point on the curve)
import hashlib
import random
from ecpy.curves import Curve

# for secp256k1 curve

# order
n = 115792089237316195423570985008687907852837564279074904382605163141518161494337
# Generator
G = [55066263022277343669578718895168534326250603453777594175500187360389116729240, 32670510020758816978083085130507043184471273380659243275938904335757337482424]

msg = "Hello"
privKey = 0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80

def ecdsa_sign(msg, privKey):
    print(f"------ Signing {msg} ------- \n")
    # h = hash(msg) sha-256 hash
    # k = random number between 1 to n-1 (MUST be unique per signature!)
    # R = k * G
    # r = R.x
    # s = k^-1 * (h + r*privKey) (mod n)
    # {r, s} is signature
    
    # Generate fresh k for each signature (CRITICAL for security)
    k = random.randint(1, n-1)
    
    msg_encoded = msg.encode('utf-8')
    h = hashlib.sha256(msg_encoded)
    h_digest = h.hexdigest()
    print(f"The SHA256 hash of '{msg}' is: {h_digest}")
    print(f"k is '{k}'")
    cv = Curve.get_curve('secp256k1')
    R = k * cv.generator 
    print(f"R is '{R}'")
    r = R.x # You can use R.y as well, but then use the same in the verification step
    
    # Reject invalid signatures (r == 0)
    if r == 0:
        raise ValueError("Invalid signature: r == 0, must retry with different k")
    
    print(f"r is '{r}'")
    k_inv = pow(k, -1, n)
    print(f"k_inv is '{k_inv}'")
    hash_int = int.from_bytes(h.digest(), 'big')
    s = (k_inv * (hash_int + (r*privKey))) % n
    
    # Reject invalid signatures (s == 0)
    if s == 0:
        raise ValueError("Invalid signature: s == 0, must retry with different k")
    
    print(f"s is '{s}' \n")
    return [r, s]
    

def ecdsa_pubkey(privKey):
    print("------ Generating Public Key ------- \n")
    cv     = Curve.get_curve('secp256k1')
    pub_key = privKey * cv.generator 
    print(f"pub_key is '{pub_key}' \n")
    return pub_key

def verify_ecdsa(msg, pub_key, r, s):
    # h = hash(msg) sha-256 hash
    # s_inv = modular inverse of s
    # R_p is R' = (h * s^-1) * G + (r * s^-1) * pubKey
    # r_p is r' = R'.x
    # verification is r == r'
    print("------ Verification ------- \n")
    
    # Reject invalid signatures
    if r == 0 or r >= n:
        print("Invalid signature: r out of valid range")
        return False
    if s == 0 or s >= n:
        print("Invalid signature: s out of valid range")
        return False
    
    msg_encoded = msg.encode('utf-8')
    h = hashlib.sha256(msg_encoded)
    h_digest = h.hexdigest()
    print(f"The SHA256 hash of '{msg}' is: {h_digest}")
    cv = Curve.get_curve('secp256k1')
    s_inv = pow(s, -1, n)
    hash_int = int.from_bytes(h.digest(), 'big')
    R_p = ((hash_int * s_inv) * cv.generator) + ((r * s_inv) * pub_key)
    r_p = R_p.x
    print(f"r_p is: {r_p}")
    print(f"r is: {r}")
    is_valid = (r == r_p)
    print(f"r == r_p is {is_valid} \n")
    return is_valid

def sign_and_verify(msg, privKey):
    pub_key = ecdsa_pubkey(privKey)
    rs = ecdsa_sign(msg, privKey)
    verify_ecdsa(msg, pub_key, rs[0], rs[1])
   
 
sign_and_verify("Hello", privKey)

# READ : https://cryptobook.nakov.com/digital-signatures/ecdsa-sign-verify-messages
