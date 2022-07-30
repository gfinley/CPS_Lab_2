from paho.mqtt import client as mqtt_client
import random
import time

broker = 'localhost'
port = 1883
HIGH_TEMP = 212
topic_sense = "sensor"
topic_act = "action"
    

client_id = f'python-mqtt-{random.randint(0, 1000)}'


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

def subscribe(client: mqtt_client, topic):
    def on_message(client, userdata, msg):
        print(f"I saw the following template message`{msg.payload.decode()}` from `{msg.topic}` topic")
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
