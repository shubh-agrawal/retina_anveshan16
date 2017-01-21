import subprocess

p = subprocess.Popen('ps aux | grep python', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
for line in p.stdout.readlines():
    pid = line.split(' ')
    print pid
    strn = "comm.launch\n"
    if strn in pid:
        print pid[6]
        cmd = "kill -9 " + str(pid[6])
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)


