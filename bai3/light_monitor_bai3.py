import asyncio
import json
from datetime import datetime

import aiocoap

LIGHT_URI = "coap://localhost:5683/iot/lab/light01/status"


async def main():
    context = await aiocoap.Context.create_client_context()
    print("Registering CoAP Observe...")
    try:
        request = aiocoap.Message(code=aiocoap.GET, uri=LIGHT_URI, observe=0)
        observation = context.request(request)
        first = True
        try:
            async for response in observation.observation:
                data = json.loads(response.payload.decode("utf-8"))
                label = "Initial State" if first else "State Updated"
                print(f"\n[{datetime.now().strftime('%H:%M:%S')}] {label}")
                print(f"Device: {data['device_id']}")
                print(f"Status: {data['status']}")
                if first:
                    print("Observe registration active; waiting for updates...")
                    first = False
        except aiocoap.error.RequestCancelled:
            pass
    finally:
        await context.shutdown()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nMonitoring stopped.")
