import asyncio
import json

import aiocoap

LIGHT_URI = "coap://localhost:5683/iot/lab/light01/status"


async def main():
    context = await aiocoap.Context.create_client_context()
    try:
        while True:
            command = (await asyncio.to_thread(
                input, "Nhap lenh (ON/OFF/STATUS/EXIT): "
            )).strip().upper()

            if command == "EXIT":
                break
            if command in ("ON", "OFF"):
                payload = json.dumps({
                    "device_id": "light01",
                    "command": command,
                }).encode("utf-8")
                print("Sending PUT request...")
                request = aiocoap.Message(
                    code=aiocoap.PUT,
                    uri=LIGHT_URI,
                    payload=payload,
                    content_format=50,
                )
            elif command == "STATUS":
                print("Sending GET request...")
                request = aiocoap.Message(code=aiocoap.GET, uri=LIGHT_URI)
            else:
                print("Lenh khong hop le. Hay nhap ON, OFF, STATUS hoac EXIT.")
                continue

            try:
                response = await context.request(request).response
                print(f"Response Code: {response.code}")
                print(f"Response: {response.payload.decode('utf-8', errors='replace')}")
                if command == "STATUS" and response.payload:
                    try:
                        print(json.dumps(json.loads(response.payload.decode("utf-8")), ensure_ascii=False))
                    except json.JSONDecodeError:
                        pass
            except Exception as exc:
                print(f"Loi giao tiep CoAP: {exc}")
    finally:
        await context.shutdown()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nController stopped.")
