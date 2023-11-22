import random
import math
def is_prime(number):
    if number<2:
        return False
    for i in range(2,sqrt(number)):
        if number%i==0:
            return False
    return True
def generate_prime(min_value,max_value):
    prime=random.randint(min_value,max_value)
    while not is_prime(prime):
        prime=random.randint(min_value,max_value)
    return prime

def mod_inverse(e,phi):
    for d in range(3,phi):
        if (d*e)%phi==1:
            return d
    raise ValueError('No mod inverse found')

p,q=generate_prime(1000,5000), generate_prime(1000,5000)
while p==q:
    q=generate_prime(1000,5000)
n=p*q
phi=(p-1)*(q-1)

e=random.randint(3,phi-1)
while math.gcd(e,phi)!=1:
    e=random.randint(3,phi-1)

d=mod_inverse(e,phi)

print('Public key: ', e)
print('Private key: ', d)
print('n: ', n)
print('phi: ', phi)
print('p: ', p)
print('q: ', q)

message=input('Enter message: ')

encoded_message=[ord(char) for char in message]
cipher= [pow(char,e,n) for char in encoded_message]

print('Cipher: ', cipher)

decoded_message=[chr(pow(char,d,n)) for char in cipher]
message=''.join(chr(char) for char in encoded_message)
print('Decoded message: ', message)
