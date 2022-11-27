import json
from typing import Any

import uvicorn
from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse

from app.depends import get_crt_user
from app.routes import router
from app import schemas


class DefaultResponse(JSONResponse):
    def render(self, content: Any) -> bytes:
        if content is None:
            content = schemas.DefaultSchema().dict()

        if isinstance(content, bytes):
            return content
        return json.dumps(content).encode(self.charset)


app = FastAPI(dependencies=[Depends(get_crt_user)], default_response_class=DefaultResponse)
app.include_router(router)


if __name__ == "__main__":
    uvicorn.run("main:app", port=8111, reload=True, debug=True)  # for debug
