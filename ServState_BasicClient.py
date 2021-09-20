# ServState TCP Client: C:/Users/roseb/AppData/Local/Programs/Python/Python39/python.exe "f:/Documents/- Code -/ServState/ServState_BasicClient.py"
#                       
import socket
import threading
from time import sleep
import time
import json
import psutil
import signal
import sys

REPORT_RATE = 2 * 10**9      # nanoseconds between status reports
DATA_UPDATE_RATE = 10        # milliseconds between data updates

LOCK = threading.Lock()

# leave blank if not reporting that disk's stats
DISK1_ADDR = "C:/"
DISK2_ADDR = ""
DISK3_ADDR = ""
DISK4_ADDR = ""

REPORTDATA = {"cpu_usage": True, "cpu_freq": True, "disk1_usage": True, "disk2_usage": False, "disk3_usage": False,"disk4_usage": False, "up_time": True}
current_data = {"epoch_time": 0, "cpu_usage": 0, "cpu_freq": 0, "disk1_usage": 0, "disk2_usage": 0, "disk3_usage": 0,"disk4_usage": 0, "up_time": 0}

runStatsUpdate = True
def updateStats():
    while runStatsUpdate:
        epoch_time = time.time_ns();
        if REPORTDATA["cpu_usage"]: cpu_usage = psutil.cpu_percent(interval=1)
        if REPORTDATA["cpu_freq"]: cpu_freq = psutil.cpu_freq().current
        if REPORTDATA["disk1_usage"]: disk1_usage = psutil.disk_usage(DISK1_ADDR).percent
        if REPORTDATA["disk2_usage"]: disk2_usage = psutil.disk_usage(DISK2_ADDR).percent
        if REPORTDATA["disk3_usage"]: disk3_usage = psutil.disk_usage(DISK3_ADDR).percent
        if REPORTDATA["disk4_usage"]: disk4_usage = psutil.disk_usage(DISK4_ADDR).percent
        if REPORTDATA["up_time"]: up_time =  epoch_time - (psutil.boot_time() * 10**9)
        
        with LOCK:
            current_data["epoch_time"] = epoch_time
            if REPORTDATA["cpu_freq"]: current_data["cpu_freq"] = cpu_freq
            if REPORTDATA["cpu_usage"]: current_data["cpu_usage"] = cpu_usage
            if REPORTDATA["disk1_usage"]: current_data["disk1_usage"] = disk1_usage
            if REPORTDATA["disk2_usage"]: current_data["disk2_usage"] = disk2_usage
            if REPORTDATA["disk3_usage"]: current_data["disk3_usage"] = disk3_usage
            if REPORTDATA["disk4_usage"]: current_data["disk4_usage"] = disk4_usage
            if REPORTDATA["up_time"]: current_data["up_time"] = up_time
        
        sleep(DATA_UPDATE_RATE/1000)
            

HOST = socket.gethostname()
PORT = 2004
BUFFER_SIZE = 2000 

print("[i] Press ctrl-C to close the connection")
print("[!] Connecting to server: " + HOST + ':' + str(PORT))

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
client.connect((HOST, PORT))

statsthread = threading.Thread(target=updateStats)
statsthread.start()

# if ctrl-c sent, tidy then close
def quit(sig, frame):
    global runStatsUpdate
    print("[-] Disconnecting from server")
    with LOCK:
        runStatsUpdate = False
    client.close()
    statsthread.join()
    sys.exit(0)

signal.signal(signal.SIGINT, quit)

print("[+] Connected to server, reporting every " + str(REPORT_RATE/10**9) + " seconds")

last_run = 0
while True:
    if (time.time_ns() - last_run < REPORT_RATE):
        continue

    last_run = time.time_ns();

    with LOCK:
        msg = current_data
    msg_string = json.dumps(msg)

    client.send(bytes(msg_string, "utf-8"))

    data = client.recv(BUFFER_SIZE)
    print("[r] Client received data:", data)