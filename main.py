from fastapi import FastAPI
from routes.health import router as health_router
from routes.process_email import router as processemail_router
app= FastAPI()

app.include_router(health_router)
app.include_router(processemail_router)
@app.get('/')

def get_data():
    return ("hello world")