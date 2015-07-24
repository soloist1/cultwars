"""
mem.py - A script which calculates, formats, and displays a customer's
memory usage
"""

import subprocess
import sys
import collections
import textwrap
import re

HEADER = '\033[95m'
BLUE = '\033[94m'
RED = '\033[1;31m'
GREEN = '\033[92m'
GREY = '\033[1;30m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'

CMD = "ps -o rss,command -u %s | grep -v peruser | awk '{sum += $1} END {print sum / 1024}'"
MEM = {}

CMD2 = "ps -o rss,command -u %s | grep -v peruser" 
MEM2 = collections.defaultdict(lambda:[0,0]) # kb, count

def main():
    proc = subprocess.Popen('groups', shell=True, stdout=subprocess.PIPE)
    proc.wait()
    stdout = proc.stdout.read()

    for user in stdout.split():
        proc = subprocess.Popen(CMD % user, shell=True, stdout=subprocess.PIPE)
        proc.wait()

        MEM[user] = int(float(proc.stdout.read()))

        proc = subprocess.Popen(CMD2 % user, shell=True, stdout=subprocess.PIPE)
        proc.wait()
        for line in list(proc.stdout.readlines())[1:]:
            line = line.strip()
            if not line:
                continue
            kb,p = line.split(' ', 1)
            MEM2[p][0] += int(kb)
            MEM2[p][1] += 1

    print
    print (HEADER+'Total Memory Usage: '+ENDC+RED+'%i MB'+ENDC) % sum(MEM.values())
    print
    for user in sorted(MEM.keys()):
        print user.ljust(15), str(MEM[user]).rjust(3), 'MB'
    print
    print GREY+'Stripping /home/user/webapps/'+ENDC
    print GREY+'='*79+ENDC
    wrapper = textwrap.TextWrapper()
    wrapper.initial_indent = ' '*14
    wrapper.subsequent_indent = ' '*14
    wrapper.width = 79
    for p in sorted(MEM2.keys()):
        print "%6.2f MB" % (MEM2[p][0]/1024.0),
        if MEM2[p][1] > 1:
            print (BLUE+" %ix"+ENDC) % MEM2[p][1],
        else:
            print "   ",
        p = re.sub(r'/home/\w+/webapps/', '', p)
        p = re.sub(r'/home/\w+', '~', p)
        p = wrapper.fill(p)[14:]
        p = re.sub(r'(\w)+(?=/apache\d/)', BLUE+'\g<0>'+ENDC, p, 1)
        print p
    print GREY+'='*79+ENDC
    print

if __name__ == '__main__':
    main()
