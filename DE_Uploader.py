from socket import *
import json
import os
import datetime

def uploader():

    serverPort = 8000
    serverSocket = socket(AF_INET, SOCK_STREAM)

    #edit the IP
    serverIp = '25.102.76.123'

    serverSocket.bind((serverIp, serverPort))
    serverSocket.listen(1)
    print('The uploader server is ready to receive files')

    while 1:

        connectionSocket, addr = serverSocket.accept()
        message = connectionSocket.recv(1024)

        jdict = json.loads(message.decode('utf-8'))
        chunkname = list(jdict.values())[0]
        print(str(addr[0]) + " requested " + str(chunkname) + "." + '\n' + " Sending..." + '\n')

        chunkArray = os.listdir("myChunks")
        for chunk in chunkArray:
            if chunkname == chunk:
                with open("myChunks/" + chunkname, 'rb') as readfile:

                    data = readfile.read(2048)
                    while data:
                        connectionSocket.send(data)
                        data = readfile.read(2048)

                    ct = datetime.datetime.now()
                    ts = ct.timestamp()
                    with open("logs/uploaderlog.txt", 'a') as logFile:
                        logFile.write("chunk: " + chunkname + " timestamp: " + str(ts) + " to " + addr[0]+'\n')
                    logFile.close()
                break
        connectionSocket.close()

if __name__ == '__main__':
    uploader()