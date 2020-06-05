import os
import sys
import subprocess


script_path = os.path.join(os.path.dirname(__file__), 'zs-dl.py')
call = ['python', script_path, '-u']
for f in sys.argv[1:]:
	call.append(f)
subprocess.Popen(call)