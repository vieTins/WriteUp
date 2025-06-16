from pwn import *
from hashlib import sha256

context.log_level = 'error'  # Ẩn thông tin thừa

HOST = '61.14.233.78'
PORT = 9000

def get_hash(message):
    io = remote(HOST, PORT)

    io.recvuntil(b"$ ")  # menu
    io.sendline(b"1")  # chọn "Sign Your Message"
    io.recvuntil(b"$ ")
    io.sendline(message)

    response = io.recvline_contains(b"=> Hash:")
    hash_hex = response.decode().strip().split(":")[1].strip()
    io.close()
    return bytes.fromhex(hash_hex)

def recover_flag_byte(position, known_flag_bytes):
    message = b"A" * (position + 1)
    hash_observed = get_hash(message)

    for guess in range(256):
        flag_guess = known_flag_bytes + bytes([guess])
        xored = bytes([m ^ f for m, f in zip(message, flag_guess)])
        trial_hash = sha256(xored).digest()

        if trial_hash == hash_observed:
            print(f"[+] FLAG[{position}] = {guess} ({chr(guess)})")
            return guess
    return None

def main():
    recovered_flag = b""
    max_flag_length = 44  # đoán dài tối đa

    for i in range(max_flag_length):
        byte = recover_flag_byte(i, recovered_flag)
        if byte is None:
            break
        recovered_flag += bytes([byte])

        # Nếu kết thúc bằng '}' thì flag xong
        if recovered_flag.endswith(b"}"):
            break

    print("\n[!] Recovered FLAG:", recovered_flag.decode())

if __name__ == "__main__":
    main()
