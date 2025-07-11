<p align="center">
  <img src="https://img.shields.io/badge/Python-3.9-blue.svg" alt="Python 3.9"/>
  <img src="https://img.shields.io/badge/Flask-2.x-orange.svg" alt="Flask"/>
  <img src="https://img.shields.io/badge/Docker–Compose-blue.svg" alt="Docker Compose"/>
  <img src="https://img.shields.io/badge/Version-1.0.0-brightgreen.svg" alt="Version"/>
</p>

# 📡 Custom Load Balancer

A production-ready, Flask-based load balancer leveraging **consistent hashing** for distributed traffic management, dynamic scaling, and fault tolerance.

---

<<<<<<< Updated upstream
## 📝 Purpose & Background

In distributed systems, evenly distributing client requests across backend servers—and quickly recovering from node failures—is crucial for performance and availability. This project demonstrates how to build a **high-availability**, **scalable** load-balancing solution that:

* Uses **consistent hashing** (with virtual nodes) to minimize key remapping when servers join or leave.
* Provides **heartbeat monitoring** to detect unhealthy replicas and reroute traffic automatically.
* Exposes a simple **REST API** for operational control (add/remove replicas, list servers, proxy requests).
* Runs entirely in **Docker** containers for easy deployment & orchestration.

---
=======
### Task 1: Server Implementation
- Created a simple Flask server with the following endpoints:
  - `/home`: Returns the server ID in JSON format.
  - `/heartbeat`: Returns 200 OK for health checks.
- Dockerized the server using a custom `Dockerfile`.

### Task 2: Consistent Hashing
- Implemented a consistent hashing ring with:
  - **512 total slots**
  - **9 virtual nodes per physical server**
- Hash functions used:
  - `H(i) = i + 2i + 17`
  - `Φ(i, j) = i + j + 2j + 25`
- Used **linear probing** to resolve slot conflicts in the hash ring.

### Task 3: Load Balancer
- Built a Flask-based load balancer with the following features:
  - Routes incoming requests to backend replicas using consistent hashing.
  - Monitors server health using heartbeat checks.
  - Supports dynamic addition and removal of replicas.
- Implemented the following endpoints:
  - `GET /rep` – Returns the list of current replica servers.
  - `POST /add` – Adds a new replica server.
  - `POST /rm` – Removes a replica server (specified or random).
  - `GET /<path>` – Forwards requests to the appropriate server.

### Task 4: Performance Analysis
- **A-1:** Launched **10,000 asynchronous requests** to the load balancer with **N = 3** replicas. Logged server hits and plotted a bar chart to analyze distribution.
- **A-2:** Varied `N` from **2 to 6** and measured the average load per server.
- **A-3:** Removed a server during runtime and verified that the load balancer rerouted requests without crashing.
- **A-4:** Modified the hash functions and observed the impact on distribution and system behavior.
>>>>>>> Stashed changes

## ✨ Features

* **Dynamic Scaling**
  Add or remove replicas at runtime via REST API
* **Fault Tolerance**
  Automatic health checks & rerouting on failure
* **Consistent Hashing**

  * 512 slots in the ring
  * 9 virtual nodes per physical server
  * Custom hash functions & linear probing
* **RESTful Control API**
  Manage replicas and proxy traffic with simple endpoints
* **Performance Benchmarks**
  Scripts & charts to visualize load distribution

---

## 🛠 Technologies & Dependencies

* **Language:** Python 3.9
* **Web Framework:** Flask
* **Containerization:** Docker Engine & Docker Compose
* **Utilities:** Make (optional), curl
* **Libraries:** `requests`, `flask`

---

## 📋 Prerequisites

1. **Docker Engine** ≥ 20.10
2. **Docker Compose** (plugin or standalone)
3. **Make** (optional, for convenient scripts)
4. **curl** (for testing endpoints)
5. **git** (to clone the repository)

---

## ⚙️ Installation & Setup

1. **Clone the repository**

   ```bash
   git clone https://github.com/your-org/Distributed_Systems_2.git
   cd Distributed_Systems_2
   ```

2. **Build Docker images**

   ```bash
   make build
   ```

   *Or, without Make:*

   ```bash
   docker-compose build
   ```

3. **Start the stack**

   ```bash
   make up
   ```

   *Or, without Make:*

   ```bash
   docker-compose up -d --scale server=3
   ```

4. **Verify containers are running**

   ```bash
   docker ps
   curl http://localhost:5000/home   # → {"id":"<server-uuid>"}
   ```

5. **Shut down the stack**

   ```bash
   make down
   ```

   *Or:*

   ```bash
   docker-compose down
   ```

---

## ▶️ Usage & API Reference

| Endpoint      | Method | Description                              |
| ------------- | ------ | ---------------------------------------- |
| `/rep`        | GET    | List all active replica server addresses |
| `/add`        | POST   | Spin up a new replica                    |
| `/rm`         | POST   | Remove a replica (specific or random)    |
| `/<any_path>` | GET    | Proxy request to the appropriate replica |

```bash
# List current replicas
curl http://localhost:5000/rep

# Add a replica
curl -X POST http://localhost:5000/add

# Remove a replica
curl -X POST http://localhost:5000/rm

# Proxy any path (e.g., /home)
curl http://localhost:5000/home
```

---

## 📊 Performance Analysis

All benchmarking scripts live under the `tests/` directory:

1. **A-1:** 10 000 asynchronous requests (N=3) → bar chart of hits per server
2. **A-2:** Vary replica count N from 2→6 → average load metrics
3. **A-3:** Runtime removal test → validate zero downtime
4. **A-4:** Hash function experiments → compare distribution effects

> **Tip:**
> Run `python3 tests/performance_test.py` or open the Jupyter notebooks in `tests/` for interactive charts.

---

## 🔧 Configuration

* **Ports:**

  * Load Balancer: `5000`
  * Backends: assigned dynamically by Compose

* **Replica Count:**
  Adjust `--scale server=<N>` in the `make up` command or in `docker-compose.yml`.

* **Hash Ring Settings:**
  Modify the `RING_SIZE` and `VNODE_COUNT` constants in `load_balancer.py`.

---

## 🐞 Troubleshooting

* **“permission denied” on `/var/run/docker.sock`**

  ```bash
  sudo usermod -aG docker $USER && exit
  # Log out and back in
  ```

* **Docker daemon not running**

  ```bash
  sudo systemctl start docker
  ```

* **Compose version warning**
  Remove the top-level `version:` key from `docker-compose.yml`.

---


