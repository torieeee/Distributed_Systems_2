class ConsistentHashMap:
    def __init__(self, num_slots=512, virtual_nodes=9):
        self.num_slots = num_slots
        self.virtual_nodes = virtual_nodes
        self.ring = [None] * num_slots
        self.servers = {}

    def hash_request(self, key):
        # H(i) = i + 2i + 2172
        return (key + 2 * key + 2172) % self.num_slots

    def hash_virtual_node(self, server_id, virtual_id):
        # Φ(i, j) = i + j + 2j + 25
        return (server_id + virtual_id + 2 * virtual_id + 25) % self.num_slots

    def add_server(self, server_id, hostname):
        if server_id not in self.servers:
            self.servers[server_id] = hostname
            for v in range(self.virtual_nodes):
                slot = self.hash_virtual_node(server_id, v)
                while self.ring[slot] is not None:
                    slot = (slot + 1) % self.num_slots  # Linear probing
                self.ring[slot] = (server_id, hostname)

    def remove_server(self, server_id):
        if server_id in self.servers:
            hostname = self.servers.pop(server_id)
            for v in range(self.virtual_nodes):
                slot = self.hash_virtual_node(server_id, v)
                while self.ring[slot] is not None and self.ring[slot][0] == server_id:
                    self.ring[slot] = None
                    slot = (slot + 1) % self.num_slots

    def get_server(self, key):
        slot = self.hash_request(key)
        original_slot = slot
        while True:
            if self.ring[slot] is not None:
                return self.ring[slot][1]  # Return hostname
            slot = (slot + 1) % self.num_slots
            if slot == original_slot:
                break
        return None  # No server available