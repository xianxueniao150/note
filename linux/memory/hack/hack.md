https://blog.holbertonschool.com/hack-the-virtual-memory-c-strings-proc/

DESCRIPTION
       The  strdup()  function returns a pointer to a new string which is a duplicate of the string s.
       Memory for the new string is obtained with malloc(3), and can be freed with free(3).
	   
Based on what we said earlier about virtual memory, where do you think the duplicate string will be located? At a high or low memory address?
Probably in the lower addresses (in the heap). Let’s compile and run our small C program to test our hypothesis:

```
julien@holberton:~/holberton/w/hackthevm0$ gcc -Wall -Wextra -pedantic -Werror main.c -o holberton
julien@holberton:~/holberton/w/hackthevm0$ ./holberton 
0x1822010
```
Our duplicated string is located at the address 0x1822010. Great. But is this a low or a high memory address?

How big is the virtual memory of a process
The size of the virtual memory of a process depends on your system architecture. In this example I am using a 64-bit machine, so theoretically the size of each process’ virtual memory is 2^64 bytes. In theory, the highest memory address possible is 0xffffffffffffffff (1.8446744e+19), and the lowest is 0x0.

0x1822010 is small compared to 0xffffffffffffffff, so the duplicated string is probably located at a lower memory address. We will be able to confirm this when we will be looking at the proc filesystem).

The proc filesystem
From man proc:

The proc filesystem is a pseudo-filesystem which provides an interface to kernel data structures.  It is commonly mounted at `/proc`.  Most of it is read-only, but some files allow kernel variables to be changed.
If you list the contents of your /proc directory, you will probably see a lot of files. We will focus on two of them:

/proc/[pid]/mem
/proc/[pid]/maps
mem
From man proc:

      /proc/[pid]/mem
              This file can be used to access the pages of a process's memory
          through open(2), read(2), and lseek(2).
Awesome! So, can we access and modify the entire virtual memory of any process?

maps
From man proc:

      /proc/[pid]/maps
              A  file containing the currently mapped memory regions and their access permissions.
          See mmap(2) for some further information about memory mappings.

              The format of the file is:

       address           perms offset  dev   inode       pathname
       00400000-00452000 r-xp 00000000 08:02 173521      /usr/bin/dbus-daemon
       00651000-00652000 r--p 00051000 08:02 173521      /usr/bin/dbus-daemon
       00652000-00655000 rw-p 00052000 08:02 173521      /usr/bin/dbus-daemon
       00e03000-00e24000 rw-p 00000000 00:00 0           [heap]
       00e24000-011f7000 rw-p 00000000 00:00 0           [heap]
       ...
       35b1800000-35b1820000 r-xp 00000000 08:02 135522  /usr/lib64/ld-2.15.so
       35b1a1f000-35b1a20000 r--p 0001f000 08:02 135522  /usr/lib64/ld-2.15.so
       35b1a20000-35b1a21000 rw-p 00020000 08:02 135522  /usr/lib64/ld-2.15.so
       35b1a21000-35b1a22000 rw-p 00000000 00:00 0
       35b1c00000-35b1dac000 r-xp 00000000 08:02 135870  /usr/lib64/libc-2.15.so
       35b1dac000-35b1fac000 ---p 001ac000 08:02 135870  /usr/lib64/libc-2.15.so
       35b1fac000-35b1fb0000 r--p 001ac000 08:02 135870  /usr/lib64/libc-2.15.so
       35b1fb0000-35b1fb2000 rw-p 001b0000 08:02 135870  /usr/lib64/libc-2.15.so
       ...
       f2c6ff8c000-7f2c7078c000 rw-p 00000000 00:00 0    [stack:986]
       ...
       7fffb2c0d000-7fffb2c2e000 rw-p 00000000 00:00 0   [stack]
       7fffb2d48000-7fffb2d49000 r-xp 00000000 00:00 0   [vdso]

              The address field is the address space in the process that the mapping occupies.
          The perms field is a set of permissions:

                   r = read
                   w = write
                   x = execute
                   s = shared
                   p = private (copy on write)

              The offset field is the offset into the file/whatever;
          dev is the device (major:minor); inode is the inode on that device.   0  indicates
              that no inode is associated with the memory region,
          as would be the case with BSS (uninitialized data).

              The  pathname field will usually be the file that is backing the mapping.
          For ELF files, you can easily coordinate with the offset field
              by looking at the Offset field in the ELF program headers (readelf -l).

              There are additional helpful pseudo-paths:

                   [stack]
                          The initial process's (also known as the main thread's) stack.

                   [stack:<tid>] (since Linux 3.4)
                          A thread's stack (where the <tid> is a thread ID).
              It corresponds to the /proc/[pid]/task/[tid]/ path.

                   [vdso] The virtual dynamically linked shared object.

                   [heap] The process's heap.

              If the pathname field is blank, this is an anonymous mapping as obtained via the mmap(2) function.
          There is no easy  way  to  coordinate
              this back to a process's source, short of running it through gdb(1), strace(1), or similar.

              Under Linux 2.0 there is no field giving pathname.
This means that we can look at the /proc/[pid]/mem file to locate the heap of a running process. If we can read from the heap, we can locate the string we want to modify. And if we can write to the heap, we can replace this string with whatever we want.

pid
A process is an instance of a program, with a unique process ID. This process ID (PID) is used by many functions and system calls to interact with and manipulate processes.

We can use the program ps to get the PID of a running process (man ps).

C program
We now have everything we need to write a script or program that finds a string in the heap of a running process and then replaces it with another string (of the same length or shorter). We will work with the following simple program that infinitely loops and prints a “strduplicated” string.

#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>

/**              
 * main - uses strdup to create a new string, loops forever-ever
 *                
 * Return: EXIT_FAILURE if malloc failed. Other never returns
 */
int main(void)
{
     char *s;
     unsigned long int i;

     s = strdup("Holberton");
     if (s == NULL)
     {
          fprintf(stderr, "Can't allocate mem with malloc\n");
          return (EXIT_FAILURE);
     }
     i = 0;
     while (s)
     {
          printf("[%lu] %s (%p)\n", i, s, (void *)s);
          sleep(1);
          i++;
     }
     return (EXIT_SUCCESS);
}
Compiling and running the above source code should give you this output, and loop indefinitely until you kill the process.

julien@holberton:~/holberton/w/hackthevm0$ gcc -Wall -Wextra -pedantic -Werror loop.c -o loop
julien@holberton:~/holberton/w/hackthevm0$ ./loop 
[0] Holberton (0xfbd010)
[1] Holberton (0xfbd010)
[2] Holberton (0xfbd010)
[3] Holberton (0xfbd010)
[4] Holberton (0xfbd010)
[5] Holberton (0xfbd010)
[6] Holberton (0xfbd010)
[7] Holberton (0xfbd010)
...
If you would like, pause the reading now and try to write a script or program that finds a string in the heap of a running process before reading further.

.

.

.

looking at /proc
Let’s run our loop program.

julien@holberton:~/holberton/w/hackthevm0$ ./loop 
[0] Holberton (0x10ff010)
[1] Holberton (0x10ff010)
[2] Holberton (0x10ff010)
[3] Holberton (0x10ff010)
...
The first thing we need to find is the PID of the process.

julien@holberton:~/holberton/w/hackthevm0$ ps aux | grep ./loop | grep -v grep
julien     4618  0.0  0.0   4332   732 pts/14   S+   17:06   0:00 ./loop
In the above example, the PID is 4618 (it will be different each time we run it, and it is probably a different number if you are trying this on your own computer). As a result, the maps and mem files we want to look at are located in the /proc/4618 directory:

/proc/4618/maps
/proc/4618/mem

As we have seen earlier, the /proc/pid/maps file is a text file, so we can directly read it. The content of the maps file of our process looks like this:

julien@ubuntu:/proc/4618$ cat maps
00400000-00401000 r-xp 00000000 08:01 1070052                            /home/julien/holberton/w/funwthevm/loop
00600000-00601000 r--p 00000000 08:01 1070052                            /home/julien/holberton/w/funwthevm/loop
00601000-00602000 rw-p 00001000 08:01 1070052                            /home/julien/holberton/w/funwthevm/loop
010ff000-01120000 rw-p 00000000 00:00 0                                  [heap]
7f144c052000-7f144c20c000 r-xp 00000000 08:01 136253                     /lib/x86_64-linux-gnu/libc-2.19.so
7f144c20c000-7f144c40c000 ---p 001ba000 08:01 136253                     /lib/x86_64-linux-gnu/libc-2.19.so
7f144c40c000-7f144c410000 r--p 001ba000 08:01 136253                     /lib/x86_64-linux-gnu/libc-2.19.so
7f144c410000-7f144c412000 rw-p 001be000 08:01 136253                     /lib/x86_64-linux-gnu/libc-2.19.so
7f144c412000-7f144c417000 rw-p 00000000 00:00 0 
7f144c417000-7f144c43a000 r-xp 00000000 08:01 136229                     /lib/x86_64-linux-gnu/ld-2.19.so
7f144c61e000-7f144c621000 rw-p 00000000 00:00 0 
7f144c636000-7f144c639000 rw-p 00000000 00:00 0 
7f144c639000-7f144c63a000 r--p 00022000 08:01 136229                     /lib/x86_64-linux-gnu/ld-2.19.so
7f144c63a000-7f144c63b000 rw-p 00023000 08:01 136229                     /lib/x86_64-linux-gnu/ld-2.19.so
7f144c63b000-7f144c63c000 rw-p 00000000 00:00 0 
7ffc94272000-7ffc94293000 rw-p 00000000 00:00 0                          [stack]
7ffc9435e000-7ffc94360000 r--p 00000000 00:00 0                          [vvar]
7ffc94360000-7ffc94362000 r-xp 00000000 00:00 0                          [vdso]
ffffffffff600000-ffffffffff601000 r-xp 00000000 00:00 0                  [vsyscall]
Circling back to what we said earlier, we can see that the stack ([stack]) is located in high memory addresses and the heap ([heap]) in the lower memory addresses.

[heap]
Using the maps file, we can find all the information we need to locate our string:

010ff000-01120000 rw-p 00000000 00:00 0                                  [heap]
The heap:

Starts at address 0x010ff000 in the virtual memory of the process
Ends at memory address: 0x01120000
Is readable and writable (rw)
A quick look back to our (still running) loop program:

...
[1024] Holberton (0x10ff010)
...
-> 0x010ff000 < 0x10ff010 < 0x01120000. This confirms that our string is located in the heap. More precisely, it is located at index 0x10 of the heap. If we open the /proc/pid/mem/ file (in this example /proc/4618/mem) and seek to the memory address 0x10ff010, we can write to the heap of the running process, overwriting the “Holberton” string!

Let’s write a script or program that does just that. Choose your favorite language and let’s do it!

If you would like, stop reading now and try to write a script or program that finds a string in the heap of a running process, before reading further. The next paragraph will give away the source code of the answer!

.

.

.

Overwriting the string in the virtual memory
We’ll be using Python 3 for writing the script, but you could write this in any language. Here is the code:

Note: You will need to run this script as root, otherwise you won’t be able to read or write to the /proc/pid/mem file, even if you are the owner of the process.

Running the script
```
julien@holberton:~/holberton/w/hackthevm0$ sudo python3 ./read_write_heap.py 4618 Holberton "Fun w vm!"
[*] maps: /proc/4618/maps
[*] mem: /proc/4618/mem
[*] Found [heap]:
    pathname = [heap]
    addresses = 010ff000-01120000
    permisions = rw-p
    offset = 00000000
    inode = 0
    Addr start [10ff000] | end [1120000]
[*] Found 'Holberton' at 10
[*] Writing 'Fun w vm!' at 10ff010
julien@holberton:~/holberton/w/hackthevm0$ 
```
Note that this address corresponds to the one we found manually:

The heap lies from addresses 0x010ff000 to 0x01120000 in the virtual memory of the running process
Our string is at index 0x10 in the heap, so at the memory address 0x10ff010
If we go back to our loop program, it should now print “fun w vm!”

...
[2676] Holberton (0x10ff010)
[2677] Holberton (0x10ff010)
[2678] Holberton (0x10ff010)
[2679] Holberton (0x10ff010)
[2680] Holberton (0x10ff010)
[2681] Holberton (0x10ff010)
[2682] Fun w vm! (0x10ff010)
[2683] Fun w vm! (0x10ff010)
[2684] Fun w vm! (0x10ff010)
[2685] Fun w vm! (0x10ff010)
...
hack the virtual memory of a process: mind blowing    !



Files
This repo contains the source code for all programs shown in this tutorial:

main.c: the first C program that prints the location of the string and exits
loop.c: the second C program that loops indefinitely
read_write_heap.py: the script used to modify the string in the running C program

