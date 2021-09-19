import socket 
from threading import Thread
import sys 
import json

# Multithreaded Python server : TCP Server Socket Thread Pool
class ClientThread(Thread): 
 
    def __init__(self,ip,port): 
        Thread.__init__(self) 
        self.ip = ip 
        self.port = port 
        print("[+] Client connected: " + ip + ":" + str(port))
 
    def run(self): 
        while True:
            try:
                data = conn.recv(2048)
            except ConnectionAbortedError:
                print("[-] Client aborted connection: " + ip + ":" + str(port))
                sys.exit() # end thread
            except ConnectionResetError:
                print("[-] Client forcibly closed connection: " + ip + ":" + str(port))
                sys.exit() # end thread

            if (data == b""):
                print("[-] Client closed connection: " + ip + ":" + str(port))
                sys.exit() # end thread

            data_string = data.decode("urf-8")
            data_dict = json.loads(data_string)

            print("[r] Server received data:", data_dict)

            MESSAGE = "RCVD"
            conn.send(bytes(MESSAGE, "utf-8"))


# Multithreaded Python server : TCP Server Socket Program Stub
TCP_IP = '0.0.0.0' 
TCP_PORT = 2004 
BUFFER_SIZE = 20  # Usually 1024, but we need quick response 

tcpServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
tcpServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
tcpServer.bind((TCP_IP, TCP_PORT)) 
threads = [] 
 
while True: 
    tcpServer.listen(4) 
    print("[!] Waiting for connections from TCP clients...")
    (conn, (ip,port)) = tcpServer.accept()
    newthread = ClientThread(ip,port)
    newthread.start()
    threads.append(newthread)
 
for t in threads: 
    t.join() 