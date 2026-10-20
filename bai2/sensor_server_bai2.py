import asyncio
import json
import random

import aiocoap
import aiocoap.resource as resource


class SensorResource(resource.Resource):
    def __init__(self):
        super().__init__()
        self.temperature = round(random.uniform(22.0, 34.0), 1)
        self.humidity = round(random.uniform(40.0, 75.0), 1)

    def update_values(self):
        self.temperature = round(random.uniform(20.0, 40.0), 1)
        self.humidity = round(random.uniform(30.0, 80.0), 1)

    async def render_get(self, request):
        data = {
            "device_id": "sensor01",
            "temperature": self.temperature,
            "humidity": self.humidity,
        }
        return aiocoap.Message(
            code=aiocoap.CONTENT,
            payload=json.dumps(data, ensure_ascii=False).encode("utf-8"),
            content_format=50,  # application/json
        )


async def main():
    sensor = SensorResource()
    root = resource.Site()
    root.add_resource(["iot", "lab", "sensor01", "data"], sensor)
    await aiocoap.Context.create_server_context(root, bind=("0.0.0.0", 5683))
    print("Sensor CoAP Server started on UDP port 5683")
    try:
        while True:
            await asyncio.sleep(3)
            sensor.update_values()
            print(f"Updated sensor: {sensor.temperature} C, {sensor.humidity} %")
    finally:
        print("Sensor server stopped.")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nServer stopped.")
