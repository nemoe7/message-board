def msgToClient(msgFromServer):
    jsonFormat =  {"message":msgFromServer}
    intoJSON = json.dumps(jsonFormat) # converting to JSON
    bytesSend = str.encode(intoJSON)

    return bytesSend

import socket
import json

encoding = 'utf-8'
localIP     = "127.0.0.1"
localPort   = 12345
bufferSize  = 1024
handles = []
global destAddr

msgFromServer = "Hello UDP Client"
jsonFormat =  {"message":msgFromServer}
intoJSON = json.dumps(jsonFormat)
bytesToSend = str.encode(intoJSON)

# Create a datagram socket
UDPserver = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPserver.bind((localIP, localPort)) # Bind to address and ip

print("UDP server up and listening")

# Listen for incoming datagrams
while(True):
    bytesAddressPair = UDPserver.recvfrom(bufferSize) # Receive from Server a tuple (bytes, address)
    address = bytesAddressPair[1]
    convertMsg = str(bytesAddressPair[0], encoding) # Converting message from bytes to str
    jsonMsg = json.loads(convertMsg) # Parse str to json

    if jsonMsg["command"] == "/join":
        print("New client connected at " + address[0] + ":" + str(address[1]))
        bytesToSend = msgToClient("Connection Successful! Welcome!")
        UDPserver.sendto(bytesToSend, address) # Sending a reply to client

    elif jsonMsg["command"] == "/leave":
        bytesToSend = msgToClient("Connection closed. Thank you!")
        UDPserver.sendto(bytesToSend, address) # Sending a reply to client
        print("A connection closed.")

    elif jsonMsg["command"] == "/register":
        if (len(handles) == 0):
            handles.append({'handle' : jsonMsg["handle"], 'addr' : address})
            msgFromServer = "Welcome " + jsonMsg["handle"] + "!"
            bytesToSend = msgToClient(msgFromServer)
            print(handles)
        else:
            if any(d['handle'] == jsonMsg["handle"] for d in handles):
                bytesToSend  = msgToClient("Error: Registration failed. Handle or alias already exists.")
            else:
                handles.append({'handle' : jsonMsg["handle"], 'addr' : address})
                msgFromServer = "Welcome " + jsonMsg["handle"] + "!"
                bytesToSend = msgToClient(msgFromServer)
                print(handles)

        UDPserver.sendto(bytesToSend, address) # Sending a reply to client

    elif jsonMsg["command"] == "/msg":
        if any(d['handle'] == jsonMsg["handle"] for d in handles):
            destList = next(x for x in handles if x["handle"] == jsonMsg["handle"])
            destAddr=destList['addr']
            srcList = next(x for x in handles if x["addr"] == address)
            srcHandle = srcList['handle']

            msgSrcClient = jsonMsg["message"]
            bytesSendDest = msgToClient("\n[From " + srcHandle + "]: " + msgSrcClient + "\nEnter command: ")
            bytesSendSource = msgToClient("\n[To " + jsonMsg["handle"] + "]: " + msgSrcClient)

            UDPserver.sendto(bytesSendDest, destAddr) # Sending a reply to destination client
            UDPserver.sendto(bytesSendSource, address) # Sending a reply to source client
        else:
            bytesToSend = msgToClient("Error: Handle or alias not found.")
            UDPserver.sendto(bytesToSend, address)

    elif jsonMsg["command"] == "/all":
        list = [x for x in handles if x["addr"] == address]
        obj = iter(list)
        srcList = next(obj, 1)
        if srcList == 1:
            msgFromServer = "Invalid command. Client not registered. Type /register to register"
            bytesToSend = msgToClient(msgFromServer)
            UDPserver.sendto(bytesToSend, address)
        else:
            srcHandle = srcList['handle']
            msgSrcClient = jsonMsg["message"]

            bytesToSend = msgToClient("\n" + srcHandle + ": " + msgSrcClient + "\nEnter command: ")

            for x in handles:
                destAddr = x["addr"] 
                UDPserver.sendto(bytesToSend, destAddr) # Sending a reply to destination clients
