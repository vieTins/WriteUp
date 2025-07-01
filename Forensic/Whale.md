# Whale

## Reconnaissance

Đề cho ta một static website, bước đầu tiên ta sẽ recon các thông tin từ website.

### Tìm IP Address

Tìm IP address của website bằng: [IP Location](https://www.iplocation.net/ip-lookup)

**IP Address:** `54.160.131.50`

### Port Scanning

Scan các port mở bằng Nmap:

```bash
nmap -sC -sV -Pn 54.160.131.50
```

**Kết quả:**

```
Starting Nmap 7.95 ( https://nmap.org ) at 2025-06-28 09:30 UTC
Nmap scan report for ec2-54-160-131-50.compute-1.amazonaws.com (54.160.131.50)
Host is up (0.25s latency).
Not shown: 997 filtered tcp ports (no-response)
PORT     STATE SERVICE VERSION
22/tcp   open  ssh     OpenSSH 9.2p1 Debian 2+deb12u6 (protocol 2.0)
| ssh-hostkey:
|   256 be:74:3a:8a:f8:1a:cc:00:f3:61:0f:1d:30:5f:0e:77 (ECDSA)
|_  256 c8:fc:23:8a:7a:37:90:80:de:e6:90:9a:be:33:70:eb (ED25519)
80/tcp   open  http    nginx 1.22.1
|_http-server-header: nginx/1.22.1
|_http-title: Beautiful Web Front-End
5000/tcp open  http    nginx 1.22.1
|_http-title: Welcome to nginx!
|_http-server-header: nginx/1.22.1
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 37.83 seconds
```

**Port Summary:**

| Port     | Service | Version       | Description     |
| -------- | ------- | ------------- | --------------- |
| 22/tcp   | SSH     | OpenSSH 9.2p1 | SSH Access      |
| 80/tcp   | HTTP    | nginx 1.22.1  | Web Server      |
| 5000/tcp | HTTP    | nginx 1.22.1  | Docker Registry |

## Docker Registry Analysis

Theo như name và description của bài thì đây chắc chắn là một bài Docker Forensic. Port 5000 thường được sử dụng cho Docker Registry - Dịch vụ lưu trữ Docker Images.

### Kiểm tra Docker Registry

```bash
curl http://54.160.131.50:5000/v2/
```

**Response:**

```json
{}
```

Endpoint v2 trả về {} → Docker Registry tồn tại!

### Liệt kê Docker Images

```bash
curl http://54.160.131.50:5000/v2/_catalog
```

**Response:**

```json
{ "repositories": ["challenge_docker"] }
```

Repository found: `challenge_docker`

### Kiểm tra Tags

```bash
curl http://54.160.131.50:5000/v2/challenge_docker/tags/list
```

**Response:**

```json
{ "name": "challenge_docker", "tags": ["latest"] }
```

### Pull Docker Image

```bash
docker pull 54.160.131.50:5000/challenge_docker:latest
```

**Verify:**

```bash
docker image ls
```

**Output:**

```
REPOSITORY                            TAG       IMAGE ID       CREATED      SIZE
54.160.131.50:5000/challenge_docker   latest    68a8579032f9   2 days ago   133MB
```

## Docker Image Layer Analysis

Sử dụng tool [dive](https://github.com/wagoodman/dive) để phân tích các layer của Docker image.

Docker Image được xây dựng từ nhiều layer chồng lên nhau:

- **Base layer**: Hệ điều hành như Ubuntu, Alpine, v.v.
- **Additional layers**: Tương ứng với mỗi lệnh trong Dockerfile (RUN, COPY, ADD, ...)

### Export Docker Image

```bash
docker save 54.160.131.50:5000/challenge_docker > chall.tar
```

### Analyze with Dive

```bash
dive docker-archive://chall.tar
```

### Key Finding

**Layer ID:** `ff4d1ba7a60a870c89a22ef55839e9b36fe5dfe373399ddd8ecbecdd1722bb33`

Action: Copy folder `src/` vào folder `/app`

Sau khi unzip và vào folder theo ID Layer, ta phát hiện:

```
.git/  ← Git repository!
```

## Git Recovery

Sử dụng [GitTools](https://github.com/internetwache/GitTools) để recover source code và xem lịch sử commit.

### Flag Extraction

**File 1:**

```bash
cat 3-bae161fb6dfa1753544a1a6f963d619fb9b9e5f5/secret.txt
```

**Output:**

```
The flag is VSL{d0ck3r_4nd_
```

**File 2:**

```bash
cat 8-7c08a227bed06d8e7f1b34474369809f1f11ab02/secret.txt
```

**Output:**

```
g1t_1s_u5efu11}
```

## Flag

```
VSL{d0ck3r_4nd_g1t_1s_u5efu11}
```
