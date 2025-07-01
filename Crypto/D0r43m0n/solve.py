def password_to_master_key_bits(password):
    import string
    ALPHABET = string.ascii_letters + string.digits + '~!@#$%^&*'
    mid = len(ALPHABET) // 2

    bits = []
    for c in password:
        if c in ALPHABET[:mid]:
            bits.append('1')
        elif c in ALPHABET[mid:]:
            bits.append('0')
        else:
            raise ValueError(f"Invalid character: {c}")
    
    return ''.join(reversed(bits))  # reverse lại bit order

def bits_to_master_key(bits):
    as_int = int(bits, 2)
    length = (as_int.bit_length() + 7) // 8
    return as_int.to_bytes(length, 'little')

def decrypt_flag(master_key_bytes, encrypted_b64):
    from Crypto.Cipher import AES
    from Crypto.Util.Padding import unpad
    from hashlib import sha256
    from base64 import b64decode

    key = sha256(master_key_bytes).digest()
    cipher = AES.new(key, AES.MODE_ECB)
    ciphertext = b64decode(encrypted_b64)
    plaintext = unpad(cipher.decrypt(ciphertext), 16)
    return plaintext.decode()

# ==========================

with open('output.txt') as f:
    lines = f.readlines()
    password = lines[0].strip().split('Password : ')[1]
    encrypted_flag_b64 = lines[1].strip().split('Encrypted Flag : ')[1]

bitstring = password_to_master_key_bits(password)
master_key = bits_to_master_key(bitstring)
flag = decrypt_flag(master_key, encrypted_flag_b64)

print("FLAG:", flag)
