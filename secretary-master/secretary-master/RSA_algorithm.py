# author: github/lia0wang
# last modified: 4/4/2022
import random
import math
from sre_compile import isstring

# determine whether a num is a prime
def is_prime(num):
    # case: 0, 1
    if num < 2:
        return False
    # case: num > 3
    for i in range(3, num):
        if num % i == 0:
            return False
    else:
        return True

# generate two primes out of range 2->100
def generate_two_primes():
    primes = [i for i in range(11, 100) if is_prime(i)]
    p = random.choice(primes)
    q = random.choice(primes)
    while q == p:
        q = random.choice(primes)
    # return (p, q) where p != q    
    return (p, q)

# calculate N= p*q
def calculate_N(tuple):
    p, q = tuple
    return p * q

# find the Euler’s Totient
def calculate_phi(tuple):
    p, q = tuple
    return (p - 1) * (q - 1)

def select_e(phi):
    e = random.randrange(1, phi)
    while math.gcd(e, phi) != 1 or e == mod_inverse(e, phi):
        e = random.randrange(1, phi)
    return e
    
# calculate d where d inverse of e (mod phi(n))
def mod_inverse(e, phi):
    for x in range(1, phi):
        if (e * x) % phi == 1:
            return x
    return -1

# encrypt str use public key
def encrypt_RSA(str, public):
    e, n = public
    encrypt_str = [pow(ord(c), e, n) for c in str]
    return encrypt_str

# decrypt str use private key
def decrypt_RSA(str, private):
    d, n = private
    decrypt_str = [chr(pow(c, d, n)) for c in str]
    return decrypt_str

if __name__ == "__main__":
    while 1:
        p_q = generate_two_primes()
        n = calculate_N(p_q)
        phi = calculate_phi(p_q)
        e = select_e(phi)
        d = mod_inverse(e, phi)

        public = (e, n)
        private = (d, n)

        msg = "ldl@qad.com"
        msg2 = "bjdksbnadksdnas,/."

        encrypt_msg = encrypt_RSA(msg, public)
        encrypt_msg2 = encrypt_RSA(msg2, public)
        print(encrypt_msg)
        print(encrypt_msg2)

        decrypt_msg = ','.join(decrypt_RSA(encrypt_msg, private)).replace(',','')
        decrypt_msg2 = ','.join(decrypt_RSA(encrypt_msg2, private)).replace(',','')
        assert(isstring(decrypt_msg))
        assert(isstring(decrypt_msg2))
        print(decrypt_msg)
        print(decrypt_msg2)
