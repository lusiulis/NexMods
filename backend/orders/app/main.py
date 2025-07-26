from fastapi import FastAPI

app = FastAPI(title="Orders Service")  # cambia el título según servicio

@app.get("/")
async def root():
    return {"message": "Orders service is alive"}