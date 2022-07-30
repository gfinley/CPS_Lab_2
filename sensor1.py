'''
Filename:   sensor1.py
Author:     LT Finley
Date:       30-JULY-2022

Purpose:     
Sensor1.py is part of Cyber physical systems lab 2. it acts a "sensor" for an engine that regularly publishes its temperature to a MQTT broker.
sensor1 communicates with the controller.py script to send the temperature of the engine.


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
ENGINE_TEMP = 150       #initial temperature#
INCREASE_TEMP = True    #switch to increase temperature
STOP_CHANGE = False     #switch to stop change of temperature
ENGINE_NUMBER = 1       #engine random_number

#mqtt brocker is run on the local machine and port is designed
broker = 'localhost'
port = 1883
client_id = f'python-mqtt-{random.randint(0, 1000)}'

topic_sense = "sensor"


#conencts to mqtt broker
def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)
    #
    #set id (random) no impact on code
    client = mqtt_client.Client(client_id, clean_session=True)
    client.connect(broker, port)
    return client

def publish(client,topic):
    global ENGINE_TEMP, ENGINE_NUMBER
    #container for message to be transmitted (JSON format)
    message = {}
    while True:
        time.sleep(1)
        temp = get_temp()
        
        #add temperature and engine number to message
        message['engine'] = ENGINE_NUMBER
        message['temp'] = ENGINE_TEMP
        
        #convert message to out_data
        out_data = json.dumps(message)
        
        result = client.publish(topic, out_data, qos=1)
        
        status = result[0]
        if status == 0:
            print("Sensor1 published Engine: \'{}\' and Temp: \'{}\' to Topic:\'{}\'".format(ENGINE_NUMBER, ENGINE_TEMP, topic))
        else:
            print(f"Failed to send message to topic {topic}")

def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

    client.on_message = on_message
    
#main function to run the program
def run():
    client = connect_mqtt()
    print("Connected to MQTT Broker!")
    client.loop_start()
    publish(client, topic_sense)

#simulate temperature measurement from initial temp to maxtemp then back down, leveling @140
def get_temp():
    global ENGINE_TEMP
    global INCREASE_TEMP
    global STOP_CHANGE
    if ENGINE_TEMP > 235:
        INCREASE_TEMP = False
    
    if INCREASE_TEMP == True:
        ENGINE_TEMP = ENGINE_TEMP + 5
        return ENGINE_TEMP
    else:
        if STOP_CHANGE == False:
            ENGINE_TEMP = ENGINE_TEMP - 10
    if ENGINE_TEMP < 140:
        STOP_CHANGE = True    
        
    return ENGINE_TEMP
        

if __name__ == '__main__':
    run()
