# Homomorphic Encryption Math
#Original Concept and Mathematics: Jeremy Muskat, Ph.D.
#Written By: Joseph (Joe) Vennard, with support from William (Willow) Keenan-Harte
#Addapted to Server By: William (Willow) Keenan-Harte

'''
    N value never changes, only r that changes :D
'''

from random import randrange
from math import pow, gcd, log10
import random

# primesList = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31] #11 stored integers for rand selection

'''
    define a checker for coprime nums; i.e., check to see if the only factor shared between n and i is 1
'''


def randNumList(keyVal):
    newList = []
    # print("place checker 1")

    # print(listOfCoprimes)
    for i in range(2, keyVal):
        if i != p and i != q:
            newList.append(i)
            # print("appended " + str(i))
    return newList


def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    g, y, x = egcd(b % a, a)
    return (g, x - (b // a) * y, y)


def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('No modular inverse')
    return x % m


def encryptVote(usrVote, randInt, voteVal):  # general funcion for step by step encryption technique
    # n = n+1 #1+n in encrypt function
    if voteVal == 0:
        return 0
    equationPartOne = (n + 1) ** voteVal  # result of 1+n to the power of voteVal
    # listOfCoprimes = prime_range(2, n) # creation of random number r for encrypting
    # r = random.choice(listOfCoprimes) #random variable in the list of numbers coprime to the product of prime1 and prime2
    randomToProduct = randInt ** n  # r to the power of n
    fullEquation = equationPartOne * randomToProduct  # the main equation ((n+1)**m ) * (r ** n)
    nSquare = n ** 2
    result = fullEquation % nSquare  # final step in the equation, taking modulo of t (above) with square of n
    return result  # function encryptVote returns the result of above equations so as to show the user what their vote is, changing each time


# keep n the same, only change r

def prime_range(lower, upper):
    prime_list = []
    for num in range(lower, upper + 1):
        if num > 1:
            for i in range(2, num):
                if (num % i) == 0:
                    break
            else:  # I don't know why this works, i don't like that this works, but it works and we don't touch this ever
                prime_list.append(num)
    # print(num)
    return prime_list


retval = 0


def powerMod(A, N, M):
    '''print("a: " + str(A))
    print("n: " + str(N))
    print("m: " + str(M))'''
    print(A)
    print(N)

    retval = A ** N
    # print("retval: " + str(retval))
    # print("pow func: " + str(pow(A, N, M)))
    return (retval % M)


'''
    FOUND MOD_INVERSE DOCUMENTATION ON geeksforgeeks, DIRECTLY CORRELATES TO SAGEMATH INVERSE_MOD
'''
def modInverse(A, M):
    for X in range(1, M):
        if (((A % M) * (X % M)) % M == 1):
            return X
    return -1


def decryptTotal(total):
    power_mod = powerMod(total, lam, (n ** 2))
    print("power mod val: " + str(power_mod))
    result = int((power_mod - 1) / n)
    print("result val 1:" + str(result))
    result = result * mu
    print("result val 2:" + str(result))
    checkVal = result % n
    if checkVal == 1:
        return 1
    elif checkVal == 100:
        return 100
    # elif checkVal == 662:
    #    return 10000
    else:
        return checkVal
