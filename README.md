# Anas Hussain | Student ID: 23049

## PDC-Sp24-23049-Hussain
### Assignment: Building Resilient Distributed Systems
### Course: Parallel and Distributed Computing (PDC)

---

## Problem Solved
**Problem 3 — Fault Tolerance: Circuit Breaker Pattern**

When the external LLM API goes down, instead of blocking the entire
server, the Circuit Breaker detects repeated failures and instantly
returns a fallback response, keeping the app alive for all users.

---

## Project Structure
PDC-Sp24-23049-Hussain/
├── main.py                  # FastAPI app + middleware
├── circuit_breaker.py       # Circuit Breaker implementation
├── test_circuit_breaker.py  # All test cases
└── README.md                # This file

---

## How to Run

### 1. Clone the repo
```bash
git clone https://github.com/AnasHussain301/PDC-Sp24-23049-Hussain
cd PDC-Sp24-23049-Hussain
```

### 2. Create and activate virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install fastapi uvicorn httpx pytest requests
```

### 4. Start the server
```bash
uvicorn main:app --reload
```

### 5. Test the endpoints
```bash
# Health check
curl http://localhost:8000/health

# Ask LLM (returns fallback when LLM is down)
curl http://localhost:8000/ask

# Check circuit breaker status
curl http://localhost:8000/circuit-status
```

---

## How to Run Tests
```bash
pytest test_circuit_breaker.py -v
```

---

## How to Demo (Before and After)

### BEFORE — Server hangs without Circuit Breaker
```bash
# Terminal 1: simulate a slow unresponsive LLM
nc -l 9999

# Terminal 2: hit /ask — it will hang for 3 seconds then error
curl http://localhost:8000/ask
```

### AFTER — Circuit Breaker handles it gracefully
```bash
# Hit /ask 3 times — circuit opens after threshold
curl http://localhost:8000/ask  # failure 1
curl http://localhost:8000/ask  # failure 2
curl http://localhost:8000/ask  # failure 3 — circuit OPENS

# 4th call is instant — no hang, clean fallback
curl http://localhost:8000/ask

# Check the circuit state
curl http://localhost:8000/circuit-status
```

---

## Custom Header
Every single API response includes this header:
X-Student-ID: 23049

---

## Author
- **Name:** Anas Hussain
- **Student ID:** 23049
- **GitHub:** https://github.com/AnasHussain301
- **Course:** Parallel and Distributed Computing (PDC)
