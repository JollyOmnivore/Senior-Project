# Homomorphic Encryption Math
#Original Concept and Mathematics: Jeremy Muskat, Ph.D.
#Written By: Joseph (Joe) Vennard, with support from William (Willow) Keenan-Harte
#Addapted to Server (Hamfistedly) By: William (Willow) Keenan-Harte

"""
    N value never changes, only r that changes :D
    define a checker for coprime nums; i.e., check to see if the only factor shared between n and i is 1
"""



import random
import json
import gmpy2

#prepare json files for arrays
with open('instance/prime_numbers.json', 'r') as f:
    data = json.load(f)
primesListBig = data['10kPrimeList']
with open('instance/prime_numbers99980001.json', 'r') as k:
    data = json.load(k)
rValsList = data['1MPrimeList']


# creates a list of random coprimes in the range of 2 through the n value (aka keyVal)
def randNumList(keyVal, p, q):
    newList = []
    for i in range(2, keyVal):
        if i != p and i != q:
            newList.append(i)
    return newList


# the extended euclidean algorithm, recursive because hehe recursion
def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    g, y, x = egcd(b % a, a)
    return (g, x - (b // a) * y, y)


# working version of modular inverse with exceptions thrown when no modular inverse exists
def encryptVote(randInt, voteVal, n):
    if voteVal == 0:
        return 0
    equationPartOne = gmpy2.powmod(n+1, voteVal, n**2)
    randomToProduct = gmpy2.powmod(randInt, n, n**2)
    fullEquation = gmpy2.mul(equationPartOne, randomToProduct) % (n**2)
    return int(fullEquation)


def modinv(a, m):
    # Using gmpy2 for computing modular inverse
    return int(gmpy2.invert(a, m))


def powerMod(A, N, M):
    return int(gmpy2.powmod(A, N, M))


def decryptTotal(total, lam, n, mu):
    power_mod = powerMod(total, lam, n**2)
    result = (power_mod - 1) // n
    result = result * mu % n
    return int(result)
# prime number generation from a lower bound to an upper bound, stored in a list for ease of access


# the below function should be used once at the start of a new created vote to
# generate the n, lam, p, q, mu, and list of r values
def createVals():
    p = random.choice(primesListBig) #swap to primesListBig
    q = random.choice(primesListBig) #when json time
    while p == q:
        q = random.choice(primesListBig) #here too
    n = p * q
    lam = (p - 1) * (q - 1)
    mu = modinv(lam, n)


def createVals():
  p = random.choice(primesListBig) # random prime value 1
  q = random.choice(primesListBig) # random prime value 2
  while (p == q) or (p < 6000) or (q < 6000) or (p > 10000) or (q > 10000): # ensures p and q are not the same
    p = random.choice(primesListBig) # random prime value 1
    q = random.choice(primesListBig) # random prime value 2
  n = p * q # get prime product
  lam = (p-1) * (q-1) # get val of p-1 * q-1 for later use & security
  mu = modinv(lam,n) # get mod inverse of lam and n
  return n, p, q, lam, mu, rValsList


def tallyUp(actualResult):
    #init all votes as zeros, just to be sure.
    totalVotesA\
        =totalVotesB\
        =totalVotesC\
        =totalVotesD\
        =totalNoVotes\
        =totalVotersCounted = 0

    while (actualResult - 1000000) >= 0:
        # print("vote for D")
        actualResult -= 1000000
        totalVotesD += 1
        totalVotersCounted += 1

    # checks for total amount of 'C' vals
    while (actualResult - 10000) >= 0:
        # print("vote for C")
        actualResult -= 10000
        totalVotesC += 1
        totalVotersCounted += 1

    # checks for total amount of 'B' vals
    while (actualResult - 100) >= 0:
        # print("vote for B")
        actualResult -= 100
        totalVotesB += 1
        totalVotersCounted += 1

    # checks for total amount of 'A' vals
    while (actualResult - 1) >= 0:
        # print("vote for A")
        actualResult -= 1
        totalVotesA += 1
        totalVotersCounted += 1

    #Replace with abstain code when ready.
    #totalNoVotes = 10 - totalVotersCounted
    return totalVotesA, totalVotesB, totalVotesC, totalVotesD#, totalNoVotes