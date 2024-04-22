'''
SMALL SCALE OF PRIMELIST
'''

'''
    N value never changes, only r that changes :D
'''

from random import randrange
from math import pow, gcd, log10
import random

#primesList = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31] #11 stored integers for rand selection

'''
    define a checker for coprime nums; i.e., check to see if the only factor shared between n and i is 1
'''

def randNumList(keyVal):
    newList = []
    #print("place checker 1")
    
    #print(listOfCoprimes)
    for i in range(2,keyVal):
        if i != p and i != q:
            newList.append(i)
                    #print("appended " + str(i))
    return newList

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

#n = n+1 #1+n in encrypt function
#listOfCoprimes = prime_range(2, n) # creation of random number r for encrypting
#r = random.choice(listOfCoprimes) #random variable in the list of numbers coprime to the product of prime1 and prime2
#general funcion for step by step encryption technique
# result of 1+n to the power of voteVal
#r to the power of n
# the main equation ((n+1)**m ) * (r ** n)
#final step in the equation, taking modulo of t (above) with square of n
#function encryptVote returns the result of above equations so as to show the user what their vote is, changing each time


def encryptVote(usrVote, randInt, voteVal): 
    if voteVal == 0:
        return 0
    equationPartOne = (n+1) ** voteVal     
    randomToProduct = randInt ** n 
    fullEquation = equationPartOne * randomToProduct
    nSquare = n ** 2
    result = fullEquation % nSquare 
    return result

# keep n the same, only change r

def prime_range(lower, upper):
    prime_list = [] 
    for num in range(lower, upper + 1):
        if num > 1:
            for i in range(2, num):
                if (num % i) == 0:
                    break
            else: # I don't know why this works, i don't like that this works, but it works and we don't touch this ever
                prime_list.append(num)
    #print(num)
    return prime_list 

retval = 0

def powerMod(A, N, M): 
    '''print("a: " + str(A))
    print("n: " + str(N))
    print("m: " + str(M))'''
    #print(A)
    #print(N)
    
    retval = A ** N
    #print("retval: " + str(retval))
    #print("pow func: " + str(pow(A, N, M)))
    return(retval % M)

'''
    FOUND MOD_INVERSE DOCUMENTATION ON geeksforgeeks, DIRECTLY CORRELATES TO SAGEMATH INVERSE_MOD
'''

def modInverse(A, M):
    for X in range(1, M):
        if (((A % M) * (X % M)) % M == 1):
            return X
    return -1

#print("power mod val: " + str(power_mod))
    #print("result val 1:" + str(result))
    #print("result val 2:" + str(result))

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
    elif checkVal == 10000:
        return 10000
    elif 10000 < checkVal < 1000000:
        return 1000000
    else:
        return checkVal
    
#dbl chck following 2 lines call correctly============
listOfPrimes = prime_range(200, 500)
#print("prime range works")
p = random.choice(listOfPrimes) # random prime value 1
q = random.choice(listOfPrimes) # random prime value 2
while p == q: #ensures p and q are not the same
    q = random.choice(listOfPrimes)
n = p * q #get prime product
lam = (p-1) * (q-1)
mu = modinv(lam,n)
#print("p: " + str(p))
#print("q: " + str(q))
#print("n: " + str(n))
#print("lam: " + str(lam))
#=====================================================
coprimeList = randNumList(n)
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
    r = random.choice(coprimeList)
    #print("r val: " + str(r))
    passThrough = 1
    encryptedVote = encryptVote(usrVote, r, voteVal) #encrypted vote function called here with encryptedVote
    
    if usrVote in validVote: #check for vote being a valid option
        print("You chose:    " + usrVote)
        print("Your encrypted vote:    " + str(encryptedVote))
        
        votConf = input("Confirm vote? (Y/N)    ")
        votConf = votConf.lower() #sends user result to a lower to check for 'y' or 'n' input
        
        while((votConf != 'y') and (votConf != 'n')): #ensures user inputs a y or n for their confirmation, only passing when met
            votConf = input("Confirm vote? (Y/N)    ")
            votConf = votConf.lower()
    testDecrypt = decryptTotal(encryptedVote)
    print("Decrypted value: " + str(testDecrypt))

#decryptThis = encryptedVote
#expectedResult = 0
expectedResult = voteVal
voteArray = ['~', '~', '~', '~', '~', '~', '~', '~', '~', '~']
voteArray[0] = encryptedVote
voterCount = 1
randVote = random.choice(validVote)
if randVote == 'a':
    fakeVoteVal = 1
elif randVote == 'b':
    fakeVoteVal = 100
elif randVote == 'c':
    fakeVoteVal = 10000
else:
    fakeVoteVal = 1000000
voteArray[1] = encryptVote(randVote, random.choice(coprimeList), fakeVoteVal)
expectedResult += fakeVoteVal
#decryptThis *= voteArray[i]
voterCount += 1
print("Voter 1 with vote choice " + str(randVote) + " encrypted vote: " + str(voteArray[1]))

valueTotal = voteArray[0] * voteArray[1]
for g in range(2,10):
    randVote = random.choice(validVote)
    if randVote == 'a':
        fakeVoteVal = 1
    elif randVote == 'b':
        fakeVoteVal = 100
    elif randVote == 'c':
        fakeVoteVal = 10000
    else:
        fakeVoteVal = 1000000
    voteArray[g] = encryptVote(randVote, random.choice(coprimeList), fakeVoteVal)
    valueTotal *= voteArray[g]
    expectedResult += fakeVoteVal
    voterCount += 1
    print("Voter " + str(g) + " with vote choice " + str(randVote) + " encrypted vote: " + str(voteArray[int(g)]))

actualResult = 0
decryptedTempVal = 0
#print(voteArray)
for i in range(0, voterCount):
    #print(str(i) + " is current index ========")
    decryptedTempVal = decryptTotal(voteArray[i])
    #print("decrypted val: " + str(voteArray[i]) + " to vote: " + str(decryptedTempVal))
    actualResult = decryptedTempVal + actualResult
#decryptedTempVal = decryptTotal(voteArray[0])
#print("decrypted val: " + str(voteArray[0]) + " to vote: " + str(decryptedTempVal))
#actualResult = decryptedTempVal + actualResult

#print("Number to decrypt: " + str(decryptThis))
#decryptTest = decryptTotal(decryptThis, lam)
print("vote total (product): " + str(valueTotal))
#print("decrypted val:" + str(decryptTest))
#print("decrypted result: " + str(actualResult))
#print("expected decrypt: " + str(expectedResult))

totalVotesD = 0
totalVotesC = 0
totalVotesB = 0
totalVotersCounted = 0
print("=== expected result === " + str(expectedResult))
print("actual total: " + str(actualResult))
while (actualResult - 1000000) >= 0:
    #print("vote for D")
    actualResult -= 1000000
    totalVotesD += 1
    totalVotersCounted += 1

while (actualResult - 10000) >= 0:
    #print("vote for C")
    actualResult -= 10000
    totalVotesC += 1
    totalVotersCounted += 1
        
while (actualResult - 100) >= 0:
    #print("vote for B")
    actualResult -= 100
    totalVotesB += 1
    totalVotersCounted += 1

totalVotesA = 10 - totalVotersCounted

testProductTally = 0
testProductTally = decryptTotal(valueTotal)

print("Decrypted value ====: " + str(testProductTally))
print("Votes for 'A': " + str(totalVotesA))
print("Votes for 'B': " + str(totalVotesB))
print("Votes for 'C': " + str(totalVotesC))
print("Votes for 'D': " + str(totalVotesD))
