from random import randrange
import random
import json
import gmpy2
with open('prime_numbers.json', 'r') as f: # import data from prime num json
    data = json.load(f)
primesListBig = data['10kPrimeList']
with open('prime_numbers99980001.json', 'r') as k: # import data from larger prime num json
    data = json.load(k)
rValsList = data['1MPrimeList']

def encryptVote(randInt, voteVal, n): # function to encrypt votes
    if voteVal == 0: # checks for novote
        return 0
    equationPartOne = gmpy2.powmod(n+1, voteVal, n**2)  # (n+1)^voteVal % n^2
    randomToProduct = gmpy2.powmod(randInt, n, n**2)  # r^n % n^2
    fullEquation = gmpy2.mul(equationPartOne, randomToProduct) % (n**2)  # (ep1 * ep2) % n^2
    return fullEquation

def modinv(a, m):
    # Using gmpy2 for computing modular inverse
    return int(gmpy2.invert(a, m))

def powerMod(A, N, M):
    # Using gmpy2 for power mod
    return int(gmpy2.powmod(A, N, M))

# function to decrypt the vote(s)
def decryptTotal(total, lam, n, mu):
    power_mod = powerMod(total, lam, n**2) # total^lam % n^2
    result = (power_mod - 1) // n #prev result - 1 // n
    result = result * mu % n #prev result * mu % n
    return result
    
p = random.choice(primesListBig) # random prime value 1
q = random.choice(primesListBig) # random prime value 2
while (p == q) or (p < 1500) or (q < 1500) or (p > 2500) or (q > 2500): # ensures p and q are not the same
    p = random.choice(primesListBig) # random prime value 1
    q = random.choice(primesListBig) # random prime value 2
n = p * q # get prime product
lam = (p-1) * (q-1) # get val of p-1 * q-1 for later use & security
mu = modinv(lam,n) # get mod inverse of lam and n
#print("p: " + str(p)) # check val p
#print("q: " + str(q)) # check val q
print("n: " + str(n)) # check val n
print("lam: " + str(lam)) # check val lam
print("mu: " + str(mu)) # check val mu

validVote = ['a', 'b', 'c', 'd']	# list of valid input options for user vote
votConf = "n" # boolean between y and n checking for user confirmation of their vote
passThrough = 0
while(votConf != "y"): # checks against user input for confirming vote
    print("Option A: Apple		Option B: Orange") # prints options for voting
    print("Option C: Jerky		Option D: Abstain")
    usrVote = input("Please select your vote: A, B, C, D:     ")
    usrVote = usrVote.lower() # forces user vote to lower
    # below if-elif-elif-else keys voteVal to what user chose as an option.
    if usrVote == 'a':
        voteVal = 1
    elif usrVote == 'b':
        voteVal = 100
    elif usrVote == 'c':
        voteVal = 10000
    else:
        voteVal = 1000000
    # r val generated with each time user chooses a vote to ensure their encrypt vote is random
    r = random.choice(rValsList)
    print("r val: " + str(r))
    passThrough = 1
    # encrypted vote function called here with encryptedVote
    encryptedVote = encryptVote(r, voteVal, n) 
    
    if usrVote in validVote: #check for vote being a valid option
        print("You chose:    " + usrVote)
        print("Your encrypted vote:    " + str(encryptedVote))
        
        votConf = input("Confirm vote? (Y/N)    ")
        votConf = votConf.lower() # sends user result to a lower to check for 'y' or 'n' input
        
        while((votConf != 'y') and (votConf != 'n')): # ensures user inputs a y or n for their confirmation, only passing when met
            votConf = input("Confirm vote? (Y/N)    ")
            votConf = votConf.lower()
    testDecrypt = decryptTotal(encryptedVote, lam, n, mu)
    # displays user decrypted value to show correct tally
    print("Decrypted value: " + str(testDecrypt))

# expected results stored as summation of vote values (1, 100, 10000, 1000000)
expectedResult = voteVal
voteArray = ['~', '~', '~', '~', '~', '~', '~', '~', '~', '~'] # arr to store all votes (sim of DB)
voteArray[0] = encryptedVote # stores user's vote in the 'database'
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
voteArray[1] = encryptVote(random.choice(rValsList), fakeVoteVal, n) # fake voter 1 choice stored
expectedResult += fakeVoteVal # tally of expected results
voterCount += 1 # total voters counted
print("Voter 1 with vote choice " + str(randVote) + " encrypted vote: " + str(voteArray[1]))

valueTotal2 = voteArray[0] * voteArray[1] # product of encrypted votes stored
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
    valueTotal2 *= voteArray[g]
    valueTotal2 = valueTotal2 % (n**2) # multiplies vote product and mods by 2 for storage of smaller size w/ same result
    expectedResult += fakeVoteVal # tallies simulated votes to check against
    voterCount += 1 # increases voter count w/ total voters
    print("Voter " + str(g) + " with vote choice " + str(randVote) + " encrypted vote: " + str(voteArray[int(g)]))

actualResult = 0
decryptedTempVal = 0

print("vote total (product): " + str(valueTotal2))

totalVotesD = 0
totalVotesC = 0
totalVotesB = 0
totalVotesA = 0
totalVotersCounted = 0
actualResult = decryptTotal(valueTotal2, lam, n, mu) # decrypt of encrypted votes product to generate vote tally
testProductModN2 = actualResult # stores total into a temp val to not modify one value and modify the other
print("=== expected result === " + str(expectedResult))
print("actual total: " + str(actualResult))
# checks for total amount of 'D' vals
while (actualResult - 1000000) >= 0:
    #print("vote for D")
    actualResult -= 1000000
    totalVotesD += 1
    totalVotersCounted += 1

# checks for total amount of 'C' vals
while (actualResult - 10000) >= 0:
    #print("vote for C")
    actualResult -= 10000
    totalVotesC += 1
    totalVotersCounted += 1
        
# checks for total amount of 'B' vals
while (actualResult - 100) >= 0:
    #print("vote for B")
    actualResult -= 100
    totalVotesB += 1
    totalVotersCounted += 1

# checks for total amount of 'A' vals
while (actualResult - 1) >= 0:
    #print("vote for A")
    actualResult -= 1
    totalVotesA += 1
    totalVotersCounted +=1

totalNoVotes = 10 - totalVotersCounted #10 is total voters in this simulation

# display results in readable format
print("Mod n2 value ====: " + str(testProductModN2))
print("Votes for 'A': " + str(totalVotesA))
print("Votes for 'B': " + str(totalVotesB))
print("Votes for 'C': " + str(totalVotesC))
print("Votes for 'D': " + str(totalVotesD))
