import sys
import subprocess


call = ['python', 'zs-dl.py', '-u']
call.extend(sys.argv[1:])
subprocess.Popen(call)
