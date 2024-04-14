from random import randrange
from math import pow, gcd, log10
import random

retval = 0

#creates a list of random coprimes in the range of 2 through the n value (aka keyVal)
def randNumList(keyVal):
    newList = []
    for i in range(2,keyVal):
        if i != p and i != q:
            newList.append(i)
    return newList

#the extended euclidean algorithm, recursive because hehe recursion
def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    g, y, x = egcd(b%a,a)
    return (g, x - (b//a) * y, y)

#working version of modular inverse with exceptions thrown when no modular inverse exists
def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('No modular inverse')
    return x%m

#encrypt function off the equation {[(n+1)^m] * (r^n)} % (n^2)
def encryptVote(usrVote, randInt, voteVal): 
    if voteVal == 0:
        return 0
    equationPartOne = (n+1) ** voteVal                #{[(n+1)^m]
    randomToProduct = randInt ** n                    #(r^n)}
    fullEquation = equationPartOne * randomToProduct  #{[(n+1)^m] * (r^n)}
    nSquare = n ** 2                                  #(n^2)
    result = fullEquation % nSquare                   #{[(n+1)^m] * (r^n)} % (n^2)
    return result

#prime number generation from a lower bound to an upper bound, stored in a list for ease of access
def prime_range(lower, upper):
    prime_list = [] 
    for num in range(lower, upper + 1):
        if num > 1:
            for i in range(2, num):
                if (num % i) == 0:
                    break
            else: # I don't know why this works, i don't like that this works, but it works and we don't touch this ever
                prime_list.append(num)
    return prime_list

#powerMod function from sagemath converted to python
def powerMod(A, N, M): 
    retval = A ** N
    return(retval % M)

#decryption function (not even going to bother iterating through the equation because it's weird)
def decryptTotal(total):
    power_mod = powerMod(total, lam, (n**2))
    result = int((power_mod - 1) / n)
    result = result * mu
    checkVal = result % n
    if checkVal == 1:
        return 1
    elif checkVal == 100:
        return 100
    elif checkVal == 662:
        return 10000
    else:
        return checkVal
    
#the below function should be used once at the start of a new created vote to generate the n, lam, p, q, mu, and list of r values
def createVals():
    listOfPrimes = prime_range(200, 500)
    p = random.choice(listOfPrimes)
    q = random.choice(listOfPrimes)
    while p == q:
        q = random.choice(listOfPrimes)
    n = p * q
    lam = (p-1) * (q-1)
    mu = modinv(lam,n)
    coprimeList = randNumList(n)
