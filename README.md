<p align="center">
  <img src="https://img.shields.io/badge/Python-3.9-blue.svg" alt="Python 3.9"/>
  <img src="https://img.shields.io/badge/Flask-2.x-orange.svg" alt="Flask"/>
  <img src="https://img.shields.io/badge/Docker–Compose-blue.svg" alt="Docker Compose"/>
  <img src="https://img.shields.io/badge/Version-1.0.0-brightgreen.svg" alt="Version"/>
</p>

# 📡 Custom Load Balancer

A production-ready, Flask-based load balancer leveraging **consistent hashing** for distributed traffic management, dynamic scaling, and fault tolerance.

---

## 📝 Purpose & Background

In distributed systems, evenly distributing client requests across backend servers—and quickly recovering from node failures—is crucial for performance and availability. This project demonstrates how to build a **high-availability**, **scalable** load-balancing solution that:

* Uses **consistent hashing** (with virtual nodes) to minimize key remapping when servers join or leave.
* Provides **heartbeat monitoring** to detect unhealthy replicas and reroute traffic automatically.
* Exposes a simple **REST API** for operational control (add/remove replicas, list servers, proxy requests).
* Runs entirely in **Docker** containers for easy deployment & orchestration.

---

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

## 🤝 Contributing

1. Fork the repo
2. Create a branch:

   ```bash
   git checkout -b feature/your-feature
   ```
3. Commit your changes:

   ```bash
   git commit -m "Add awesome feature"
   ```
4. Push to your branch:

   ```bash
   git push origin feature/your-feature
   ```
5. Open a Pull Request

Please ensure tests and linting pass and update docs as needed.
