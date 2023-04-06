def join(userCommand):
    try:
        inputCommand = str.split(userCommand," ")
        jsonFormat =  { "command":inputCommand[0]}

        # converting to JSON
        intoJSON = json.dumps(jsonFormat)
        bytesSend = str.encode(intoJSON)
        serverAP = (inputCommand[1], int(inputCommand[2])) # Server Address Port

        print(serverAP)

        return bytesSend, serverAP
    except:
        print("Error: Command parameters do not match or is not allowed.")

def leave(userCommand):
    jsonFormat =  { "command":userCommand}

    # converting to JSON
    intoJSON = json.dumps(jsonFormat)
    bytesSend = str.encode(intoJSON)

    return bytesSend

def register(userCommand):
    inputCommand = str.split(userCommand," ")
    jsonFormat =  { "command":inputCommand[0], "handle":inputCommand[1]}

    # converting to JSON
    intoJSON = json.dumps(jsonFormat)
    bytesSend = str.encode(intoJSON)

    return bytesSend

def msg(userCommand):
    inputCommand = str.split(userCommand," ",2)
    print(inputCommand)
    jsonFormat =  { "command":inputCommand[0], "handle":inputCommand[1], "message":inputCommand[2]}

    # converting to JSON
    intoJSON = json.dumps(jsonFormat)
    bytesSend = str.encode(intoJSON)

    return bytesSend

def all(userCommand):
    inputCommand = str.split(userCommand," ",1)
    jsonFormat =  { "command":inputCommand[0], "message":inputCommand[1]}

    # converting to JSON
    intoJSON = json.dumps(jsonFormat)
    bytesSend = str.encode(intoJSON)

    return bytesSend

def printServer(bytesAddressPair):
    convertMsg = str(bytesAddressPair[0], encoding)
    jsonMsg = json.loads(convertMsg)
    serverMsg = "\nMessage from Server:{}".format(jsonMsg["message"])
    print(serverMsg)

# Listen for incoming datagrams
def sender():
    global serverAddressPort
    global joined
    while(True):
        userCommand = input("Enter command: ")

        if "/join" in userCommand:
            try:
                lock.acquire() # Acquire lock before modifying joined variable
                joined = True
                bytesSend, serverAddressPort = join(userCommand)

                # Sent to the server using UDP Socket
                UDPClientSocket.sendto(bytesSend, serverAddressPort)

            except:
                print("Error: Connection to the Message Board Server has failed!")
                print("Please check IP Address and Port Number")
            finally:
                lock.release() # Release lock after modifying joined variable

        elif "/leave" in userCommand:
            lock.acquire() # Acquire lock before modifying joined variable
            if joined == True:
                bytesSend = leave(userCommand)

                # Sent to the server using UDP Socket
                UDPClientSocket.sendto(bytesSend, serverAddressPort)
                joined = False
                break
            else:
                print("Error: Disconnection failed. Please connect to the server first.")

            lock.release() # Release lock after modifying joined variable

        elif "/register" in userCommand:
            bytesSend = register(userCommand)
            # Sent to the server using UDP Socket
            UDPClientSocket.sendto(bytesSend, serverAddressPort)

        elif "/msg" in userCommand:
            bytesSend = msg(userCommand)
            # Sent to the server using UDP Socket
            UDPClientSocket.sendto(bytesSend, serverAddressPort)

        elif "/all" in userCommand:
            bytesSend = all(userCommand)
            # Sent to the server using UDP Socket
            UDPClientSocket.sendto(bytesSend, serverAddressPort)

        elif "/?" in userCommand:
            print(" ")
            print("------ SYNTAX COMMANDS ------")
            print(" ")
            print("Connect to Server App: /join <server_ip_add> <port>")
            print("Disconnect from Server App: /leave")
            print("Register unique hand;e: /register <handle>")
            print("Send message to all: /all <message>")
            print("Send direct messages to a single handle: /msg <handle> <message>")
            print("Syntax commands references: /?")
            print("----------------------------")
            print(" ")

        else:
            print("Error: Command not found.")

        time.sleep(1)

def receiver():

    while(True):
        try:
            bytesAddressPair = UDPClientSocket.recvfrom(bufferSize) # Receive from Server a tuple (bytes, address)
            printServer(bytesAddressPair)
        except:
            print("Error: Connection to the Message Board Server has failed!")
            print("Please check IP Address and Port Number")



import json
import socket
import threading
import time

encoding = 'utf-8'
bufferSize = 1024
global serverAddressPort
global joined
joined = False

# Creating a UDP socket at client side
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

lock = threading.Lock()

while (joined==False):
    userStartCommand = input("Enter command: ")
    commandLen = len(str.split(userStartCommand, " "))
    if "/join" in userStartCommand and commandLen == 3:
        try:
            bytesSend, serverAddressPort = join(userStartCommand)

            # Sent to the server using UDP Socket
            print(serverAddressPort)
            UDPClientSocket.sendto(bytesSend, serverAddressPort)
            joined = True

        except:
            print("Error: Connection to the Message Board Server has failed!")
            print("Please check IP Address and Port Number")
    elif "/?" in userStartCommand:
            print(" ")
            print("------ SYNTAX COMMANDS ------")
            print(" ")
            print("Connect to Server App: /join <server_ip_add> <port>")
            print("Disconnect from Server App: /leave")
            print("Register unique hand;e: /register <handle>")
            print("Send message to all: /all <message>")
            print("Send direct messages to a single handle: /msg <handle> <message>")
            print("Syntax commands references: /?")
            print("----------------------------")
            print(" ")
    else:
        print("Error: Command not found.")

receive = threading.Thread(target=receiver)
send = threading.Thread(target=sender)

if (joined==True):
    print("Thread started")
    receive.start()
    send.start()
