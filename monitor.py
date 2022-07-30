'''
Filename:   monitor.py
Author:     LT Finley
Date:       30-JULY-2022

Purpose:     
Monitor acts as a monitor to view all messages in all topics. 
It subscribes to all topics and prints out the messages.

major sources:
https://pypi.org/project/paho-mqtt/
http://www.steves-internet-guide.com/mqtt-last-will-example/
https://www.digi.com/resources/documentation/Digidocs/90001541/reference/r_example_subscribe_mqtt.htm
'''

from paho.mqtt import client as mqtt_client
import random
import time

broker = 'localhost'
port = 1883
topic = "python/mqtt"
client_id = f'python-mqtt-{random.randint(0, 1000)}'

#topics to subscribe to
topic_sense = "sensor"
topic_act = "action"
topic_master_monitor = "master_monitor"

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)
    # Set Connecting Client I
    client = mqtt_client.Client(client_id, clean_session=True)

    #client.username_pw_set(username, password)
    client.connect(broker, port)
    return client

#print out every received message
def subscribe(client: mqtt_client,topic):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

    client.subscribe(topic)
    client.on_message = on_message
    
    
def run():
    client = connect_mqtt()
    print("Connected to MQTT Broker!")
    client.loop_start()
    subscribe(client, topic_sense)
    subscribe(client, topic_act)
    subscribe(client, topic_master_monitor)
    
if __name__ == '__main__':
    run()
    while True:
        time.sleep(.1)
