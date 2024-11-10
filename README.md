# Monitoring Quote Application with Prometheus and Grafana

## Installing Quote App, Grafana and Prometheus using Docker

In order to dockerize the Quote application, create the following files:
- **Dockerfile**: Describes the applications environment
- **requirements.txt**: Lists all applications dependencies
- **docker-compose.yml**: Used to run multi-container applications (services)
- **quote-app-network**: A custom bridge network, which ensures all services can communicate with each other

Directory structure:
```sh
quotes_app/
├── app.py
├── templates/
│   └── index.html
├── static/
│   └── # list of images
├── Dockerfile
├── requirements.txt
├── docker-compose.yml
└── prometheus/
    └── prometheus.yml
```

Create `quote-app` image before starting `docker compose` command:
```sh
$ docker build -t quote-app:latest .
```

In `docker-compose.yml` file use the following:
```yml
services:
  quote-app:
    image: quote-app:latest
```

Create `quote-app` image with `docker compose` command.
In `docker-compose.yml` file use the following:
```yml
services:
  quote-app:
    build: .
```

Run the following command:
```sh
$ docker compose up -d --build
```

Accessing the service:
- Quote application: `http://localhost:5000`
- Prometheus: `http://localhost:9090`
- Grafana: `http://localhost:3000`

### Troubleshooting Steps when installing using Docker Compose

If there are problems with connection between components, here are some steps that can be done to troubleshoot existing problems.

**Test Connectivity with Prometheus**

From Prometheus container, try pinging the Quote application services:
```sh
$ docker exec -it prometheus ping quote-app
```

Also, try curling the /metrics endpoint to ensure it's accessible:
```sh
$ docker exec -it prometheus curl http://quote-app:5000/metrics
```

**Check Docker container logs**

Use the following commands to check the logs of all containers:
```sh
$ docker-compose logs quote-app
$ docker-compose logs prometheus
```

Look for any errors related to connection issues, such as "connection refused," "host unreachable," or "service not found."

**Check service ports**

Confirm that the services are listening on the expected ports:
```sh
$ docker exec -it quote-app netstat -tuln
```

## Monitoring Quote Application

Monitoring application is a simple Flask application that displays famous quotes (along with author's name and image).
Application exposes multiple endpoints, such as `/health`  which is used to report the application's health and `\metrics` endpoint which exposes all application-specific metrics in a format that Prometheus can scrape. The application also collects and exposes metrics related to system resources, such as CPU and memory usage.

### Starting Application

Ensure all dependencies are installed:
```sh
$ pip3 install -r requirements.txt
```

Start the Flask application using:
```sh
$ python3 app.py
```

Application will run on `http://localhost:5000`, which serves as the main entry point to the application.
The following endpoints are also available:
- `http://localhost:5000/health` returns the current health status of the application.
- `http://localhost:5000/metrics` exposes all the collected metrics in a format compatible with Prometheus.

### Exposed Endpoints

The following endpoints are available:

**Home Endpoint** (`/`)

- This is the main entry point of the application. When accessed, it serves an HTML page that displays a random quote. The user can click on the displayed quote to view the next one in the sequence.

**Health Check Endpoint** (`/health`)

- This endpoint returns the current health status of the application. It always responds with a status of "healthy", along with a metric `HEALTH_STATUS` set to 1, indicating that the application is running as expected.

**Metrics Endpoint** (`/metrics`)

- This endpoint exposes all the collected metrics in a format compatible with Prometheus. Metrics include request counts, request latency, error counts, CPU and memory usage, uptime, and various others related to the application's performance and resource consumption.

**Next Quote Endpoint** (`/next_quote/<int:index>`)

- This endpoint returns the next quote in the sequence based on the provided index. Each time a quote is retrieved, the corresponding counter for that quote is incremented.

### Metrics Explanation

Description of all the metrics used in the Flask application, detailing what each metric tracks and its purpose.

**Total Request Count** (`REQUEST_COUNT`)
- Tracks the total number of requests received by the application. This metric increments every time an endpoint is accessed.

**Total Error Count** (`ERROR_COUNT`)
- Tracks the total number of errors that occur within the application. Each time an error is encountered, this counter is incremented.

**Application Health Status** (`HEALTH_STATUS`)
- Represents the health status of the application. This metric can be set to 1 for healthy and 0 for unhealthy.

**CPU Usage Percent** (`CPU_USAGE`)
- Tracks the percentage of CPU being utilized by the application.

**Memory Usage Percent** (`MEMORY_USAGE`)
- Tracks the percentage of memory being utilized by the application.

**Memory Usage in MB** (`MEMORY_USAGE_MB`)
- Tracks the memory usage of the application in megabytes.

**Application Uptime** (`APP_UPTIME`)
- Tracks the total time (in seconds) that the application has been running since the last restart.

**Total Quotes Displayed** (`TOTAL_QUOTES_DISPLAYED`)
- Tracks the total number of quotes that have been displayed on the home page. Each time a quote is shown, this counter increments.

**Successful Requests** (`SUCCESSFUL_REQUESTS`)
- Tracks the number of successful requests made to the `/process` endpoint.

**Individual Quote Display Count** (`quote_<index>_count`)
- Tracks the number of times each specific quote has been displayed. There is a counter for each quote, incremented whenever that quote is displayed.
