import hashlib
import time
import json
import random

# ======================
# Block Structure
# ======================
class Block:
    def __init__(self, index, data, prev_hash):
        self.index = index
        self.timestamp = time.time()
        self.data = data
        self.prev_hash = prev_hash
        self.nonce = 0
        self.hash = self.calc_hash()

    def calc_hash(self):
        block_str = json.dumps({
            "index": self.index,
            "timestamp": self.timestamp,
            "data": self.data,
            "prev_hash": self.prev_hash,
            "nonce": self.nonce
        }, sort_keys=True).encode()
        return hashlib.sha256(block_str).hexdigest()

# ======================
# Blockchain (Node)
# ======================
class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis()]

    def create_genesis(self):
        return Block(0, "Genesis Block", "0")

    def setBlock(self, data):
        prev_block = self.chain[-1]
        new_block = Block(len(self.chain), data, prev_block.hash)
        self.chain.append(new_block)
        return new_block

    def getBlock(self, index):
        if 0 <= index < len(self.chain):
            return self.chain[index]
        return None

    def blocksExplorer(self):
        for block in self.chain:
            print(f"Index: {block.index}, Data: {block.data}, Hash: {block.hash}, Prev: {block.prev_hash}, Nonce: {block.nonce}")

    def mineBlock(self, block, difficulty=4):
        target = "0" * difficulty
        while not block.hash.startswith(target):
            block.nonce += 1
            block.hash = block.calc_hash()
        print(f"Block {block.index} mined: {block.hash}")

# ======================
# Decentralized Network Simulation
# ======================
class Network:
    def __init__(self, nodes_count=3):
        # Each node has its own blockchain
        self.nodes = [Blockchain() for _ in range(nodes_count)]

    def broadcastBlock(self, block):
        print("\nBroadcasting block to all nodes...")
        for i, node in enumerate(self.nodes):
            # In a real network, you’d validate the block
            node.chain.append(block)
            print(f"Node {i+1} updated with block {block.index}")

    def showChains(self):
        for i, node in enumerate(self.nodes):
            print(f"\n=== Node {i+1} Blockchain ===")
            node.blocksExplorer()

# ======================
# Testing the system
# ======================
if __name__ == "__main__":
    network = Network(nodes_count=3)

    # Create and mine a block on node 0
    block = network.nodes[0].setBlock("Alice pays Bob 10 coins")
    network.nodes[0].mineBlock(block, difficulty=3)

    # Broadcast to all nodes
    network.broadcastBlock(block)

    # Explorer all nodes
    network.showChains()
