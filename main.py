from fastapi import FastAPI
from routes import items
app = FastAPI()

app = FastAPI(title="Custom Backend Ops")


# registrar routers modulares
app.include_router(items.router, prefix="/items", tags=["items"])

@app.get("/")
def root():
    return {"message": "Hello, Worldi!"}