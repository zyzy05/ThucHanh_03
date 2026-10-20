import asyncio
import json
from datetime import datetime

import aiocoap
import aiocoap.resource as resource


class LightResource(resource.ObservableResource):
    def __init__(self):
        super().__init__()
        self.status = "OFF"

    def payload(self):
        return json.dumps(
            {"device_id": "light01", "status": self.status},
            ensure_ascii=False,
        ).encode("utf-8")

    async def render_get(self, request):
        print("GET request received: /iot/lab/light01/status")
        return aiocoap.Message(
            code=aiocoap.CONTENT,
            payload=self.payload(),
            content_format=50,
        )

    async def render_put(self, request):
        try:
            data = json.loads(request.payload.decode("utf-8"))
            device_id = data.get("device_id")
            command = str(data.get("command", "")).upper()
        except (UnicodeDecodeError, json.JSONDecodeError):
            return aiocoap.Message(code=aiocoap.BAD_REQUEST, payload=b"Invalid JSON")

        if device_id != "light01" or command not in ("ON", "OFF"):
            return aiocoap.Message(
                code=aiocoap.BAD_REQUEST,
                payload=b"device_id must be light01 and command must be ON or OFF",
            )

        old_status = self.status
        print("\nPUT request received:")
        print(f"Time: {datetime.now().strftime('%H:%M:%S')}")
        print(f"Device: {device_id}")
        print(f"Command: {command}")
        self.status = command

        if self.status != old_status:
            self.updated_state()
            print(f"Light state changed: {old_status} -> {self.status}")
            print(f"Notify observers: {self.status}")
        else:
            print(f"Light state unchanged: {self.status}")

        return aiocoap.Message(
            code=aiocoap.CHANGED,
            payload=f"Da cap nhat den light01: {self.status}".encode("utf-8"),
            content_format=0,
        )


async def main():
    root = resource.Site()
    root.add_resource(["iot", "lab", "light01", "status"], LightResource())
    await aiocoap.Context.create_server_context(root, bind=("0.0.0.0", 5683))
    print("CoAP Smart Light Server started on UDP port 5683")
    print("Resource: /iot/lab/light01/status")
    await asyncio.get_running_loop().create_future()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nServer stopped.")
