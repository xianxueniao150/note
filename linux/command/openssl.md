```sh
# 加密
$ openssl enc -aes-256-cbc -salt -in a.txt -out file.enc -pass pass:mypass -p
salt=7AC02D0264B8CAF7
key=9BD8ECD14C43A6B5B11A7FF4F1D8F6C7F09DF43CDD5D4EB40986DF62CCDE27CD
iv =822269E88C09AB5BC3DCBDE06B1E64CD
# 解密
$ openssl enc -d -aes-256-cbc -in file.enc
enter aes-256-cbc decryption password:
aa
bb
...
```

hmac
```cpp
$ openssl dgst -hmac "mykey" a.txt
HMAC-SHA256(a.txt)= 6d18869c269ea7c9f2f5df323de9b93513c3bf990de29cdf3903f057a18cd95c
```

rsa加解密
```sh
# 密钥对生成
# 生成私钥,生成的密钥长度是 2048 比特
$ openssl genrsa -out mykey.pem 2048
# 从密钥对中分离出公钥
$ openssl rsa -in mykey.pem  -pubout -out mypubkey.pem

# 加解密
# -pubin 声明密钥是公钥
$ openssl rsautl -encrypt -pubin -inkey mypubkey.pem -in a.txt -out cipher.txt
$ openssl rsautl -decrypt -inkey mykey.pem -in cipher.txt

hello
```
