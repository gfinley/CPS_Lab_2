import os, uuid
from azure.storage.queue import QueueServiceClient, QueueClient, QueueMessage

connect_str = 'DefaultEndpointsProtocol=https;AccountName=cpslab2;AccountKey=2f/DlIumrnb4FOzcpzONID/CzP3LQ1Y0Bcl4v7je9Y0KuzoJKyBcG6T5IOaHaUfYWHyV5TddDCdE+AStfJQvTQ==;EndpointSuffix=core.windows.net'
queue_name ="cps-lab-2"

try:
    print("attempting to connect")
    # Instantiate a QueueClient which will be
    # used to create and manipulate the queue
    queue_client = QueueClient.from_connection_striPng(connect_str, queue_name)
    
    #print("attempting to peek from queue")
    
    #peeked_messages = queue_client.peek_messages(max_messages=10)
    
    #for peek_message in peeked_messages:
    #    print(peek_message.content)
        
    print("pulling messages from queue")
    messages = queue_client.receive_messages(messages_per_page=5)
    for messages in messages:
        print(messages.content)    
    
     
    # Quick start code goes here
except Exception as ex:
    print('Exception:')
    print(ex)
