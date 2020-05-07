# Covert C&C and Exfiltration

#### https://github.com/HyejunJeong/covert-cnc-exfiltration

This program is a client and a server for covert command and control of, and data exfiltration from, an infected client. 


#### Requirements for Server and Client
* Linux

## Getting Started

This project is divided into the server and client program.

### Running the Server

#### Instructions
1. cd to the project directory, and ssh into aws cloud server. 
    ```shell
    chmod 700 ./aws_key.pem 
    ssh -i "aws_key.pem" ubuntu@ec2-18-205-103-236.compute-1.amazonaws.com
    ```
2. In the aws cloud server, cd to covert-cnc-exfiltration and run the server.
    ```shell
    cd covert-cnc-exfiltration
    sudo python3 server2.py
    ```


### Running the _client_
> **Note:** You will have to **start the server first** before running the clients. You may run the client program in multiple machines.

1. Clone this repository.
    ```shell
    git clone https://github.com/HyejunJeong/covert-cnc-exfiltration
    ```

2. Run the client on the project directory (in the client machine).
    ```shell
    python3 client2.py
    ```
    > **Note:** By running client2.py on your computer will give the cloud server control of your computer (hence "botnet") so it's good idea to use a virtual machine instead of your actual computer.


------------------------------------------
server2 and client2 lack data hiding from scapy and use regular tcp socket only. Besides this, it has everything the project required.

Run server2 first and then client2 on your ubuntu machine. 

Wait for client connection and run list to see connected clients. 

run select <client number> to select the target. 

Run quit to exit out of target. 

After that, try running a command. You can download and upload files using download <file name from target> and upload <file name from C&C computer> to download and send files from/to victim respectively 

We need to rewrite the message send and recieve through a covert channel so data is not suspicious


ssh into aws cloud server 

run "chmod 700 ./aws_key.pem"
then do "ssh -i "aws_key.pem" ubuntu@ec2-18-205-103-236.compute-1.amazonaws.com"

UPDATED: 
client2 now connects to the aws cloud server. server2.py thus should run inside the aws server. You can access the cloud server machine by using the above commands. Note, by running client2 on your computer will give the cloud server control of your computer(hence "botnet") so its good idea to use a virtual machine instead of your actual computer.

If your command is invlaid, it will say no such file found or something similar. This is because subproccess uses the underlying POSIX execve and thats what it will report if command is invalid. 

If you do download on a file that doesn't exist, it will give you the same error.

If you do upload on a file that doesn't exist, it will tell you so. 

To rewrite the send and receieve function so data are hidden; please edit the server_send(self, conn, msg) in server2.py, def server_recv(self, conn) in server2py, def client_send(self, msg) in client2.py, and def client_recv(self) in client2.py

A server and the client communicates through a TCP with encryption.
