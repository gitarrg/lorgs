


PAYLOAD_1 = {
    "insertId": "61788754000a0b8b43f0b2dc",
    "labels": {
        "clone_id": "00c61b117cba9972023680f55995e09a97c2673752ae057c2dd100a829309e2710f47552c7fc80f7624dbbba69003bbd53b295080d4b358e5b1838ce446ea85b5cede1fb6d53cdec"
    },
    "logName": "projects/lorrgs/logs/stderr",
    "receiveTimestamp": "2021-10-26T22:55:16.913830757Z",
    "resource": {
        "labels": {
            "module_id": "default",
            "project_id": "lorrgs",
            "version_id": "user-reports",
            "zone":"europe-west2-3"
        },
        "type": "gae_app"
    },
    "severity": "ERROR",
    "timestamp": "2021-10-26T22:55:16.658315Z",
    "textPayload": "Traceback (most recent call last):\nFile \"/layers/google.python.pip/pip/lib/python3.9/site-packages/uvicorn/protocols/http/httptools_impl.py\",line 375, in run_asgi\nresult = await app(self.scope, self.receive, self.send)\nFile \"/layers/google.python.pip/pip/lib/python3.9/site-packages/uvicorn/middleware/proxy_headers.py\",line 75, in __call__\nreturn await self.app(scope, receive, send)\nFile \"/layers/google.python.pip/pip/lib/python3.9/site-packages/fastapi/applications.py\",line 208, in __call__\nawait super().__call__(scope, receive, send)\nFile \"/layers/google.python.pip/pip/lib/python3.9/site-packages/starlette/applications.py\", line 112, in __call__\nawait self.middleware_stack(scope, receive, send)\nFile \"/layers/google.python.pip/pip/lib/python3.9/site-packages/starlette/middleware/errors.py\", line 181, in __call__\nraise exc\n File \"/layers/google.python.pip/pip/lib/python3.9/site-packages/starlette/middleware/errors.py\", line 159, in __call__\nawait self.app(scope, receive, _send)\nFile \"/layers/google.python.pip/pip/lib/python3.9/site-packages/starlette/exceptions.py\", line 82, in __call__\nraise exc\n File \"/layers/google.python.pip/pip/lib/python3.9/site-packages/starlette/exceptions.py\", line 71, in __call__\nawait self.app(scope, receive, sender)\nFile \"/layers/google.python.pip/pip/lib/python3.9/site-packages/starlette/routing.py\", line 656, in __call__\nawait route.handle(scope, receive, send)\nFile \"/layers/google.python.pip/pip/lib/python3.9/site-packages/starlette/routing.py\", line 259, in handle\nawait self.app(scope, receive, send)\nFile \"/layers/google.python.pip/pip/lib/python3.9/site-packages/starlette/routing.py\", line 61, in app\nresponse = await func(request)\n File \"/layers/google.python.pip/pip/lib/python3.9/site-packages/fastapi/routing.py\", line 226, in app\nraw_response = await run_endpoint_function(\nFile \"/layers/google.python.pip/pip/lib/python3.9/site-packages/fastapi/routing.py\", line 161, in run_endpoint_function\nreturn await run_in_threadpool(dependant.call, **values)\nFile \"/layers/google.python.pip/pip/lib/python3.9/site-packages/starlette/concurrency.py\", line 39, in run_in_threadpool\nreturn await anyio.to_thread.run_sync(func, *args)\nFile \"/layers/google.python.pip/pip/lib/python3.9/site-packages/anyio/to_thread.py\", line 28, in run_sync\nreturn await get_asynclib().run_sync_in_worker_thread(func, *args, cancellable=cancellable,\nFile \"/layers/google.python.pip/pip/lib/python3.9/site-packages/anyio/_backends/_asyncio.py\", line 805, in run_sync_in_worker_thread\nreturn await future\nFile \"/layers/google.python.pip/pip/lib/python3.9/site-packages/anyio/_backends/_asyncio.py\", line 743, in run\nresult = func(*args)\n File \"/workspace/./lorgs/routes/api.py\", line 45, in error\nraise ValueError(\"something went wrong!\")\nValueError: something went wrong!",
}



import base64
import json
from tasks import error_notify


data = json.dumps(PAYLOAD_1)
data = data.encode('utf-8')
data = base64.b64encode(data)

error_notify.send_message(
    event={
        "data": data
    }
)



