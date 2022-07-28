import sys
from azure.messaging.webpubsubservice import WebPubSubServiceClient


#main and variable declarations
if __name__ == '__main__':

    if len(sys.argv) != 3:
        print('Usage: python publish.py <connection-string> <hub-name> <message>')
        exit(1)


    #connection string to a spooled Azure broker
    connection_string = 'Endpoint=https://coslab2.webpubsub.azure.com;AccessKey=HvQkZiRWCI4aKpNkkd3ueDhdyqqdDQXR3g7mM2uouvU=;Version=1.0;'
    hub_name = sys.argv[1]
    message = sys.argv[2]

    service = WebPubSubServiceClient.from_connection_string(connection_string, hub=hub_name)
    res = service.send_to_all(message, content_type='text/plain')
    print(res)