from fastapi import FastAPI
from app.routes.auth_routes import router as auth_router
from app.routes.business_routes import router as business_router
from app.routes.review_routes import router as review_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(business_router)
app.include_router(review_router)

@app.get("/health")
async def health_check():
    return {"status": "healthy"}