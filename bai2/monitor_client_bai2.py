import asyncio
import json
from datetime import datetime

import aiocoap

SENSOR_URI = "coap://localhost:5683/iot/lab/sensor01/data"


async def main():
    context = await aiocoap.Context.create_client_context()
    print("Monitoring sensor01. Press Ctrl+C to stop.")
    try:
        while True:
            try:
                response = await context.request(
                    aiocoap.Message(code=aiocoap.GET, uri=SENSOR_URI)
                ).response
                data = json.loads(response.payload.decode("utf-8"))
                print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Received sensor data")
                print(f"Device: {data['device_id']}")
                print(f"Temperature: {data['temperature']} C")
                print(f"Humidity: {data['humidity']} %")
                warnings = []
                if data["temperature"] > 35:
                    warnings.append("CANH BAO: Nhiet do cao")
                if data["humidity"] < 40:
                    warnings.append("CANH BAO: Do am thap")
                print("\n".join(warnings) if warnings else "Trang thai: Binh thuong")
                print("-" * 30)
            except Exception as exc:
                print(f"Khong lay duoc du lieu cam bien: {exc}")
            await asyncio.sleep(3)
    finally:
        await context.shutdown()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nMonitoring stopped.")
