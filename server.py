from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
import uvicorn
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI()

# Health check endpoint
@app.get("/")
async def root():
    return {"status": "ok", "message": "BATL N1 Bot is running"}

# Keep-alive endpoint
@app.get("/keepalive")
async def keep_alive():
    return {"status": "alive"}

# Webhook endpoint for Telegram
@app.post("/webhook")
async def webhook(request: Request):
    # Here you can add your webhook handling logic
    # For now, it just returns a 200 OK response
    return {"status": "webhook received"}

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("server:app", host="0.0.0.0", port=port, reload=True)
