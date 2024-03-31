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

def encryptVote(usrVote, randInt, voteVal): #general funcion for step by step encryption technique
    #n = n+1 #1+n in encrypt function
    if voteVal == 0:
        return 0
    equationPartOne = (n+1) ** voteVal     # result of 1+n to the power of voteVal
    #listOfCoprimes = prime_range(2, n) # creation of random number r for encrypting
    #r = random.choice(listOfCoprimes) #random variable in the list of numbers coprime to the product of prime1 and prime2
    randomToProduct = randInt ** n 	#r to the power of n
    fullEquation = equationPartOne * randomToProduct	# the main equation ((n+1)**m ) * (r ** n)
    nSquare = n ** 2
    result = fullEquation % nSquare #final step in the equation, taking modulo of t (above) with square of n
    return result #function encryptVote returns the result of above equations so as to show the user what their vote is, changing each time

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

def powerMod(A, N, M): 
    print("a: " + str(A))
    print("n: " + str(N))
    print("m: " + str(M))
    retval = A ** N
    print("retval: " + str(retval))
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

def decryptTotal(total, LAM):
    mu = modInverse(LAM,n)
    print("mu val: " + str(mu))
    power_mod = powerMod(total, LAM, (n**2))
    print("power mod val: " + str(power_mod))
    result = int((power_mod - 1) / n)
    print("result val 1:" + str(result))
    result = result * mu
    print("result val 2:" + str(result))
    return (result % n)
    
#dbl chck following 2 lines call correctly============
listOfPrimes = prime_range(2, 25)
print("prime range works")
p = random.choice(listOfPrimes) # random prime value 1
q = random.choice(listOfPrimes) # random prime value 2
while p == q: #ensures p and q are not the same
    q = random.choice(listOfPrimes)
n = p * q #get prime product
lam = (p-1) * (q-1)
print("p: " + str(p))
print("q: " + str(q))
print("n: " + str(n))
print("lam: " + str(lam))
#=====================================================
coprimeList = randNumList(n)
validVote = ['a', 'b', 'c']	# list of valid input options for user vote
votConf = "n" #boolean between y and n checking for user confirmation of their vote
passThrough = 0
while(votConf != "y"):
    print("Option A: Apple		Option B: Orange") #prints options for voting; option A for apple, B for orange, C for abstain/novote
    print("         Option C: Abstain")
    usrVote = input("Please select your vote: A, B, C:     ")
    usrVote = usrVote.lower() #forces user vote to lower
    #below if-elif-else keys voteVal to what user chose as an option.
    if usrVote == 'a':
        voteVal = 1
    elif usrVote == 'b':
        voteVal = 100
    else:
        voteVal = 0
    #below if only generates a new r on the first passthrough of the vote
    #if passThrough == 0:
    r = random.choice(coprimeList)
    print("r val: " + str(r))
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

decryptThis = encryptedVote
expectedResult = voteVal
voteArray = ['~', '~', '~', '~']#, '~', '~', '~', '~', '~', '~'
for i in range(1,4):
    randVote = random.choice(validVote)
    if randVote == 'a':
        fakeVoteVal = 1
    elif randVote == 'b':
        fakeVoteVal = 100
    else:
        fakeVoteVal = 10
    voteArray[i] = encryptVote(randVote, random.choice(coprimeList), fakeVoteVal)
    expectedResult += fakeVoteVal
    decryptThis *= voteArray[i]
    print("Voter " + str(i) + " with vote choice " + str(randVote) + " encrypted vote: " + str(voteArray[i]))
    


print("Number to decrypt: " + str(decryptThis))
    
decryptTest = decryptTotal(decryptThis, lam)

print("decrypted val:" + str(decryptTest))
print("expected decrypt: " + str(expectedResult))
