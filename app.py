from flask import Flask, render_template, jsonify
from prometheus_client import Counter, Gauge, generate_latest
import time
import psutil

app = Flask(__name__)

# Prometheus Metrics
REQUEST_COUNT = Counter('app_request_count', 'Total number of requests')
ERROR_COUNT = Counter('app_error_count', 'Total number of errors')
HEALTH_STATUS = Gauge('app_health_status', 'Application health status')
CPU_USAGE = Gauge('app_cpu_usage_percent', 'CPU usage percent')
MEMORY_USAGE = Gauge('app_memory_usage_percent', 'Memory usage percent')
MEMORY_USAGE_MB = Gauge('app_memory_usage_mb', 'Memory usage in MB')
APP_UPTIME = Gauge('app_uptime_seconds', 'Application uptime in seconds')
TOTAL_QUOTES_DISPLAYED = Counter('app_total_quotes_displayed', 'Total number of quotes displayed')
SUCCESSFUL_REQUESTS = Counter('app_successful_requests', 'Total number of successful requests')

quote_counters = [
    Counter(f'quote_{i+1}_count', f'Number of times quote {i+1} was displayed')
    for i in range(15)
]

start_time = time.time()

@app.route('/')
def home():
    REQUEST_COUNT.inc()
    return render_template('index.html')

@app.route('/quote/<int:index>')
def increment_quote_counter(index):
    if 1 <= index <= len(quote_counters):
        quote_counters[index - 1].inc()
        TOTAL_QUOTES_DISPLAYED.inc()
        SUCCESSFUL_REQUESTS.inc()
        return jsonify({"message": "Quote counter incremented"}), 200
    return jsonify({"error": "Quote with that index does not exists!"}), 400

@app.route('/metrics')
def metrics():
    CPU_USAGE.set(psutil.cpu_percent())
    MEMORY_USAGE.set(psutil.virtual_memory().percent)
    MEMORY_USAGE_MB.set(psutil.virtual_memory().used / 1024 / 1024)
    APP_UPTIME.set(time.time() - start_time)
    return generate_latest()

@app.route('/error')
def error():
    REQUEST_COUNT.inc()
    ERROR_COUNT.inc()
    return jsonify({"error": "An intentional error occurred!"}), 500

@app.route('/health')
def health():
    HEALTH_STATUS.set(1)
    return jsonify({"status": "System is healthy."})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
