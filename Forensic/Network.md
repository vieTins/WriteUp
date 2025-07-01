# Network

## Phân tích file PCAP

Đề bài cho một file .pcap, filter với protocol HTTP.

Theo như traffic thì IP `192.168.56.105` download hai file là `flag.zip` và `secret.txt` về máy. Tiến hành Export File để tiếp tục phân tích.

## Phân tích file secret.txt

```bash
cat secret.txt
```

**Output:**

```
The password is a day chosen for creating the VSL Club. Day format: dd/mm/yyyy
```

Theo như nội dung của file secret thì password của file zip chứa flag sẽ là ngày thành lập VSL CLUB, tuy nhiên mình có search Google thì nó sai. Đành brute force password theo day format ban tổ chức đã cho.

## Brute force password

```python
import os
import subprocess

def test_password(day, month, year):
    password = f"{day:02d}/{month:02d}/{year}"
    print(f"Trying: {password}")
    result = subprocess.run(
        ['7z', 't', '-p' + password, 'flag.zip'],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    if b'Everything is Ok' in result.stdout:
        print(f"[+] Correct password: {password}")
        return True
    return False

for month in range(1, 13):
    max_day = 31
    if month in [4, 6, 9, 11]: max_day = 30
    if month == 2: max_day = 28
    for day in range(1, max_day + 1):
        if test_password(day, month, 2023):
            exit(0)

print("[-] No password matched.")
```

**Kết quả:**

```
[+] Correct password: 11/11/2023
```

## Flag

```
VSL{84eddc6148bcb0b8381e39c971919e5fb520f79cd48ecd4a12852832576b3a3d}
```
