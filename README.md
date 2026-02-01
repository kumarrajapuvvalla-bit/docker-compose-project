# Docker Compose Demo

This project illustrates how to use **Docker Compose** to orchestrate a
multi‑container application consisting of a web service and a
PostgreSQL database.  The web service is built with Python and Flask
and exposes endpoints to create and list messages stored in the
database.  Compose handles container networking, environment
variables, volumes, and health‑checks automatically.

## Architecture

* `web` – a Python Flask application (`web/app.py`) that connects to
  PostgreSQL using the `psycopg2` driver.  It exposes the following
  endpoints:
  * `POST /messages` – insert a message into the database.
  * `GET /messages` – list all messages.
  * `GET /health` – return a simple status check.
* `db` – an official `postgres` container initialised with a `messages`
  database.  At startup it runs `db/init.sql` to create the table.
* `docker-compose.yml` – defines both services, their dependencies,
  environment variables, volumes for persistent storage, and a custom
  network.

## Getting Started

### Prerequisites

* **Docker Desktop** or Docker Engine with Compose support.
* **Python 3.9** (optional) if you want to run the web service on its
  own.

### Running with Docker Compose

1. From the root of this project, build and start the services:

   ```bash
   docker-compose up --build
   ```

2. Once the containers are up, you can interact with the API:

   ```bash
   # Add a message
   curl -X POST -H "Content-Type: application/json" \
        -d '{"text": "Hello Compose"}' http://localhost:5000/messages

   # List messages
   curl http://localhost:5000/messages
   ```

3. To stop and remove the containers, press `Ctrl+C` and run:

   ```bash
   docker-compose down
   ```

### Running Locally Without Compose

If you prefer to run the application outside of Docker, install the
dependencies and point the app at a running PostgreSQL instance:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r web/requirements.txt
export POSTGRES_HOST=localhost
export POSTGRES_DB=messages
export POSTGRES_USER=user
export POSTGRES_PASSWORD=pass
python web/app.py
```

## Extending This Project

This Compose setup can serve as a foundation for more complex
microservice environments.  Ideas for extensions:

* Add another service (for example a React or Angular front‑end) that
  communicates with the API.
* Introduce a third container such as a message broker (RabbitMQ or
  Kafka) to illustrate asynchronous processing.
* Use environment variables and `.env` files to separate development
  and production configurations.
* Add health checks (`healthcheck` directive) and restart policies to
  improve resiliency.
* Deploy the Compose stack to a cloud environment using a tool like
  Docker Swarm or by converting it into Kubernetes manifests with
  `kompose`.

Through this project you demonstrate your ability to containerise
applications, orchestrate dependencies, and manage data persistence.
