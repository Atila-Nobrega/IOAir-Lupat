from time import sleep
from azure.iot.device.aio import IoTHubDeviceClient
from datetime import datetime
import pnp_helper
import asyncio
import serial

#
#

arduino = serial.Serial(port="COM3", baudrate=9600, timeout=15)


DEVICE_CONNECTION_STRING = "HostName=IoTHub-Sensor.azure-devices.net;DeviceId=Sensor;SharedAccessKey=SWkjtiEFKMPhz7PgC+/pV5jsu2Fdlhmbz4d8aw7th6k="
DEVICE_ID="Sensor"

thermostat_1_component_name = "Termostato1"

device_client = IoTHubDeviceClient.create_from_connection_string(
    DEVICE_CONNECTION_STRING, product_info=DEVICE_ID
)

async def iothub_messaging_sample_run():
    try:
        i = 0

        while(True):
            message = arduino.read_until().decode("utf-8")
            data = message.split('|')
            if(len(data) < 5):
                print("Incorrect message Received:")
                print(message)
            else:
                data.pop()

                if(message != ''):
                    i += 1
                    print("sending message!")
                    
                    dict = {
                        "humidity": data[0],
                        "celsius": data[1],
                        "fahrenheit": data[2],
                        "heatindexcelsius": data[3],
                        "heatindexfahrenheit": data[4],
                        "airquality": data[5],
                        "alarmset": data[6],
                        "date": datetime.now().isoformat()
                    }

                    await send_telemetry_from_temp_controller(
                        device_client, dict, thermostat_1_component_name
                    )

                    print("OK!")
                    sleep(3)
                else:
                    print("Aguardando mensagem...")

    except Exception as ex:
        print ( "Unexpected error {0}" % ex )
        return
    except KeyboardInterrupt:
        print ( "IoT Hub C2D Messaging service sample stopped" )

async def send_telemetry_from_temp_controller(device_client, telemetry_msg, component_name=None):
    msg = pnp_helper.create_telemetry(telemetry_msg, component_name)
    await device_client.send_message(msg)

    await asyncio.sleep(1)


if __name__ == '__main__':
    print ( "Starting the Python IoT Hub C2D Messaging service sample..." )
    asyncio.run(iothub_messaging_sample_run())