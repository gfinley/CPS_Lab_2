import asyncio
import sys
import websockets

from azure.messaging.webpubsubservice import WebPubSubServiceClient


async def connect(url):
    async with websockets.connect(url) as ws:
        print('connected')
        while True:
            print('Received message: ' + await ws.recv())

if __name__ == '__main__':

    if len(sys.argv) != 2:
        print('Usage: python subscribe.py  <hub-name>')
        exit(1)

    connection_string = 'Endpoint=https://coslab2.webpubsub.azure.com;AccessKey=HvQkZiRWCI4aKpNkkd3ueDhdyqqdDQXR3g7mM2uouvU=;Version=1.0;'
    hub_name = sys.argv[1]

    service = WebPubSubServiceClient.from_connection_string(connection_string, hub=hub_name)
    token = service.get_client_access_token()

    try:
        asyncio.get_event_loop().run_until_complete(connect(token['url']))
    except KeyboardInterrupt:
        pass