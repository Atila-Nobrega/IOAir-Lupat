from azure.eventhub.aio import EventHubConsumerClient
import asyncio
import json
from utils.db_functions import db_inserir_dados, db_create_table_if_not_exists
from utils.db_object import db
from time import sleep

RECEIVED_MESSAGES = 0
isConnected = False

# Access to the Event Hub-compatible connection string
CONNECTION_STR = "Endpoint=sb://ihsuprodcqres017dednamespace.servicebus.windows.net/;SharedAccessKeyName=iothubowner;SharedAccessKey=j1+9a4vFDgr4tv6P0ZCB+/Z5ck3tsXtK1qY/eG7xYKI=;EntityPath=iothub-ehub-iothub-sen-22804972-e8e802f2e3"

# Define callbacks to process events
async def on_event_batch(partition_context, events):
    global isConnected

    if isConnected:
        pass
    else:
        print("Connecting to database!")
        await db.connect()

        await db_create_table_if_not_exists()
        print("SUCCESS!")

        isConnected = True

    for event in events:

        data = json.loads(event.body_as_str())

        try:
            await db_inserir_dados(data)
            print("OK!")
            print()
        except Exception as e:
            print(e)
    await partition_context.update_checkpoint()

        

        

async def on_error(partition_context, error):
    # Put your code here. partition_context can be None in the on_error callback.
    if partition_context:
        print("An exception: {} occurred during receiving from Partition: {}.".format(
            partition_context.partition_id,
            error
        ))
    else:
        print("An exception: {} occurred during the load balance process.".format(error))


def main():

    loop = asyncio.get_event_loop()
    print ("Starting the Python IoT Hub C2D Messaging device sample...")

    # Instantiate the client
    client = EventHubConsumerClient.from_connection_string(
        conn_str=CONNECTION_STR,
        consumer_group="$default",
    )


    print ("Waiting for C2D messages, press Ctrl-C to exit")
    try:
        loop.run_until_complete(client.receive_batch(on_event_batch=on_event_batch, on_error=on_error))

    except KeyboardInterrupt:
        print("IoT Hub C2D Messaging device sample stopped")
    finally:
        # Graceful exit
        print("Shutting down IoT Hub Client")
        loop.run_until_complete(client.close())
        loop.stop()

if __name__ == '__main__':
    main()