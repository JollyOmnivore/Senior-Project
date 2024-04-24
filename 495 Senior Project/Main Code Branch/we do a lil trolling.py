from random import randrange
from math import gcd, log10
import random, math
import numpy as np
import json
import sys
sys.set_int_max_str_digits(100000)
import gmpy2
gmpy2.get_context().precision=1000  # Adjust precision if necessary

with open('prime_numbers.json', 'r') as f:
    data = json.load(f)
primesListBig = data['10kPrimeList']
with open('prime_numbers99980001.json', 'r') as k:
    data = json.load(k)
rValsList = data['1MPrimeList']

def encryptVote(randInt, voteVal, n): 
    if voteVal == 0:
        return 0
    equationPartOne = gmpy2.powmod(n+1, voteVal, n**2)
    randomToProduct = gmpy2.powmod(randInt, n, n**2)
    fullEquation = gmpy2.mul(equationPartOne, randomToProduct) % (n**2)
    return fullEquation

def modinv(a, m):
    # Using gmpy2 for computing modular inverse
    return int(gmpy2.invert(a, m))

def powerMod(A, N, M): 
    return int(gmpy2.powmod(A, N, M))

def decryptTotal(total, lam, n, mu):
    power_mod = powerMod(total, lam, n**2)
    result = (power_mod - 1) // n
    result = result * mu % n
    return result
    
# Main voting and setup logic...
p = random.choice(primesListBig)
q = random.choice([x for x in primesListBig if x != p and 1500 <= x <= 2000])
n = p * q
lam = (p-1) * (q-1)
mu = modinv(lam, n)

# Test with a single vote...
r = random.choice(rValsList)
while r < 50 or r > n:
    r = random.choice(rValsList)


votelist = []

encryptedVote = encryptVote(r, 1000000, n)
print("Encrypted vote:", encryptedVote)
votelist.append(encryptedVote)

encryptedVote = encryptVote(r, 100, n)
print("Encrypted vote:", encryptedVote)
votelist.append(encryptedVote)

encryptedVote = encryptVote(r, 10, n)
print("Encrypted vote:", encryptedVote)
votelist.append(encryptedVote)

encryptedVote = encryptVote(r, 10, n)
print("Encrypted vote:", encryptedVote)
votelist.append(encryptedVote)

encryptedVote = encryptVote(r, 10000, n)
print("Encrypted vote:", encryptedVote)
votelist.append(encryptedVote)

encryptedVote = encryptVote(r, 10000, n)
print("Encrypted vote:", encryptedVote)
votelist.append(encryptedVote)

encryptedVote = encryptVote(r, 1000000, n)
votelist.append(encryptedVote)

product = math.prod(votelist)


decryptedVote = decryptTotal(product, lam, n, mu)
print("Encrypted vote:", encryptedVote)
print("Decrypted vote:", decryptedVote)

