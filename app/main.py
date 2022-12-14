import json
from typing import Any

import sentry_sdk
import uvicorn
from fastapi import FastAPI, Depends, Request
from fastapi.responses import JSONResponse

from app.depends import get_crt_user
from app.routes import router
from app import schemas

sentry_sdk.init(
    dsn="https://0303c01fe6244ed4a2bb56d9aa79646a@o1114395.ingest.sentry.io/4504328211398656",

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production,
    traces_sample_rate=1.0,
    _experiments={
        "profiles_sample_rate": 1.0,
      },
)


class DefaultResponse(JSONResponse):
    def render(self, content: Any) -> bytes:
        if content is None:
            content = schemas.DefaultSuccessSchema().dict()

        if isinstance(content, bytes):
            return content
        return json.dumps(content).encode(self.charset)


app = FastAPI(
    dependencies=[Depends(get_crt_user)],
    default_response_class=DefaultResponse,
    responses={
        418: {"model": schemas.DefaultExceptionSchema}
    }
)
app.include_router(router)


@app.exception_handler(Exception)
def base_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=418,
        content={
            "result": False,
            "error_type": str(type(exc)),
            "error_message": str(exc)
        },
    )


if __name__ == "__main__":
    uvicorn.run("main:app", port=8111, reload=True, debug=True)  # for debug
