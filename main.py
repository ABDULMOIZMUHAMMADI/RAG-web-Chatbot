from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from auth_routes import router as auth_router
from chat_routes import router as chat_router
from website_routes import router as web_router
from database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()
@app.get("/")
def root():
    return {"status": "ok", "message": "Backend is running!"}

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allow all for local dev/Space compatibility
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(web_router)
app.include_router(chat_router)