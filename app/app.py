from flask import Flask, jsonify, render_template
import socket
import datetime
import psutil
import os

app = Flask(__name__)

# -------------------------------
# Helper function to get metrics
# -------------------------------
def get_system_metrics():
    return {
        "cpu_usage": psutil.cpu_percent(interval=1),
        "memory_usage": psutil.virtual_memory().percent,
        "disk_usage": psutil.disk_usage('/').percent,
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

# -------------------------------
# Security headers (DevSecOps)
# -------------------------------
@app.after_request
def add_security_headers(response):
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=63072000; includeSubDomains"
    response.headers["Content-Security-Policy"] = "default-src 'self'"
    return response

# -------------------------------
# Dashboard Route
# -------------------------------
app_env = os.getenv("APP_ENV", "development")
app_version = os.getenv("APP_VERSION", "1.0")

@app.route("/")
def dashboard():
    metrics = get_system_metrics()
    hostname = socket.gethostname()
    current_time = datetime.datetime.now()

    return render_template(
     "dashboard.html",
     metrics=metrics,
     hostname=hostname,
     current_time=current_time,
     app_env=app_env,
     app_version=app_version
     )
# -------------------------------
# JSON Metrics API (for monitoring tools)
# -------------------------------
@app.route("/metrics")
def metrics():
    return jsonify(get_system_metrics())

# -------------------------------
# Health Check Endpoint
# -------------------------------
@app.route("/health")
def health():
    return jsonify({
        "status": "healthy",
        "service": "devsecops-dashboard",
        "time": datetime.datetime.utcnow().isoformat()
    }), 200

# -------------------------------
# Entry point for local run
# (Gunicorn will ignore this)
# -------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)