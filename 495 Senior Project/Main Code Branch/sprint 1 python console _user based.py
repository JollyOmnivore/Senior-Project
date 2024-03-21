from random import randrange
from math import pow, gcd, log10
import random

#primesList = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31] #11 stored integers for rand selection

def randNumList(keyVal):
    newList = []
    #print("place checker 1")
    listOfCoprimes = prime_range(2, n)
    #print(listOfCoprimes)
    for i in range(2,n):
        if not i in listOfCoprimes:
            newList.append(i)
            #print(i)
    return newList

def encryptVote(usrVote, randInt, voteVal): #general funcion for step by step encryption technique
    #n = n+1 #1+n in encrypt function
    
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
            else:
                prime_list.append(num)
    #print(num)
    return prime_list 

'''def decryptTotal(total, lam):
    mu = pow(lam, -1, n)
    power_mod = pow(total, lam[, (n**2)])
    result = (power_mod - 1) / n
    result = result * mu
    return (result % n)'''
#dbl chck following 2 lines call correctly============
listOfPrimes = prime_range(400, 800)
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
        voteVal = 10000
    #below if only generates a new r on the first passthrough of the vote
    if passThrough == 0:
        r = random.choice(coprimeList)
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
voteArray = ['~', '~', '~', '~', '~', '~', '~', '~', '~', '~']
for i in range(1,10):
    randVote = random.choice(validVote)
    if randVote == 'a':
        fakeVoteVal = 1
    elif randVote == 'b':
        fakeVoteVal = 100
    else:
        fakeVoteVal = 10000
    voteArray[i] = encryptVote(randVote, random.choice(coprimeList), fakeVoteVal)
    decryptThis += voteArray[i]
    print("Voter " + str(i) + " with vote choice " + str(randVote) + " encrypted vote: " + str(voteArray[i]))
    


print("Number to decrypt: " + str(decryptThis))
    
#decryptTest = decryptVote(decryptTotal, lam)


'''num1 = int(10 ** (candidates /2 * log10(numVoters)))
print("num1:", str(num1))

num2 = int(10 ** (candidates / 2 * log10(numVoters+1)))
print(num2)

l=prime_range(num1, num2)
print(l)
#C: l should return as a list

p=l[randrange(len(l))];
q=l[randrange(len(l))];
while p==q:
    q=l[randrange(len(l))]
n=p*q;
lam=(p-1)*(q-1);
mu=pow(lam,-1, n);
#C: Check that "good" primes are selected.  Always works 
# for primes of same size, but I haven't proven this yet.
#W: Currently errors here, pow doesnt accept negative 1
# for param 2, even though by all acounts it should. Goal
# is to do inverse modulo here. Check if there's a func
# from Muskat for this.
gcd(n,(p-1)*(q-1))'''
