import asyncio
from datetime import datetime

import aiocoap
import aiocoap.resource as resource


class MessageResource(resource.Resource):
    async def render_get(self, request):
        print("GET request received: /iot/lab/message")
        return aiocoap.Message(
            code=aiocoap.CONTENT,
            payload=b"Xin chao tu CoAP Server",
            content_format=0,  # text/plain
        )

    async def render_post(self, request):
        payload = request.payload.decode("utf-8", errors="replace")
        print("\nPOST request received:")
        print(f"Payload: {payload}")
        print(f"Time: {datetime.now().strftime('%H:%M:%S')}")
        return aiocoap.Message(
            code=aiocoap.CHANGED,
            payload="Server da nhan thong diep".encode("utf-8"),
            content_format=0,
        )


async def main():
    root = resource.Site()
    root.add_resource(["iot", "lab", "message"], MessageResource())
    await aiocoap.Context.create_server_context(root, bind=("0.0.0.0", 5683))
    print("CoAP Server started on UDP port 5683")
    await asyncio.get_running_loop().create_future()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nServer stopped.")
