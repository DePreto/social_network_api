from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def first_root():
    return {"Hello": "World"}
