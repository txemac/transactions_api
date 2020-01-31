from fastapi import FastAPI
from starlette.status import HTTP_200_OK

app = FastAPI()


@app.get("/_check", status_code=HTTP_200_OK)
def read_root():
    return dict(
        message='OK'
    )
