# Script to clean up inevitable phantomjs crashes (run as sudo)
from subprocess import check_call, check_output
import glob
import os
check_call(['sudo', 'service', 'supervisor', 'stop'])
running_processes = check_output(['ps', 'auxww']).split('\n')
for process_line in running_processes:
    if 'node_modules/phantomjs' in process_line:
        process_details = process_line.split()
        pid = process_details[1]
        print 'Killing phantomjs process %s' % pid
        check_call(['sudo', 'kill', pid])
num_files = 0
for eachfile in glob.iglob('/tmp/*.dmp'):
    os.remove(eachfile)
    num_files += 1
print 'Removed %s crash dump files' % num_files
check_call(['sudo', 'service', 'supervisor', 'start'])
print 'Done!'
