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
        bytesToSend = msgToClient("Message from Server: Connection Successful! Welcome!")
        UDPserver.sendto(bytesToSend, address) # Sending a reply to client

    elif jsonMsg["command"] == "/leave":
        bytesToSend = msgToClient("Message from Server: Connection closed. Thank you!")
        UDPserver.sendto(bytesToSend, address) # Sending a reply to client
        print("A connection closed.")
        handles = [i for i in handles if i['addr'] != address]
        print(handles)
    elif jsonMsg["command"] == "/register":
        if (len(handles) == 0):
            handles.append({'handle' : jsonMsg["handle"], 'addr' : address})
            msgFromServer = "Message from Server: Welcome " + jsonMsg["handle"] + "!"
            bytesToSend = msgToClient(msgFromServer)
            print(handles)
        elif any(d['addr'] == address for d in handles):
            bytesToSend  = msgToClient("Error: Registration failed. You are already registered.")
        elif any(d['handle'] == jsonMsg["handle"] for d in handles):
            bytesToSend  = msgToClient("Error: Registration failed. Handle or alias already exists.")
        else:
            handles.append({'handle' : jsonMsg["handle"], 'addr' : address})
            msgFromServer = "Message from Server: Welcome " + jsonMsg["handle"] + "!"
            bytesToSend = msgToClient(msgFromServer)
            print(handles)

        UDPserver.sendto(bytesToSend, address) # Sending a reply to client

    elif jsonMsg["command"] == "/msg":
        list = [x for x in handles if x['addr'] == address]
        obj = iter(list)
        srcList = next(obj, 1)
        if srcList == 1:
            msgFromServer = "Message from Server: Invalid command. Client not registered. Type /register to register"
            bytesToSend = msgToClient(msgFromServer)
            UDPserver.sendto(bytesToSend, address)
        elif any(d['handle'] == jsonMsg["handle"] for d in handles):
            destList = next(y for y in handles if y['handle'] == jsonMsg["handle"])
            destAddr = destList['addr']
            srcHandle = srcList['handle']

            msgSrcClient = jsonMsg["message"]
            bytesSendDest = msgToClient("[From " + srcHandle + "]: " + msgSrcClient + "\nEnter command: ")
            bytesSendSource = msgToClient("[To " + jsonMsg["handle"] + "]: " + msgSrcClient)

            UDPserver.sendto(bytesSendDest, destAddr) # Sending a reply to destination client
            UDPserver.sendto(bytesSendSource, address) # Sending a reply to source client
        else:
            bytesToSend = msgToClient("Error: Handle or alias not found.")
            UDPserver.sendto(bytesToSend, address)

    elif jsonMsg["command"] == "/all":
        list = [x for x in handles if x['addr'] == address]
        obj = iter(list)
        srcList = next(obj, 1)
        if srcList == 1:
            msgFromServer = "Message from Server: Invalid command. Client not registered. Type /register to register"
            bytesToSend = msgToClient(msgFromServer)
            UDPserver.sendto(bytesToSend, address)
        else:
            srcHandle = srcList['handle']
            msgSrcClient = jsonMsg["message"]

            bytesToSend = msgToClient(srcHandle + ": " + msgSrcClient + "\nEnter command: ")
            bytesToSrc = msgToClient(srcHandle + ": " + msgSrcClient)
        
            for d in handles:
                if d['handle'] == srcList['handle']:
                    srcAddr = d['addr']
                    UDPserver.sendto(bytesToSrc, srcAddr) # Source client recieving echo back reply
                else:
                    destAddr = d['addr'] 
                    UDPserver.sendto(bytesToSend, destAddr) # Sending a reply to destination clients
