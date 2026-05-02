import time

class CircuitBreaker:
    def __init__(self, failure_threshold=3, recovery_timeout=15):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.failure_count = 0
        self.last_failure_time = None
        self.state = "CLOSED"  # CLOSED, OPEN, HALF_OPEN

    def call(self, func, *args, **kwargs):
        # If OPEN, check if recovery time has passed
        if self.state == "OPEN":
            time_since_failure = time.time() - self.last_failure_time
            if time_since_failure > self.recovery_timeout:
                print("[CircuitBreaker] Switching to HALF_OPEN — testing recovery...")
                self.state = "HALF_OPEN"
            else:
                remaining = int(self.recovery_timeout - time_since_failure)
                raise Exception(f"Circuit is OPEN. Retry in {remaining}s.")

        # Try calling the function
        try:
            result = func(*args, **kwargs)
            self._on_success()
            return result
        except Exception as e:
            self._on_failure()
            raise e

    def _on_success(self):
        print(f"[CircuitBreaker] Call succeeded. Resetting to CLOSED.")
        self.failure_count = 0
        self.last_failure_time = None
        self.state = "CLOSED"

    def _on_failure(self):
        self.failure_count += 1
        self.last_failure_time = time.time()
        print(f"[CircuitBreaker] Failure #{self.failure_count}")
        if self.failure_count >= self.failure_threshold:
            self.state = "OPEN"
            print(f"[CircuitBreaker] Threshold reached! Switching to OPEN.")

    def get_status(self):
        return {
            "state": self.state,
            "failure_count": self.failure_count,
            "threshold": self.failure_threshold,
        }