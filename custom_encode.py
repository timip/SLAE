#!/usr/bin/python

from random import randint
import sys

def fbxencode(shellcode):

        iv = '%x' % randint(1,0xffffffff)
        t = iter(iv)
        iv = '\\x' + '\\x'.join(a+b for a,b in zip(t, t))

        while ('\\x00' in iv):
                iv = '%x' % randint(1,0xffffffff)
                t = iter(iv)
                iv = '\\x' + '\\x'.join(a+b for a,b in zip(t, t))

        ivshellcode = iv + shellcode + '\\x90' * (4 - (len(shellcode)/4) % 4) + '\\x50\\x90\\x50\\x90'
        ivshellcode = ivshellcode.replace('\\x', '')

        blocks = []
        for i in range(0, len(ivshellcode)/8):
                blocks.append(int('0x'+ ivshellcode[i*8:i*8+8], 16))
        for i in range(len(blocks)-1):
                blocks[i+1] = (blocks[i] ^ blocks[i+1])

	encoded = ""
	for i in range(len(blocks)):
		encoded += format(blocks[i], '08x')

        return encoded 

def fbxdecode(encoded):

        blocks = []
	cleartext = ""

        for i in range(0, len(encoded)/8):
                blocks.append(int('0x'+ encoded[i*8:i*8+8], 16))

        for i in range(len(blocks)-1):
		if (blocks[i] ^ blocks[i+1] == 0x90509050):
			break
                blocks[i] = (blocks[i] ^ blocks[i+1])
                cleartext += format(blocks[i], '08x')

        return cleartext 

if (len(sys.argv) != 2):
	print "Usage: ./" + sys.argv[0] + " \"<ShellCode>\""
	exit()

shellcode = sys.argv[1]

if '\\' not in shellcode:
	print "[!] Use need to use double quotes or single quotes in shellcode"
	exit()

print "\n[Shellcode]"
print shellcode + "\n"

encoded = fbxencode(shellcode)
t = iter(encoded)
encoded_format = '0x' + ',0x'.join(a+b for a,b in zip(t, t))
while "0x00" in encoded_format:
	encoded = fbxencode(shellcode)
	t = iter(encoded)
	encoded_format = '0x' + ',0x'.join(a+b for a,b in zip(t, t))

print "[Encoded]"
t = iter(encoded)
print '0x' + ',0x'.join(a+b for a,b in zip(t, t))
t = iter(encoded)
print '\\x' + '\\x'.join(a+b for a,b in zip(t, t)) + "\n"

decoded = fbxdecode(encoded)
t = iter(decoded)
print "[Decoded]"
print '\\x' + '\\x'.join(a+b for a,b in zip(t, t)) + "\n"
