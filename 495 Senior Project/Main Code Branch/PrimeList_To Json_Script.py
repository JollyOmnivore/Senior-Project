import json

def prime_range(lower, upper):
    prime_list = [] 
    for num in range(lower, upper + 1):
        if num > 1:
            for i in range(2, num):
                if (num % i) == 0:
                    break
            else:
                prime_list.append(num)
    return prime_list 

primelist = prime_range(0, 10000)

x = {
    "10kPrimeList": primelist
}

y = json.dumps(x)
print(y)


with open('prime_numbers.json', 'w') as file:
    json.dump(x, file)  

print("JSON data has been saved to prime_numbers.json")