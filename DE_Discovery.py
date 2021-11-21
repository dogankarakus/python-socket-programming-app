import json
from socket import *


def discovery():

    serverPort = 5001

    print("The discovery server is ready to receive ")
    # Dictionary to keep dictionary.txt info
    dict_x = {}
    # Resetting the file before running the server
    open('dictionary.txt', 'w').close()

    while 1:

        # Create a UDP socket
        serverSocket = socket(AF_INET, SOCK_DGRAM)

        # EDIT THIS
        serverIp = '25.102.76.123'
        # Bind the socket to the port
        serverSocket.bind((serverIp, serverPort))

        message, clientAddress = serverSocket.recvfrom(2048)
        # JSON message to dictionary
        jdict = json.loads(message.decode('utf-8'))

        serverSocket.close()

        # If Received format is correct
        if list(jdict.keys())[0] == "chunks":

            # Discovery Log
            printArray = list(jdict.values())[0].copy()
            print('\n' + "Discovery -- Log")
            print(clientAddress[0] + " : ", end='')
            for x in printArray:
                print(x + ", ", end='')
            # Iterating over received JSON chunks: {"chunk_1", "chunk_2", ..}
            for chunkname in list(jdict.values())[0]:

                tryBool = False

                with open("dictionary.txt", 'r') as read_obj:
                    # Read all lines in the file one by one

                    for line in read_obj:
                        # For each line, check if line contains the string
                        if chunkname in line:
                            tryBool = True
                            break
                    if not clientAddress[0] == serverIp:
                        # If it contains the chunk name
                        if tryBool:

                            repetitiveIP = False
                            searchIndex = 0
                            for searchName in list(dict_x.keys()):
                                if searchName == chunkname:
                                    break
                                searchIndex += 1

                            valueArray = list(dict_x.values())[searchIndex].copy()
                            for x in valueArray:
                                if x == clientAddress[0]:
                                    repetitiveIP = True
                                    break
                            # Insert the IP address if it's new
                            if repetitiveIP == False:
                                valueArray.append(clientAddress[0])
                                d = {chunkname: valueArray}
                                dict_x.update(d)

                    # Insert the new chunk name and IP address
                    else:
                        tempDict = {chunkname: [clientAddress[0]]}
                        dict_x.update(tempDict)

            # Passing the information to dictionary.txt
            if not clientAddress[0] == serverIp:
                with open("dictionary.txt", 'wb+') as dictFile:
                    bdictx = json.dumps(dict_x).encode('utf-8')
                    dictFile.write(bdictx)
                dictFile.close()


if __name__ == "__main__":
    discovery()
