"""
SecureEncryptionAlgorithm
--------------------
This module contains classes that can encrypt the given data and
return the cipher text, and public keys.
"""

from utils import gen_rand_prime, decryption_key_helper
from random import randint, shuffle, seed
from math import gcd
from time import time, localtime
from pickle import dump, load


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
    seed(e)
    key = randint(3,23)
    print("key:",key)
    # encoded = [ord(ch)+key if ord(ch)<key else (ord(ch)-key)*-1 for ch in msg]
    encoded = [ord(ch)+key for ch in msg]
    seed(len(encoded))
    shuffle(encoded)
    seed(e)
    bkey = randint(100000000000, 500000000000)
    print("bkey:", bkey)
    cipher = [pow(c, e, n)+bkey for c in encoded]    
    print("P ->",p)
    print("Q ->",q)
    return phi_n, e, n, cipher

def encrypt_file(file_name, msg):
    phi_n, e, n, cipher = encrypt_message(msg)
    with open(file_name, "wb") as f:
        dump({"e": e, "n": n, "phi_n": phi_n, "msg":cipher}, f)
    return cipher

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

def decrypt_file(file_name):
    with open(file_name, "rb") as f:
        cipher_obj = load(f)
    msg = decrypt_message(cipher_obj["msg"],cipher_obj["e"],cipher_obj["n"],cipher_obj["phi_n"])
    with open("decrypted_"+file_name, "w") as f:
        f.write(msg)
    return msg

def decrypt_message(cipher, e, n, phi_n):
     """
     Decrypts Message
     ----------------
     Gets cipher text, e, n phi_n.\n
     Returns the message.
     """
     d = gen_decrypt_key(e, phi_n)
     seed(e)
     bkey = randint(100000000000, 500000000000)
     print("dbkey:", bkey)
    #  print("Test 0 element:", pow(cipher[0], d, n), pow(cipher[0]-bkey, d, n))
    #  print("Test -1 element:", pow(cipher[-1], d, n), (pow(-cipher[-1]-bkey, d, n))*-1)
    #  encoded = [pow(ch-bkey, d, n)  if ch>=0 else -(pow(-ch-bkey, d, n)) for ch in cipher]
     encoded = [pow(ch-bkey, d, n) for ch in cipher]
     seed(len(encoded))
     enc_ind = list(range(len(encoded)))
     shuffle(enc_ind)
     sort_ind = zip(enc_ind, encoded)
     encoded = [i[1] for i in sorted(sort_ind, key=lambda x: x[0])]
     seed(e)
     key = randint(3,23)
     print("dkey:",key)
    #  print("Test 0 element:", encoded[0], encoded[0]-key)
    #  print("Test -1 element:", chr(encoded[0]), chr(encoded[0]-key))
    #  msg = "".join(chr(ch-key) if ch>=0 else chr(-ch-key) for ch in encoded)
     
     msg = "".join(chr(ch-key) for ch in encoded)
     return msg


if __name__ == "__main__":
    inp = input("Encrypt (e) or Decrypt (d) >> ")
    if inp.lower()=="e":
        with open("inputfile.txt","r") as f:
            cont = f.read()
        st = time()
        # cont = "Hello CIT."
        t=localtime()
        file_name = str(t.tm_yday)+"_"+str(t.tm_hour)+str(t.tm_min)+str(t.tm_sec)+".sea"
        cipher = encrypt_file(file_name, cont)
        # phi_n, e, n, cipher = encrypt_message(cont)
        ed = time()
        print("----------------","Encrypted Message","----------------",cipher,sep="\n")
        print("-----------------------")
        print("Time Taken For Encryption:",ed-st,"secs")
        print("Time per 1000 chars:", ((ed-st)/len(cont))*1000)
        print("-----------------------")
    elif inp.lower()=="d":
        file_name = input("Enter full file path: ")
        st = time()
        msg = decrypt_file(file_name)
        ed = time()
        print("----------------","Decrypted Message","----------------",msg, sep="\n")
        print("-----------------------")
        print("Time Taken For Decryption:",ed-st,"secs")
        print("Time per 1000 chars:", ((ed-st)/len(msg))*1000)
        print("-----------------------")
    else:
        print("Invalid input!, Try again!!")
    # print("Enc Key:", e)
    # print("Dec Key:", d)
    # print("phi:", phi_n)
    # print("n:", n)
    # print("Integrity:", "Perfect" if cont==msg else "Mismatch")
    # print("Number of characters:", len(cont))

# if __name__ == "__main__":
#     with open("inputfile.txt","r") as f:
#         cont = f.read()
#     st = time()
#     # cont = "Hello CIT."
#     phi_n, e, n, cipher = encrypt_message(cont)
#     # phi_n, e, n, cipher = encrypt_message(cont)
#     ed = time()
#     print("----------------","Encrypted Message","----------------",cipher,sep="\n")
#     print("-----------------------")
#     print("Time Taken For Encryption:",ed-st,"secs")
#     print("Time per 1000 chars:", ((ed-st)/len(cont))*1000)
#     print("-----------------------")
#     st = time()
#     msg = decrypt_message(cipher, e, n, phi_n)
#     ed = time()
#     print("----------------","Decrypted Message","----------------",msg, sep="\n")
#     print("-----------------------")
#     print("Time Taken For Decryption:",ed-st,"secs")
#     print("Time per 1000 chars:", ((ed-st)/len(cont))*1000)
#     print("-----------------------")
#     print("Enc Key:", e)
#     print("Dec Key:", d)
#     print("phi:", phi_n)
#     print("n:", n)
#     print("Integrity:", "Perfect" if cont==msg else "Mismatch")
#     print("Number of characters:", len(cont))