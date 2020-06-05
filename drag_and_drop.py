import sys
import subprocess

# Append other args here.
call = ['python', 'zs-dl.py']
call.append('-u')
call.extend(sys.argv[1:])
subprocess.Popen(call)
