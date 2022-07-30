from glob import glob
from paho.mqtt import client as mqtt_client
import random
import time
import json

broker = 'localhost'
port = 1883

client_id = f'python-mqtt-{random.randint(0, 1000)}'


topic_sense = "sensor"
topic_act = "action"
topic_master_monitor = "master_monitor"

ENGINE_TEMP = 150
INCREASE_TEMP = True

STOP_CHANGE = False

ENGINE_NUMBER = 1




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

def publish(client,topic):
    global ENGINE_TEMP, ENGINE_NUMBER
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
        # result: [0, 1]
        status = result[0]
        if status == 0:
            print("Sensor1 published Engine: \'{}\' and Temp: \'{}\' to Topic:\'{}\'".format(ENGINE_NUMBER, ENGINE_TEMP, topic))
        else:
            print(f"Failed to send message to topic {topic}")

def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

    client.on_message = on_message
    
    
def run():
    client = connect_mqtt()
    print("Connected to MQTT Broker!")
    client.loop_start()
    publish(client, topic_sense)

#simulate temperature measurement from 200 to 300 degrees
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
    #this is a sensor
    run()
