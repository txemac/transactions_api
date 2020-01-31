from fastapi import FastAPI

app = FastAPI()


@app.get('/_check', status_code=200)
def get_check():
    return dict(
        message='OK'
    )
