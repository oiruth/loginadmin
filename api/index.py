from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import json
import random
import string
from datetime import datetime, timedelta
import os
import requests

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

KEYS_FILE = 'keys.json'
BOT_TOKEN = '7950073092:AAGIF-CiHHFG79wiCpsw-xnQRXiPllrKCTs'
CHAT_ID = '5650303115'

def generate_key():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=16))

def load_keys():
    try:
        with open(KEYS_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_keys(keys):
    with open(KEYS_FILE, 'w') as f:
        json.dump(keys, f, indent=4)

@app.get("/")
def read_root():
    return {"message": "API is running"}

@app.post("/generate_key")
def generate_key_api(validity_days: int):
    expiration_date = datetime.now() + timedelta(days=validity_days)
    expiration_str = expiration_date.strftime('%d/%m/%Y')

    new_key = generate_key()
    keys = load_keys()

    keys.append({
        'key': new_key,
        'created_at': datetime.now().strftime('%d/%m/%Y %H:%M:%S'),
        'expires_at': expiration_str
    })

    save_keys(keys)
    return {"message": "Key generated successfully", "key": new_key, "expires_at": expiration_str}

@app.get("/get_keys")
def get_keys():
    return load_keys()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
