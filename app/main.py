from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from app.database.session import engine
from app.models.base import Base
from app.api import main_router as main_router
import os

# Get the current directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

@asynccontextmanager
async def lifespan(app: FastAPI):
    # тут начало работы sql
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # тут остановочка
    await engine.dispose()

app = FastAPI(lifespan=lifespan, debug=True)

# Mount static files
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")

# Configure templates
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

# Include the main router
app.include_router(main_router)

@app.get("/login")
async def login_page(request: Request):
    return templates.TemplateResponse(
        "authorisation/authorization_form.html",
        {"request": request}
    )

@app.get("/register")
async def register_page(request: Request):
    return templates.TemplateResponse(
        "authorisation/registration_form.html",
        {"request": request}
    )
