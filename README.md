# Custom Load Balancer - Distributed Systems Assignment

## Overview
This project implements a customizable load balancer using **consistent hashing**. It manages backend server replicas using Docker containers, supports dynamic scaling, and handles server failures through heartbeat checks and fault recovery. It also exposes a simple REST API to interact with the system.

## Technologies Used
- **Python 3.9**
- **Flask** – For server and load balancer development
- **Docker & Docker Compose** – For containerization and orchestration
- **Consistent Hashing with Virtual Servers** – For efficient and scalable load distribution

## Tasks Completed

### ✅ Task 1: Server Implementation
- Created a simple Flask server with the following endpoints:
  - `/home`: Returns the server ID in JSON format.
  - `/heartbeat`: Returns 200 OK for health checks.
- Dockerized the server using a custom `Dockerfile`.

### ✅ Task 2: Consistent Hashing
- Implemented a consistent hashing ring with:
  - **512 total slots**
  - **9 virtual nodes per physical server**
- Hash functions used:
  - `H(i) = i + 2i + 17`
  - `Φ(i, j) = i + j + 2j + 25`
- Used **linear probing** to resolve slot conflicts in the hash ring.

### ✅ Task 3: Load Balancer
- Built a Flask-based load balancer with the following features:
  - Routes incoming requests to backend replicas using consistent hashing.
  - Monitors server health using heartbeat checks.
  - Supports dynamic addition and removal of replicas.
- Implemented the following endpoints:
  - `GET /rep` – Returns the list of current replica servers.
  - `POST /add` – Adds a new replica server.
  - `POST /rm` – Removes a replica server (specified or random).
  - `GET /<path>` – Forwards requests to the appropriate server.

### ✅ Task 4: Performance Analysis
- **A-1:** Launched **10,000 asynchronous requests** to the load balancer with **N = 3** replicas. Logged server hits and plotted a bar chart to analyze distribution.
- **A-2:** Varied `N` from **2 to 6** and measured the average load per server.
- **A-3:** Removed a server during runtime and verified that the load balancer rerouted requests without crashing.
- **A-4:** Modified the hash functions and observed the impact on distribution and system behavior.

## How to Run

### Build and Start Containers
```bash
make build     # Build Docker images
make up        # Start load balancer and server containers
![building the server](tests/Screenshot%20from%202025-06-19%2015-21-21.png)
![building the server](tests/Screenshot%20from%202025-06-19%2015-21-35.png)
![starting up](tests/Screenshot%20from%202025-06-19%2015-24-59.png)