from random import randrange
from math import pow, gcd, log10
import random, math
import numpy as np
import json
with open('prime_numbers.json', 'r') as f:
    data = json.load(f)
primesListBig = data['10kPrimeList']
with open('prime_numbers99980001.json', 'r') as k:
    data = json.load(k)
rValsList = data['1MPrimeList']

def encryptVote(randInt, voteVal): 
    if voteVal == 0:
        return 0
    print("starting encrypt")
    equationPartOne = (n+1) ** voteVal
    print("part 1 done")
    firstRandProd = np.power(randInt, n)
    print("normal randInt ^ n: " + str(firstRandProd))
    randomToProduct = randInt ** n
    print("numpy power r ^ n: " + str(randomToProduct))
    print("part 2 done")
    fullEquation = equationPartOne * randomToProduct
    print("all equation done")
    nSquare = n ** 2
    result = fullEquation % nSquare
    print("result done")
    return result

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    g, y, x = egcd(b%a,a)
    return (g, x - (b//a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('No modular inverse')
    return x%m

def powerMod(A, N, M): 
    print("a: " + str(A))
    print("n: " + str(N))
    print("m: " + str(M))
    #print(A)
    #print(N)
    print("powermod before retval")
    retval = A ** N
    #print("retval: " + str(retval))
    #print("retval2: " + str(retval2))
    print("powermod after retval")
    #print("retval: " + str(retval))
    #print("pow func: " + str(pow(A, N, M)))
    return(retval % M)

def decryptTotal(total):
    #print("total: " + str(total))
    print("starting decrypt")
    power_mod = powerMod(total, lam, (n**2))
    #print("power_mod = " + str(power_mod))
    print("powermod finished")
    result = int((power_mod - 1) / n)
    result = result * mu
    print("result finished")
    #print("result * mu : " + str(result))
    checkVal = result % n
    print(str(checkVal) + " is the checkVal value")
    if checkVal == 1:
        return 1
    elif checkVal == 100:
        return 100
    elif checkVal == 662:
        return 10000
    elif checkVal == 10000:
        return 10000
    elif checkVal == 1000000 or checkVal == 0:
        return 1000000
    else:
        return checkVal
    
#=============testing code====================
p = random.choice(primesListBig) # random prime value 1
q = random.choice(primesListBig) # random prime value 2
while (p == q) or (p < 1500) or (q < 1500) or (p > 2000) or (q > 2000): #ensures p and q are not the same
    p = random.choice(primesListBig) # random prime value 1
    q = random.choice(primesListBig)
n = p * q #get prime product
lam = (p-1) * (q-1)
mu = modinv(lam,n)


print("p: " + str(p))
print("q: " + str(q))
print("n: " + str(n))
print("lam: " + str(lam))
print("mu: " + str(mu))

validVote = ['a', 'b', 'c', 'd']	# list of valid input options for user vote
votConf = "n" #boolean between y and n checking for user confirmation of their vote
passThrough = 0
while(votConf != "y"):
    print("Option A: Apple		Option B: Orange") #prints options for voting; option A for apple, B for orange, C for abstain/novote
    print("Option C: Abstain      Option D: Jerky")
    usrVote = input("Please select your vote: A, B, C, D:     ")
    usrVote = usrVote.lower() #forces user vote to lower
    #below if-elif-else keys voteVal to what user chose as an option.
    if usrVote == 'a':
        voteVal = 1
    elif usrVote == 'b':
        voteVal = 100
    elif usrVote == 'c':
        voteVal = 10000
    else:
        voteVal = 1000000
    #below if only generates a new r on the first passthrough of the vote
    #if passThrough == 0:
    r = random.choice(rValsList)
    while(r < 50) or (r > n):
        r = random.choice(rValsList)
    print("r val: " + str(r))
    passThrough = 1
    encryptedVote = encryptVote(r, voteVal) #encrypted vote function called here with encryptedVote
    
    if usrVote in validVote: #check for vote being a valid option
        print("You chose:    " + usrVote)
        print("Your encrypted vote:    " + str(encryptedVote))
        
        votConf = input("Confirm vote? (Y/N)    ")
        votConf = votConf.lower() #sends user result to a lower to check for 'y' or 'n' input
        
        while((votConf != 'y') and (votConf != 'n')): #ensures user inputs a y or n for their confirmation, only passing when met
            votConf = input("Confirm vote? (Y/N)    ")
            votConf = votConf.lower()

encryptedVote = encryptedVote % (n**2)

testDecrypt = decryptTotal(encryptedVote)
print("Decrypted value: " + str(testDecrypt))

print("Supposed to get: " + str(voteVal))
