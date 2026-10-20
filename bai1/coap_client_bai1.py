import asyncio
import aiocoap

SERVER_URI = "coap://localhost:5683/iot/lab/message"
STUDENT_ID = "B23DCCN001"       # Sua thanh ma sinh vien cua ban
STUDENT_NAME = "Nguyen Van A"   # Sua thanh ho ten cua ban


async def main():
    context = await aiocoap.Context.create_client_context()
    try:
        print("CoAP Client")
        print("Sending GET request...")
        print(f"URI: {SERVER_URI}")
        response = await context.request(aiocoap.Message(code=aiocoap.GET, uri=SERVER_URI)).response
        print("\nResponse:")
        print(f"Code: {response.code}")
        print(f"Payload: {response.payload.decode('utf-8', errors='replace')}")

        message = f"Xin chao tu CoAP Client - {STUDENT_ID} - {STUDENT_NAME}"
        print("\nSending POST request...")
        print(f"Payload: {message}")
        response = await context.request(
            aiocoap.Message(code=aiocoap.POST, uri=SERVER_URI, payload=message.encode("utf-8"))
        ).response
        print("\nResponse:")
        print(f"Code: {response.code}")
        print(f"Payload: {response.payload.decode('utf-8', errors='replace')}")
    finally:
        await context.shutdown()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, Exception) as exc:
        if not isinstance(exc, KeyboardInterrupt):
            print(f"CoAP client error: {exc}")
