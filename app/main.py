from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api import auth, ai, taxes

app = FastAPI(
    title="AI BUXGALTER API",
    description="Enterprise-level automated accounting system for Uzbekistan",
    version="1.0.0"
)

# Set all CORS enabled origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(auth.router)
app.include_router(ai.router)
app.include_router(taxes.router)

@app.get("/")
async def root():
    return {"message": "Welcome to AI BUXGALTER API", "status": "running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
