import datetime
import json
import os
from socket import *

def downloader():

    serverPort = 8000
    print('\n')
    reqContent = input('Enter the filename you want to download:')

    x = ''
    with open("dictionary.txt", 'r') as readFile:
        for line in readFile:
            x = x + str(line)

    dict_x = json.loads(x)

    # Progress Bar variables
    progressBarPerc = 0
    myString = ""


    for chunkIndex in range(5):

        keyPosition = 0
        for searchIndex in list(dict_x.keys()):
            if searchIndex == reqContent + "_" + str(chunkIndex+1):
                break
            keyPosition += 1




        i = 0   #ipAddr index
        for ipAddr in list(dict_x.values())[keyPosition]:
            i += 1
            try:

                clientSocket = socket(AF_INET, SOCK_STREAM)
                clientSocket.connect((ipAddr, serverPort))

                # message to dictionary
                dict_y = {"requested_content": reqContent + "_" + str(chunkIndex + 1)}
                # dictionary to JSON
                jsonFile = json.dumps(dict_y)
                size = len(list(dict_x.values())[keyPosition])
                clientSocket.send(jsonFile.encode("utf-8"))

                # Downloading the data
                receivedFile = b''
                data = clientSocket.recv(2048)

                while data:
                    receivedFile += data
                    data = clientSocket.recv(2048)

                # If the chunk is not empty
                if receivedFile:
                    # Homemade Progress Bar
                    blankString = ""
                    progressBarPerc += 20
                    for n in range(int((100 - progressBarPerc) / 10)):
                        blankString += "  "
                    myString += "████"

                    print('\n' + reqContent + "_" + str(chunkIndex+1) + " is downloaded from " + ipAddr + " [" + myString + blankString +  "] " + str(progressBarPerc) + "%" )

                    # Writing the chunk to relevant folders
                    with open("Downloader's_Recieved_Chunks/" + reqContent + "_" + str(chunkIndex+1), 'wb+') as chunk_file:
                        chunk_file.write(receivedFile)
                    chunk_file.close()
                    with open("myChunks/" + reqContent + "_" + str(chunkIndex+1), 'wb+') as chunk_file:
                        chunk_file.write(receivedFile)
                        ct = datetime.datetime.now()
                        ts = ct.timestamp()
                        with open("logs/downloaderlog.txt", 'a') as logFile:
                            logFile.write("chunk: " + reqContent + "_" + str(chunkIndex+1) + " timestamp: " + str(ts) + " from " + ipAddr + '\n')
                        logFile.close()
                    chunk_file.close()

                    clientSocket.close()
                    break
                # If all addresses is tried and chunk cannot be downloaded
                elif i == size:
                    print("CHUNK " + reqContent + "_" + str(chunkIndex + 1) + " CANNOT BE DOWNLOADED FROM ONLINE PEERS " + '\n')
                    print("CHUNK " + reqContent + "_" + str(chunkIndex+1) + " CANNOT BE DOWNLOADED FROM "  + str(ipAddr) + "!")
                clientSocket.close()
            # If any error occur
            except error:
                # Resetting the file for new operation
                receivedFile = b''




    chunkArray = os.listdir("Downloader's_Recieved_Chunks")

    for i in range(5):
        boolGo = False
        for x in chunkArray:
           if (reqContent + "_" + str(i+1)) == x:
                boolGo = True
        if boolGo is False:
            break


    if boolGo:
        with open("Downloaded_Contents/" + reqContent + '.png', 'wb') as outfile:
            for x in range(5):
                with open("Downloader's_Recieved_Chunks/" + reqContent + "_" + str(x+1), 'rb') as infile:
                    outfile.write(infile.read())
                infile.close()
        outfile.close()
        print("File is successfully downloaded")



if __name__ == '__main__':
    while 1:
        downloader()
        print("Do you want to continue  [y/n]?")
        if input() == "n":
            break
    print("Downloader is closed")
    exit(0)