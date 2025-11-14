from fastapi import FastAPI
from routes import items
app = FastAPI()

app = FastAPI(title="Custom Backend Ops TEST", version="0.1.0")


# registrar routers modulares
app.include_router(items.router, prefix="/items", tags=["items"])

@app.get("/")
def root():
    return {"message": "Hello, Worldi!"}