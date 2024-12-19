from multiprocessing import Process

from fastapi import FastAPI
import uvicorn

from consumer import start_consumer
from routes import router


def run_consumer():
    process = Process(target=start_consumer)
    process.start()
    return process


app = FastAPI()
app.include_router(router)


if __name__ == "__main__":
    consumer_process = run_consumer()

    try:
        app = FastAPI()
        app.include_router(router)

        uvicorn.run(app, host="0.0.0.0", port=8003)

    finally:
        if consumer_process.is_alive():
            consumer_process.terminate()
            consumer_process.join()
