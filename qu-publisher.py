import os, uuid
from azure.storage.queue import QueueServiceClient, QueueClient, QueueMessage

connect_str = 'DefaultEndpointsProtocol=https;AccountName=cpslab2;AccountKey=2f/DlIumrnb4FOzcpzONID/CzP3LQ1Y0Bcl4v7je9Y0KuzoJKyBcG6T5IOaHaUfYWHyV5TddDCdE+AStfJQvTQ==;EndpointSuffix=core.windows.net'
queue_name ="cps-lab-2"


#publish message to queue
def publish_message(message):
    try:
        #print("attempting to connect")
        # Instantiate a QueueClient which will be
        queue_client = QueueClient.from_connection_string(connect_str, queue_name)
        #print("attempting to send message to queue")
        # Send the message to the queue
        queue_client.send_message(message)
        print("message sent")
    except Exception as ex:
        print('Exception:')
        print(ex)
        
try:
    publish_message("Hello World!")
except Exception as ex:
    pass