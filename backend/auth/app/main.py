from fastapi import FastAPI

app = FastAPI(title="Auth Service")  # cambia el título según servicio

@app.get("/")
async def root():
    return {"message": "Auth service is alive"}