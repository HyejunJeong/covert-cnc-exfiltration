import socket
from cryptography.fernet import Fernet

serverIp = '127.0.0.1'
serverPort = 20001
serverAddressPort = (serverIp,serverPort)
bufferSize = 1024
key ='YbBugTC9pGKLMdak53p6lmy7OVp3E5qegMkMq4iPxU4='


msgFromClient = "this is a message from client"
encoded = msgFromClient.encode()
f = Fernet(key)
encrypted = f.encrypt(encoded)

# Create a UDP socket at client side
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
# Send to server using created UDP socket
UDPClientSocket.sendto(encrypted, serverAddressPort)
msgFromServer = UDPClientSocket.recvfrom(bufferSize)
message = msgFromServer[0]
decrypted = f.decrypt(message).decode() #actual message from server
msg = "Message from Server = {}".format(msgFromServer[0])
msgDec = "Decypted Message from server = {}".format(decrypted)
print(msg)
print(msgDec)