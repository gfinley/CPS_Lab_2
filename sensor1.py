from paho.mqtt import client as mqtt_client
import random
import time

broker = 'localhost'
port = 1883
topic = "python/mqtt"
client_id = f'python-mqtt-{random.randint(0, 1000)}'
#username = 'emqx'
#password = 'public'
topic_sense = "sensor"
topic_act = "action"


def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)
    # Set Connecting Client I
    client = mqtt_client.Client(client_id)
    #client.username_pw_set(username, password)
    client.connect(broker, port)
    return client

def publish(client,topic, msg):
    msg_count = 0
    while True:
        time.sleep(2)
        result = client.publish(topic, msg)
        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"Sendent `{msg}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")
        msg_count += 1

def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

    client.subscribe(topic)
    client.on_message = on_message
    
    
def run():
    topic = "sensor"
    client = connect_mqtt()
    print("Connected to MQTT Broker!")
    client.loop_start()
    publish(client,topic_sense,  get_temp())

#simulate temperature measurement from 200 to 300 degrees
def get_temp():
    return random.randint(200, 300)

if __name__ == '__main__':
    #this is a sensor
    run()
