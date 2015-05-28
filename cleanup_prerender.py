# Script to clean up inevitable phantomjs crashes (run as sudo)
from subprocess import check_call, check_output
import glob
import os

def kill_running_phantomjs_processes():
    running_processes = check_output(['ps', 'auxww']).split('\n')
    for process_line in running_processes:
        if 'node_modules/phantomjs' in process_line:
            process_details = process_line.split()
            pid = process_details[1]
            try:
                check_call(['sudo', 'kill', pid])
                print 'Killed phantomjs process %s' % pid
            except:
                print 'Unable to kill phantomjs process %s (already stopped?)' % pid

def remove_crash_dump_files():
    num_files = 0
    for eachfile in glob.iglob('/tmp/*.dmp'):
        os.remove(eachfile)
        num_files += 1
    print 'Removed %s crash dump files' % num_files

check_call(['sudo', 'service', 'supervisor', 'stop'])
try:
    kill_running_phantomjs_processes()
    remove_crash_dump_files()
except Exception as e:
    raise e
finally:
    check_call(['sudo', 'service', 'supervisor', 'start'])
print 'Done!'
