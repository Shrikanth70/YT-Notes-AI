# Application Entry Point - Reload Triggered
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.api import api_router
from app.core.config import settings


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    openapi_url=f"/api/v1/openapi.json"
)


@app.on_event("startup")
async def startup_event():
    print("🚀 Starting AI YouTube Notes Generator API")
    print(f"🔧 Active OpenRouter Models: {settings.OPENROUTER_MODELS}")
    print(f"✅ Primary Model: {settings.OPENROUTER_MODELS[0] if settings.OPENROUTER_MODELS else 'None'}")


# Set all CORS enabled origins
origins = [
    "http://localhost:5173",
    "https://yt-notes-ai-tan.vercel.app",
]

# CORSMiddleware must be the FIRST middleware added to ensure CORS headers
# are added to ALL responses, including those from other middlewares or errors.
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

@app.middleware("http")
async def log_requests(request, call_next):
    import time
    start_time = time.time()
    try:
        response = await call_next(request)
        process_time = time.time() - start_time
        print(f"INFO: {request.method} {request.url.path} - {response.status_code} ({process_time:.4f}s)")
        return response
    except Exception as e:
        import traceback
        process_time = time.time() - start_time
        print(f"ERROR: {request.method} {request.url.path} - 500 Internal Server Error ({process_time:.4f}s)")
        traceback.print_exc()
        from fastapi.responses import JSONResponse
        return JSONResponse(
            status_code=500,
            content={
                "detail": "Internal Server Error",
                "error": str(e),
                "type": type(e).__name__
            }
        )


@app.get("/api/v1/health")
def health_check():
    return {"status": "ok", "version": settings.APP_VERSION}


app.include_router(api_router, prefix="/api/v1")
