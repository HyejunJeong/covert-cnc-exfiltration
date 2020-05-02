
server2 and client2 lack data hiding from scapy and use regular tcp socket only. Besides this, it has everything the project required.

Run server2 first and then client2 on your ubuntu machine. 

Wait for client connection and run list to see connected clients. 

run select <client number> to select the target. 

Run quit to exit out of target. 

After that, try running a command. You can download and upload files using download <file name from target> and upload <file name from C&C computer> to download and send files from/to victim respectively 

We need to rewrite the message send and recieve through a covert channel so data is not suspicious

