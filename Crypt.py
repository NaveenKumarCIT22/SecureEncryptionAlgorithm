"""
Encryption
--------------------
This module contains classes that can encrypt the given data and
return the cipher text, and public keys.
"""

from utils import gen_rand_prime, decryption_key_helper
from random import randint, choice
from math import gcd


def gen_encrypt_key(min, max):
    """
    Generates the RSA Encryption Key
    ---------
    Gets the min and max range for prime numbers as input.\n
    Returns p, q, n, phi_n, e as a tuple of integers.
    """
    p, q = gen_rand_prime(min,max), gen_rand_prime(min,max)
    while p == q:
        q = gen_rand_prime(min, max)
    n = p*q
    phi_n = (p-1)*(q-1)
    e = randint(3, phi_n-1)
    while  gcd(e, phi_n) != 1:
        e = randint(3, phi_n-1)
    return (p, q, n, phi_n, e)


def encrypt_message(msg):
    """
    Encrypts the message
    --------------------
    Gets the message.\n
    Returns the phi_n, e, n, cipher text.
    """
    p, q, n, phi_n, e = gen_encrypt_key(1000000, 9000000)  # 293,239; 
    # n = 10832879
    # phi_n = 10826280
    # e = 10796569
    encoded = [ord(ch) for ch in msg]
    cipher = [pow(c, e, n) for c in encoded]
    print("P ->",p)
    print("Q ->",q)
    return phi_n, e, n, cipher


d = 0

def gen_decrypt_key(e, phi):
    # d = 3
    # while (d*e)%phi != 1 and d < phi:
    #     d += 1
    #     print(d,".",end="",sep="-")
    # if (d*e)%phi != 1:
    #     raise ValueError("Invalid Inputs -> Decryption key can't be generated.")
    # else:
    #     return d
    # k = randint(2,9)
    # target = phi*k+1
    global d
    d = decryption_key_helper(e,phi)
    return d



def decrypt_message(cipher, e, n, phi_n):
     """
     Decrypts Message
     ----------------
     Gets cipher text, e, n phi_n.\n
     Returns the message.
     """
     d = gen_decrypt_key(e, phi_n)
     encoded = [pow(ch, d, n) for ch in cipher]
     msg = "".join(chr(ch) for ch in encoded)
     return msg


if __name__ == "__main__":
    phi_n, e, n, cipher = encrypt_message("Hello CIT")
    print("Encrypted Message","----------------",cipher,sep="\n")
    msg = decrypt_message(cipher, e, n, phi_n)
    print("Decrypted Message","----------------",msg, sep="\n")
    print("-----------------------")
    print("Enc Key:", e)
    print("Dec Key:", d)
    print("phi:", phi_n)
    print("n:", n)