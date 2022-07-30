from paho.mqtt import client as mqtt_client
import random
import time

broker = 'localhost'
port = 1883
topic = "python/mqtt"
client_id = f'python-mqtt-{random.randint(0, 1000)}'


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
