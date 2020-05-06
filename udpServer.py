import socket
from cryptography.fernet import Fernet

#port,ip,buffersize
localIP     = "127.0.0.1"
localPort   = 20001
bufferSize  = 1024

#generated before-hand with Fernet
key ='YbBugTC9pGKLMdak53p6lmy7OVp3E5qegMkMq4iPxU4='

#encyrpt the message
msgFromServer = 'some command from server'
encoded = msgFromServer.encode()
f = Fernet(key)
encrypted = f.encrypt(encoded)

# Create a datagram socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPServerSocket.bind((localIP, localPort))
print("UDP server up and listening")

# Listen for incoming datagrams
while(True):
    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
    message = bytesAddressPair[0]
    decyrpted = f.decrypt(message).decode() #actual message from client
    address = bytesAddressPair[1]
    clientMsg = "Message from client = {}".format(message)
    clientMsgDec = "Decrypted message from client = {}".format(decyrpted)
    print(clientMsg)
    print(clientMsgDec)

    # Sending a reply to client
    UDPServerSocket.sendto(encrypted, address)