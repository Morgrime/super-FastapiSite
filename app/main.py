from fastapi import FastAPI
from uvicorn import run
from routers.index import router as routing_router



app = FastAPI()
app.include_router(routing_router)



if __name__ == "__main__":
    run(app)