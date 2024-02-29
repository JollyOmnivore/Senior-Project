#votemath V.1
# Started 2/21/24
# Willow, Joe, and Carter
# Math provided by Jeremy Muskat

# Easily adjust number of candidates and number of voters.  Best to use 99 as opposed to 100.
candidates=4;
numVoters=99;
l=prime_range(10^(candidates/2*log(numVoters,10)), 10^(candidates/2*log(numVoters,10)+1));
p=l[randrange(len(l))];
q=l[randrange(len(l))];
while p==q:
    q=l[randrange(len(l))]
n=p*q;
lam=(p-1)*(q-1);
mu=inverse_mod(lam,n);
# Check that "good" primes are selected.  Always works for primes of same size, but I haven't proven this yet.
gcd(n,(p-1)*(q-1))

# Shares distributed to candidates for threshold decryption
pow=vector([x^i for i in range(candidates)])
l=[randrange(n) for i in range(candidates-1)]
l.insert(0,p)
coeff=vector(l)
Share(x)=pow.dot_product(coeff)
[(i,Share(i)) for i in range(1,candidates+1)]

# Believe that your vote counts
def messVote(x):
    if x==0:
            return(0)
    if x==1:
            return(1)
    if x==2:
            return(10^2)
    if x==3:
            return(10^4)
    else:
            return(10^6)
def encVote(x):
    return ((n+1)^messVote(x) * power_mod(randrange(n),n,n^2)) % n^2
def decVote(x):
    return mod(((power_mod(x,lam,n^2)-1)/n) * mu, n)
def intVote(x):
    if decVote(x)==0:
            return(0)
    if decVote(x)==1:
            return(1)
    if decVote(x)==10^2:
            return(2)
    if decVote(x)==10^4:
            return(3)
    else:
            return(4)

votesSamp1=[randrange(5) for i in range(10)]
print(votesSamp1)
encVotesSamp1=[encVote(votesSamp1[i]) for i in range(len(votesSamp1))]
print(encVotesSamp1)
print([decVote(encVotesSamp1[i]) for i in range(len(votesSamp1))])
[gcd(encVotesSamp1[i],n^2) for i in range(len(votesSamp1))]
mod(product(encVotesSamp1),n^2)
decVote(product(encVotesSamp1))

# Public Bulletin. Column 1 is the Voter and Column 2 is their encrypted vote
BulletinVote=[encVote(randrange(5)) for i in range(numVoters-1)]
BulletinVote.insert(0,encVotes[0])
#BulletinVote.insert(0,"Encrypted Vote")
BulletinCandidate=[i for i in range(1,numVoters+1)]
#BulletinCandidate.insert(0,"Candidate")
A=matrix([BulletinCandidate,BulletinVote])
print(A.transpose())

# Tally
encTally=product(BulletinVote) % n^2
print(encTally)

# Decrypt the tally
decVote(encTally)

# Check
[[intVote(BulletinVote[i]) for i in range(numVoters)].count(j) for j in range(5)]

