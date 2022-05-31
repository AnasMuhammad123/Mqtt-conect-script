from ast import Break, Str
from cgi import print_directory
from re import A, I
import sys
from tracemalloc import start
from paho.mqtt import client
from random import uniform
import time
import keyboard as key
import threading


HOST = "localhost"
cond = True

def onConnect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

def onMessage(client, userdata, msg):
    if(msg.payload.decode("utf-8") == "DISC"):
        client.publish("TEMPREATURE", "DISC")
        client.disconnect()
        print("I am disconnected!")
    print("client:"+msg.topic+" "+str(msg.payload))

def onMessagePublisher(client, userdata, msg):
    global cond
    
    if(msg.payload.decode("utf-8") == "DISC"):
        cond = False
        print("Publisher disconnect")
        client.disconnect()
        client.loop_stop()

def onDisconnect(client,  userdata, rc):
    print("client is disconected")

def clientFunc():
    _client = client.Client(client_id="client_1")


    _client.connect(HOST, 1883, keepalive=20)
    _client.subscribe("TEMPREATURE")
   # _client.subscribe("OUTDOORENVIRONMENT")
    _client.on_connect = onConnect
    _client.on_message = onMessage
    _client.on_disconnect = onDisconnect
    _client.loop_start()
    
   
def publisherFunc():
    _publisher = client.Client("publisher_1")
    _publisher.connect(HOST)
    print("publisher is connected")
    _publisher.subscribe("TEMPREATURE1")
    _publisher.subscribe("OURDOOEWNVIRONMENT")
    _publisher.on_message = onMessagePublisher
    _publisher.on_disconnect=onDisconnect
    i = 0
    _publisher.loop_start()
    _timeout = 30
    _timeout_start=time.time()
        
        
    while time.time() < _timeout_start + 10:
        randNumber= uniform(20.0, 21.0)
        _publisher.publish("TEMPREATURE", randNumber)
        print("server:"+"just published "+str(i) +" Number: "+ str(randNumber) + " to Topic TEMPREATURE")
        
        time.sleep(1)
        i+= 1  
    
    print ("server is disconnected....")
    time.sleep(3)
    print("client is disconnected......")
        
         
          
 
     

 

if __name__ == "__main__":
    t1= threading.Thread(target=clientFunc)
    t1.start()
    t2= threading.Thread(target=publisherFunc)
    t2.start()
    


