'''
Filename:   controller.py
Author:     LT Finley
Date:       30-JULY-2022

Purpose:     
Controller recieves messages from sensors on topic "sensor" and if temp exceeds
some threshold then sends a message to the actuator on topic "action".
controller sets up a "last_will" to transmit to the monitor on topic "master_monitor" if it disconnects from the broker.

major sources:
https://pypi.org/project/paho-mqtt/
http://www.steves-internet-guide.com/mqtt-last-will-example/
https://www.digi.com/resources/documentation/Digidocs/90001541/reference/r_example_subscribe_mqtt.htm
'''
from paho.mqtt import client as mqtt_client
import random
import time
import json


#global vars
HIGH_TEMP = 230
ENGINE_1_TEMP = 0
ENGINE_2_TEMP = 0
COOLING_IN_PROGRESS = False

#connection info
broker = 'localhost'
port = 1883
client_id = f'python-mqtt-{random.randint(0, 1000)}'

#topic info
topic_sense = "sensor"
topic_act = "action"
topic_master_monitor = "master_monitor"


#conencts to broker
def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)
            
    client = mqtt_client.Client(client_id, clean_session=True)
    
    #establish last will message
    client.will_set(topic_master_monitor, payload="The Controller has disconnected from the Broker unxpectedly",qos= 1, retain=True)
    client.connect(broker, port)
    return client

#echos all messages received form sensor messages
def publish(client,topic, msg):
    result = client.publish(topic, msg, qos =2)
    # result: [0, 1]
    status = result[0]
    if status == 0:
        print(f"Sent `{msg}` to topic `{topic}`")
    else:
        print(f"Failed to send message to topic {topic}")


def subscribe(client: mqtt_client, topic):
    def on_message(client, userdata, msg):
        global ENGINE_1_TEMP, ENGINE_2_TEMP, COOLING_IN_PROGRESS
        in_data = {}
        try:
            #receive message load json  data
            in_data = json.loads(msg.payload.decode())
            
            #update global engine temperature
            if in_data.get('engine') == 1:
                ENGINE_1_TEMP = in_data['temp']
            if in_data.get('engine') == 2:
                ENGINE_2_TEMP = in_data['temp']
            
            #logic for controlling "cooling" from the actuator
            print("Engine: \'{}\' Temp:\'{}\' Topic:\'{}\'".format(in_data['engine'], in_data['temp'], msg.topic))
            if (in_data['temp'] > HIGH_TEMP) and (COOLING_IN_PROGRESS == False):
                print("Engine: \'{}\' Temp:\'{}\' is above {} threshold".format(in_data['temp'], in_data['engine'], HIGH_TEMP))
                publish(client, topic_act, "Begin emergency cooling operations!")
                COOLING_IN_PROGRESS = True
            
            if COOLING_IN_PROGRESS == True:
                if (ENGINE_2_TEMP < (.8 *HIGH_TEMP)) and (ENGINE_1_TEMP < (.8 *HIGH_TEMP)):
                    print("Engine 1 temp: {}\nEngine 2 temp: {}\nBoth temperatures below safety threshold, resuming normal operations".format(ENGINE_1_TEMP, ENGINE_2_TEMP))
                    publish(client, topic_act, "Stop emergency cooling operations")
                    COOLING_IN_PROGRESS = False
        except: 
            print("an error occured")

    client.subscribe(topic)
    client.on_message = on_message
    
    
def run():
    
    client = connect_mqtt()
    
    print("Connected to MQTT Broker!")
    client.loop_start()
    #set up all subscriptions
    subscribe(client, topic_sense)


if __name__ == '__main__':
    run()
    while True:
        time.sleep(.1)
