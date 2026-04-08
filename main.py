from fastapi import FastAPI
from routers import bonds

app = FastAPI(title="Bond Analytics API")

app.include_router(bonds.router)

@app.get("/health")
def health_check():
    return {"status": "ok"}