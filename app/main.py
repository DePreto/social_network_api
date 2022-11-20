import json
from typing import Any

import uvicorn
from fastapi import FastAPI, Depends, Response

from app.depends import get_crt_user
from app.routes import router


class DefaultResponse(Response):
    media_type = "application/json"

    def render(self, content: Any) -> bytes:
        if content is None:
            content = {
                "result": True,
            }

        if isinstance(content, bytes):
            return content
        return json.dumps(content).encode(self.charset)


app = FastAPI(dependencies=[Depends(get_crt_user)], default_response_class=DefaultResponse)
app.include_router(router)


if __name__ == "__main__":
    uvicorn.run("main:app", port=8111, reload=True, debug=True)  # for debug
