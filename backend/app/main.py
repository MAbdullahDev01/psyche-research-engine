from fastapi import FastAPI
from app.api.webhooks.clerk import router as clerk_webhook_router
from app.core.cors import setup_cors

app = FastAPI(title="Psyche Research Engine", version="0.1.0")

@app.get("/")
def root():
    return {"message": "Welcome to the Psyche Research Engine API!"}

app.include_router(clerk_webhook_router)

setup_cors(app)