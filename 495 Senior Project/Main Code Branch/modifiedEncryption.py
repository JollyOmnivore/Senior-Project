'''
SMALL SCALE OF PRIMELIST
'''

'''
    N value never changes, only r that changes :D
'''

from random import randrange
from math import pow, gcd, log10
import random
import json
import gmpy2
with open('prime_numbers.json', 'r') as f:
    data = json.load(f)
primesListBig = data['10kPrimeList']
with open('prime_numbers99980001.json', 'r') as k:
    data = json.load(k)
rValsList = data['1MPrimeList']

#primesList = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31] #11 stored integers for rand selection

'''
    define a checker for coprime nums; i.e., check to see if the only factor shared between n and i is 1
'''

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
    
#dbl chck following 2 lines call correctly============
#listOfPrimes = prime_range(1000, 1500)
#print("prime range works")
p = random.choice(primesListBig) # random prime value 1
q = random.choice(primesListBig) # random prime value 2
while (p == q) or (p < 1500) or (q < 1500) or (p > 2500) or (q > 2500): #ensures p and q are not the same
    p = random.choice(primesListBig) # random prime value 1
    q = random.choice(primesListBig)
n = p * q #get prime product
lam = (p-1) * (q-1)
mu = modinv(lam,n)
#print("p: " + str(p))
#print("q: " + str(q))
print("n: " + str(n))
print("lam: " + str(lam))
print("mu: " + str(mu))
#=====================================================

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
    print("r val: " + str(r))
    passThrough = 1
    encryptedVote = encryptVote(r, voteVal, n) #encrypted vote function called here with encryptedVote
    
    if usrVote in validVote: #check for vote being a valid option
        print("You chose:    " + usrVote)
        print("Your encrypted vote:    " + str(encryptedVote))
        
        votConf = input("Confirm vote? (Y/N)    ")
        votConf = votConf.lower() #sends user result to a lower to check for 'y' or 'n' input
        
        while((votConf != 'y') and (votConf != 'n')): #ensures user inputs a y or n for their confirmation, only passing when met
            votConf = input("Confirm vote? (Y/N)    ")
            votConf = votConf.lower()
    testDecrypt = decryptTotal(encryptedVote, lam, n, mu)
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
voteArray[1] = encryptVote(random.choice(rValsList), fakeVoteVal, n)
expectedResult += fakeVoteVal
#decryptThis *= voteArray[i]
voterCount += 1
print("Voter 1 with vote choice " + str(randVote) + " encrypted vote: " + str(voteArray[1]))

#valueTotal = voteArray[0] * voteArray[1]

#print("decrypted test between voter 1 and user vote: " + str(decryptTotal(valueTotal)))

valueTotal2 = voteArray[0] * voteArray[1]
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
    voteArray[g] = encryptVote(random.choice(rValsList), fakeVoteVal, n)
    #valueTotal *= voteArray[g]
    valueTotal2 *= voteArray[g]
    valueTotal2 = valueTotal2 % (n**2)
    expectedResult += fakeVoteVal
    voterCount += 1
    print("Voter " + str(g) + " with vote choice " + str(randVote) + " encrypted vote: " + str(voteArray[int(g)]))

#print("normal product: " + str(valueTotal))
print("mod n squared: " + str(valueTotal2))

actualResult = 0
decryptedTempVal = 0
#print(voteArray)
'''for i in range(0, voterCount):
    #print(str(i) + " is current index ========")
    decryptedTempVal = decryptTotal(voteArray[i])
    #print("decrypted val: " + str(voteArray[i]) + " to vote: " + str(decryptedTempVal))
    actualResult = decryptedTempVal + actualResult'''
#decryptedTempVal = decryptTotal(voteArray[0])
#print("decrypted val: " + str(voteArray[0]) + " to vote: " + str(decryptedTempVal))
#actualResult = decryptedTempVal + actualResult

#print("Number to decrypt: " + str(decryptThis))
#decryptTest = decryptTotal(decryptThis, lam)
print("vote total (product): " + str(valueTotal2))
#print("decrypted val:" + str(decryptTest))
#print("decrypted result: " + str(actualResult))
#print("expected decrypt: " + str(expectedResult))

totalVotesD = 0
totalVotesC = 0
totalVotesB = 0
totalVotesA = 0
totalVotersCounted = 0
actualResult = decryptTotal(valueTotal2, lam, n, mu)
testProductModN2 = actualResult
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

while (actualResult - 1) >= 0:
    #print("vote for A")
    actualResult -= 1
    totalVotesA += 1
    totalVotersCounted +=1

#totalVotesA = 10 - totalVotersCounted

totalNoVotes = 10 - totalVotersCounted #10 is total voters in this simulation

#testProductTally = 0
#testProductTally = decryptTotal(valueTotal)


#print("Decrypted value ====: " + str(testProductTally))
#testProductModN2 = decryptTotal(valueTotal2)
print("Mod n2 value ====: " + str(testProductModN2))
print("Votes for 'A': " + str(totalVotesA))
print("Votes for 'B': " + str(totalVotesB))
print("Votes for 'C': " + str(totalVotesC))
print("Votes for 'D': " + str(totalVotesD))
