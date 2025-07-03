from flask import Flask, jsonify, request
import docker
import random
import string
from consistent_hash import ConsistentHashMap

app = Flask(__name__)
client = docker.from_env()
hash_map = ConsistentHashMap(num_slots=512, virtual_nodes=9)
server_id_counter = 0
network_name = "load_balancer_network"

def generate_random_hostname():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))

def spawn_server():
    global server_id_counter
    server_id = server_id_counter
    hostname = f"server_{server_id}"
    server_id_counter += 1
    container = client.containers.run(
        "server_image",
        detach=True,
        environment={"SERVER_ID": server_id},
        network=network_name,
        name=hostname
    )
    hash_map.add_server(server_id, hostname)
    return server_id, hostname

# Initialize N=3 servers
for _ in range(3):
    spawn_server()

@app.route('/rep', methods=['GET'])
def get_replicas():
    replicas = list(hash_map.servers.values())
    return jsonify({
        "message": {
            "N": len(replicas),
            "replicas": replicas
        },
        "status": "successful"
    }), 200

@app.route('/add', methods=['POST'])
def add_replicas():
    data = request.get_json()
    n = data.get('n', 0)
    hostnames = data.get('hostnames', [])
    if len(hostnames) > n:
        return jsonify({
            "message": "Error: Length of hostname list is more than newly added instances",
            "status": "failure"
        }), 400
    new_hostnames = []
    for i in range(n):
        hostname = hostnames[i] if i < len(hostnames) else generate_random_hostname()
        server_id, new_hostname = spawn_server()
        new_hostnames.append(new_hostname)
    return jsonify({
        "message": {
            "N": len(hash_map.servers),
            "replicas": list(hash_map.servers.values())
        },
        "status": "successful"
    }), 200

@app.route('/rm', methods=['DELETE'])
def remove_replicas():
    data = request.get_json()
    n = data.get('n', 0)
    hostnames = data.get('hostnames', [])
    if len(hostnames) > n:
        return jsonify({
            "message": "Error: Length of hostname list is more than removable instances",
            "status": "failure"
        }), 400
    # Remove specified hostnames
    for hostname in hostnames:
        for sid, hname in list(hash_map.servers.items()):
            if hname == hostname:
                hash_map.remove_server(sid)
                container = client.containers.get(hostname)
                container.remove(force=True)
                break
    # Remove random hostnames if needed
    remaining = n - len(hostnames)
    if remaining > 0:
        available = list(hash_map.servers.items())
        random.shuffle(available)
        for sid, hostname in available[:remaining]:
            hash_map.remove_server(sid)
            container = client.containers.get(hostname)
            container.remove(force=True)
    return jsonify({
        "message": {
            "N": len(hash_map.servers),
            "replicas": list(hash_map.servers.values())
        },
        "status": "successful"
    }), 200

@app.route('/<path:path>', methods=['GET'])
def route_request(path):
    if path not in ['home', 'heartbeat']:
        return jsonify({
            "message": f"Error: '{path}' endpoint does not exist in server replicas",
            "status": "failure"
        }), 400
    key = random.randint(0, 1000000)  # Simulate request key
    hostname = hash_map.get_server(key)
    if not hostname:
        return jsonify({"message": "No servers available", "status": "failure"}), 500
    try:
        container = client.containers.get(hostname)
        # Simulate request forwarding (in practice, use HTTP client to forward)
        return jsonify({
            "message": f"Hello from Server: {hostname.split('_')[1]}",
            "status": "successful"
        }), 200
    except docker.errors.NotFound:
        hash_map.remove_server(int(hostname.split('_')[1]))
        spawn_server()  # Replace failed server
        return jsonify({"message": "Server failed, replaced", "status": "successful"}), 200

# Heartbeat check to detect failures
def check_heartbeats():
    import threading
    import time
    import requests
    def run():
        while True:
            for sid, hostname in list(hash_map.servers.items()):
                try:
                    response = requests.get(f"http://{hostname}:5000/heartbeat", timeout=5)
                    if response.status_code != 200:
                        raise Exception("Heartbeat failed")
                except:
                    hash_map.remove_server(sid)
                    client.containers.get(hostname).remove(force=True)
                    spawn_server()
            time.sleep(5)
    threading.Thread(target=run, daemon=True).start()

check_heartbeats()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)