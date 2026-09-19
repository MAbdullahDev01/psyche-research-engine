from fastapi import FastAPI
from app.api.webhooks.clerk import router as clerk_webhook_router

app = FastAPI(title="Psyche Research Engine", version="0.1.0")

@app.get("/")
def root():
    return {"message": "Welcome to the Psyche Research Engine API!"}

app.include_router(clerk_webhook_router)