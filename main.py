import httpx
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from circuit_breaker import CircuitBreaker

app = FastAPI()

# ✅ REQUIRED: Custom Middleware Header — X-Student-ID
@app.middleware("http")
async def add_student_id_header(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Student-ID"] = "23049"
    return response

# One shared Circuit Breaker instance
cb = CircuitBreaker(failure_threshold=3, recovery_timeout=15)

# ─────────────────────────────────────────
# Simulated LLM call (points to fake server)
# ─────────────────────────────────────────
def call_llm():
    print("[LLM] Attempting to call LLM API...")
    # This will fail when fake server is down
    response = httpx.get("http://localhost:9999/generate", timeout=3.0)
    response.raise_for_status()
    return response.text

# ─────────────────────────────────────────
# Routes
# ─────────────────────────────────────────

@app.get("/ask")
def ask_llm():
    """Main endpoint — calls LLM through Circuit Breaker"""
    try:
        result = cb.call(call_llm)
        return JSONResponse({"status": "success", "response": result})
    except Exception as e:
        return JSONResponse({
            "status": "fallback",
            "response": "AI features are temporarily unavailable. Please try again later.",
            "reason": str(e)
        })

@app.get("/circuit-status")
def circuit_status():
    """See the current state of the Circuit Breaker"""
    return JSONResponse(cb.get_status())

@app.get("/health")
def health():
    """Basic health check"""
    return {"status": "ok", "service": "StudySync API"}
