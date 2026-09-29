from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.analyze import router as analyze_router


app = FastAPI(
    title="AI Resume Intelligence API",
    description="AI-powered resume evaluation and job matching platform",
    version="1.0.0",
)


# ==================================================
# CORS
# ==================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==================================================
# ROUTES
# ==================================================

app.include_router(analyze_router)


@app.get("/")
def root():
    return {
        "message": "AI Resume Intelligence API is running",
        "status": "success",
        "version": "1.0.0",
    }


@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "service": "resume-evaluator",
    }