import asyncio
import nats
from nats.errors import ConnectionClosedError, TimeoutError, NoServersError

async def main():
    print("Trying to connect to NATS...")
    nc = await nats.connect("nats://nats:4222")
    print("Connected to NATS!")

    js = nc.jetstream()
    print("Connected to JetStream!")

    # check if server has jetstream enabled
    try:
        js_details = await js.account_info()
        print(js_details)
        print("JetStream enabled on server")
    except Exception as e:
        print("JetStream not enabled on server")
        return
    
    # Check if the stream exists if not create it
    try:
        l = await js.stream_info("ToDownload")
        print("Stream exists!")
    except Exception as e:
        print("Stream does not exist, creating it...")
        await js.add_stream(name="ToDownload", subjects=["ToDownload.sermons"])
    
    # # Publish a message to the stream
    # await nc.publish("ToDownload.sermons", b'http://example.com')
        
    # wait for message from the stream
    while True:
        sub = await js.subscribe("ToDownload.sermons")
        msg = await sub.next_msg()
        print(msg)
    

if __name__ == '__main__':
    asyncio.run(main())

