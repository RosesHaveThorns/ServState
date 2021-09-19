# ServState TCP Client: C:/Users/roseb/AppData/Local/Programs/Python/Python39/python.exe "f:/Documents/- Code -/ServState/ServState_BasicClient.py"
import socket
import threading
from time import sleep
import json
import psutil

LOCK = threading.Lock()

REPORTDATA = {"cpu_usage": True, "cpu_freq": True, "disk1_usage": True, "disk2_usage": False, "disk3_usage": False,"disk4_usage": False, "boot_time": True}
current_data = {"cpu_usage": 0, "cpu_freq": 0, "disk1_usage": 0, "disk2_usage": 0, "disk3_usage": 0,"disk4_usage": 0, "boot_time": 0}

def updateStats():
    while True:
        data = psutil.cpu_percent(interval=1)
        with LOCK:
            current_data["cpu_usage"] = data
            

HOST = socket.gethostname()
PORT = 2004
BUFFER_SIZE = 2000 
 
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
client.connect((HOST, PORT))

statsthread = threading.Thread(target=updateStats)
statsthread.daemon = True
statsthread.start()

inp = ""
while inp != 'q':
    inp = input("enter q to quit or nothing to continue")

    with LOCK:
        msg = current_data
    msg_string = json.dumps(msg)

    client.send(bytes(msg_string, "utf-8"))

    data = client.recv(BUFFER_SIZE)
    print("[r] Client received data:", data)

    sleep(1)


statsthread.join()
client.close()