# C:/Users/mbrin/AppData/Local/Programs/Python/Python38-32/python.exe "c:/Users/mbrin/Documents/- Code -/ServState/ServState_Server.py"

import socket 
import threading
from threading import Thread
import os, sys
import json
import keyboard

LOCK = threading.Lock()

# Multithreaded Python server : TCP Server Socket Thread Pool
class ClientThread(Thread): 
 
    def __init__(self,ip,port): 
        Thread.__init__(self) 
        self.ip = ip 
        self.end_thread = False
        self.port = port 
        print("[+] Client connected: " + ip + ":" + str(port))
 
    def run(self):
        while not self.end_thread:
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

            data_string = data.decode("utf-8")
            data_dict = json.loads(data_string)

            print("[r] Server received data:", data_dict)

            MESSAGE = "RCVD"
            conn.send(bytes(MESSAGE, "utf-8"))
        
        conn.close()


# Multithreaded Python server : TCP Server Socket Program Stub
TCP_IP = '0.0.0.0' 
TCP_PORT = 2004 
BUFFER_SIZE = 20  # Usually 1024, but we need quick response 

print("[iq] Press q to close the server")
tcpServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
tcpServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
tcpServer.bind((TCP_IP, TCP_PORT)) 
threads = [] 

# if ctrl-c sent, tidy then close
def quit():
    print("[!] Closing connections")
    for t in threads:
        t.end_thread = True
    for t in threads: 
        print("[-] Waiting for " + t.ip + "to disconnect")
        t.join() 
    os._exit(0) # for unkown reasons, sys.exit does not work

keyboard.on_press_key("q", lambda _:quit())
 
while True: 
    tcpServer.listen(4) 
    print("[!] Searching for connections from TCP clients...")
    (conn, (ip,port)) = tcpServer.accept()
    newthread = ClientThread(ip,port)
    newthread.start()
    threads.append(newthread)