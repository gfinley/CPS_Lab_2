'''
Filename:   actuator.py
Author:     LT Finley
Date:       30-JULY-2022

Purpose:     
Actuator waits for a cooling message from the controller and then "starts" cooling the engine.

major sources:
https://pypi.org/project/paho-mqtt/
http://www.steves-internet-guide.com/mqtt-last-will-example/
https://www.digi.com/resources/documentation/Digidocs/90001541/reference/r_example_subscribe_mqtt.htm
'''
from paho.mqtt import client as mqtt_client
import random
import time

HIGH_TEMP = 212

#connection info
broker = 'localhost'
port = 1883
client_id = f'python-mqtt-{random.randint(0, 1000)}'

#topic info
topic_sense = "sensor"
topic_act = "action"
    

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)
    # Set Connecting Client I
    client = mqtt_client.Client(client_id, clean_session=True)
    client.connect(broker, port)
    return client

def publish(client,topic, msg):
    while True:
        time.sleep(2)
        result = client.publish(topic, msg)
        status = result[0]
        if status == 0:
            print(f"Sendent `{msg}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")

def subscribe(client: mqtt_client, topic):
    def on_message(client, userdata, msg):
        print("From topic: \'{}\' Controller has instructed to {}".format(msg.topic, msg.payload.decode()))
    client.subscribe(topic)
    client.on_message = on_message
    
    
def run():
    client = connect_mqtt()
    print("Connected to MQTT Broker!")
    client.loop_start()
    subscribe(client, topic_act)



if __name__ == '__main__':
    #this is a the actuator listening to the topic "sensor"
    run()
    while True:
        time.sleep(.1)
