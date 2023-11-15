"""
Helper functions required to encrypt or decryt the text
"""

import random

def gen_primes(min, max):
    """
    Generates all prime numbers up to a limit 'n'
    -- Uses Sieve of Erastosthenes algorithm
    """
    n = max
    count = (max-min)/max
    primes = [1] * (n+1)
    primes[0] = primes[1] = 0
    for i in range(2,n+1):
        if primes[i]:
            for j in range(i*i, n+1, i):
                primes[j] = 0
    res = [i for i, prime in enumerate(primes) if prime]
    print(count, len(res))
    return res[int(count*len(res)):]


def gen_rand_prime(min, max):
    prime = random.randint(min, max)
    while not is_prime(prime):
        prime = random.randint(min, max)
    return prime


def is_prime(num):
    if num < 2:
        return False
    for i in range(2, num//2+1):
        if num % i == 0:
            return False
    return True


def extended_gcd(a,b):
    if a == 0:
        return b, 0, 1
    else:
        g, x, y = extended_gcd(b%a, a)
        return g, y-(b//a)*x, x
    

def decryption_key_helper(a, m):
    g, x, _ = extended_gcd(a, m)
    if g != 1:
        raise ValueError("Modular inverse does not exists")
    else:
        return x % m

if __name__ == "__main__":
    print(gen_primes(100000, 500000))