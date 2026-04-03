from fastapi import FastAPI
from auth_routes import router as auth_router
from chat_routes import router as chat_router
from website_routes import router as web_router
from database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth_router)
app.include_router(web_router)
app.include_router(chat_router)