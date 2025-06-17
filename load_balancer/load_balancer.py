from flask import Flask, request, jsonify
import hashlib, random, string, subprocess, os

app = Flask(__name__)
N = 3
M = 512
K = 9
servers = {}  # server_id: hostname
hash_ring = {}
sorted_keys = []

# Utilities
def hash_request(req_id):
    return (req_id + 2 * req_id + 17) % M

def hash_virtual(i, j):
    return (i + j + 2 * j + 25) % M
def safe_insert(hash_ring, key, value):
    original_key = key
    while key in hash_ring:
        key = (key + 1) % M  # linear probing
        if key == original_key:
            raise Exception("Hash ring full!")
   # print(f"Inserted {value} at slot {key}")
    hash_ring[key] = value

def update_ring():
    global hash_ring, sorted_keys
    hash_ring = {}
    for sid, hostname in servers.items():
        for j in range(K):
            key = hash_virtual(sid, j)
            safe_insert(hash_ring, key, hostname)
    sorted_keys = sorted(hash_ring)
    

def get_target_server(req_id):
    h = hash_request(req_id)
    for key in sorted_keys:
        if h <= key:
            return hash_ring[key]
    return hash_ring[sorted_keys[0]]

def generate_id():
    return max(servers.keys(), default=0) + 1

def generate_hostname():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))

def spawn_container(hostname, sid):
    cmd = [
        "docker", "run", "-d", "--name", hostname,
        "--network", "net1", "--network-alias", hostname,
        "-e", f"SERVER_ID={sid}", "server-image"
    ]
    subprocess.run(cmd)

def remove_container(hostname):
    subprocess.run(["docker", "rm", "-f", hostname])

# API Endpoints

@app.route("/rep", methods=["GET"])
def get_replicas():
    return jsonify({"message": {"N": len(servers), "replicas": list(servers.values())}, "status": "successful"}), 200

@app.route("/add", methods=["POST"])
def add_servers():
    data = request.json
    n = data.get("n")
    names = data.get("hostnames", [])
    if len(names) > n:
        return jsonify({"message": "<Error> Length of hostname list is more than newly added instances", "status": "failure"}), 400
    for i in range(n):
        sid = generate_id()
        hostname = names[i] if i < len(names) else generate_hostname()
        spawn_container(hostname, sid)
        servers[sid] = hostname
    update_ring()
    return get_replicas()

@app.route("/rm", methods=["DELETE"])
def remove_servers():
    data = request.json
    n = data.get("n")
    names = data.get("hostnames", [])
    if len(names) > n:
        return jsonify({"message": "<Error> Length of hostname list is more than removable instances", "status": "failure"}), 400

    to_remove = list(servers.items())
    removed = []
    for sid, hostname in to_remove:
        if hostname in names or (len(removed) < n and hostname not in removed):
            remove_container(hostname)
            removed.append(hostname)
            del servers[sid]
        if len(removed) >= n:
            break

    update_ring()
    return get_replicas()

@app.route("/<path:endpoint>", methods=["GET"])
def route_request(endpoint):
    req_id = random.randint(100000, 999999)
    server = get_target_server(req_id)
    url = f"http://{server}:5000/{endpoint}"
    try:
        import requests
        res = requests.get(url)
        return res.content, res.status_code
    except Exception:
        return jsonify({"message": f"<Error> '/{endpoint}' endpoint does not exist in server replicas", "status": "failure"}), 400

if __name__ == "__main__":
    # Initial servers
    for i in range(1, N+1):
        hostname = f"Server{i}"
        servers[i] = hostname
        spawn_container(hostname, i)
    update_ring()
    app.run(host="0.0.0.0", port=5000)
