import random
import time


enc = "0x1a2b3c4d5e6f708192a0b1c2d3e4f506172839495a5b6c7d8e9fa0b1c2d3e4f5"

hex_str = hex(enc)[2:]
if len(hex_str) % 2:
    hex_str = '0' + hex_str
enc_bytes = bytes.fromhex(hex_str)
flag_len = len(enc_bytes)

print(f"[*] Length of encrypted flag: {flag_len} bytes")

MAX = 2**32 - 1
now = int(time.time())

# Brute-force quanh thời điểm hiện tại
for seed in range(now - 20, now + 5):  # có thể mở rộng 
    random.seed(seed)
    rand_nums = [random.randint(0, MAX) for _ in range(flag_len)]
    
    recovered = [(enc_bytes[i] - rand_nums[i]) % 256 for i in range(flag_len)]
    try:
        flag = bytes(recovered).decode()
        if flag.startswith("VSL{"):
            print(f"[+] Found FLAG: {flag}")
            break
    except:
        continue
