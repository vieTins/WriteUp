# PhantomHook

## Phân tích Memory Dump

Đề cho một file memory, nên ta sẽ dùng Volatility3 để giải.

```bash
file memory.dmp
```

**Output:**

```
memory.dmp: MS Windows 64bit crash dump, version 15.19041, 4 processors, DumpType (0x1), 1048576 pages
```

## Liệt kê các Process

Đầu tiên ta sẽ liệt kê các process đang hoạt động trong hệ thống Windows tại thời điểm dump bộ nhớ được tạo.

```bash
python3 vol.py -f memory.dmp windows.pslist
```

Một process có tên là `Mal_stealer.exe` đang chạy, theo như tên file thì đây có lẽ là một malware stealer chuyên đánh cắp thông tin người dùng và gửi về C2 server.

## Tìm file Malware

```bash
python3 vol.py -f memory.dmp windows.filescan | grep "Mal_stealer"
```

**Output:**

```
0xb78895051480.0\Users\phat1\Desktop\Release\Mal_stealer.application
0xb78896c99e50  \Users\phat1\Desktop\Release\Release\Mal_stealer.exe
0xb78896cc23a0  \Users\phat1\Desktop\Release\Release\app.publish\Mal_stealer.exe
0xb78896dc3980  \Users\phat1\AppData\Local\Microsoft\CLR_v4.0_32\UsageLogs\Mal_stealer.exe.log
0xb78896e857c0  \Users\phat1\Desktop\Release\Release\Mal_stealer.exe
```

## Dump file Malware

```bash
python3 vol.py -f memory.dmp -o ~/Desktop/dump windows.dumpfiles --virtaddr 0xb78896e857c0
```

## Reverse Engineering

Sử dụng DIE để phân tích file `Mal_stealer.exe`, ta thấy đây là file .NET, viết bằng C#, ta có thể dùng dnSpy để reverse code.

Đây là một malware stealer được viết bằng C#, có một số functions như sau:

- Lấy cắp History Browser, Cookies, Password của User
- Lấy thông tin Hardware
- Truy cập file cấu hình của các ứng dụng VPN, lấy Credential
- Gửi thông tin đánh cắp được về Server C2 - ở đây là WebHook

## Dump Process Memory

Ta sẽ tìm lại thông tin mà malware này đã đánh cắp bằng cách dump process `Mal_stealer.exe`.

```bash
python3 vol.py -f memory.dmp -o ~/Desktop/dump windows.memmap --dump --pid 8576
```

Ta sẽ tìm link WebHook mà Malware đã sử dụng để gửi thông tin đánh cắp bằng grep.

Truy cập WebHook ta sẽ nhận được FLAG.

## Flag

```
VSL{7h3_l457_l364cy}
```
