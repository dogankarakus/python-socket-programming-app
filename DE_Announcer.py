import os
import math
import json
from socket import *
import threading

#
def announcer60sec():

    clientIP = '25.255.255.255'
    serverPort = 5001
    server_address = (clientIP, serverPort)
    clientSocket = socket(AF_INET, SOCK_DGRAM)

    # myChunks folder to dictionary
    myArray = os.listdir("myChunks")
    dict_z = {"chunks": myArray}
    # dictionary to JSON
    jsonFile = json.dumps(dict_z)
    message = jsonFile

    # If it's not empty announce it
    if myArray:
        clientSocket.sendto(message.encode("utf-8"), server_address)
    clientSocket.close()

# Creating a thread with the function above for periodical announcing
def threadAnnouncer():                      #   |
                                            #   |
    global chunk_announcer60sec             #   V
    chunk_announcer60sec = threading.Thread(target=announcer60sec)
    chunk_announcer60sec.start()
    threading.Timer(60, threadAnnouncer).start()
    print('\n' + "Chunk Announcer running in the background...")

#
def announcer():

    serverIP = '25.255.255.255'
    serverPort = 5001
    server_address = (serverIP, serverPort)
    clientSocket = socket(AF_INET, SOCK_DGRAM)

    # INPUT
    print("Content name: ")
    content_name = input()
    filename = content_name+'.png'


    # <CHUNK DIVIDER>
    c = os.path.getsize(filename)
    CHUNK_SIZE = math.ceil(math.ceil(c)/5)

    index = 1
    with open(filename, 'rb') as infile:
        chunk = infile.read(int(CHUNK_SIZE))
        while chunk:
            chunkname = content_name+'_'+str(index)
            with open("myChunks/" + chunkname, 'wb+') as chunk_file:
                chunk_file.write(chunk)
            index += 1
            chunk = infile.read(int(CHUNK_SIZE))
            chunk_file.close()
    infile.close()

    # </CHUNKDIVIDER>

    # Chunk folder to dictionary
    myArray = os.listdir("myChunks")
    dict_x = {"chunks": myArray}

    # Dictionary to JSON
    jsonFile = json.dumps(dict_x)
    message = jsonFile

    # Sending the message
    clientSocket.sendto(message.encode("utf-8"), server_address)
    clientSocket.close()

if __name__ == '__main__':
    # Periodical Announce
    threadAnnouncer()
    # User Interface
    while 1:
        announcer()
        print("Do you want to continue  [y/n]?")
        if input() == "n":
            break
    print("Announcer is closed")
    exit(0)
