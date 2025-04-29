import json
import time
import hashlib
from typing import List, Dict

class Block:
    def __init__(self, index: int, timestamp: float, data: str, previous_hash: str):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self) -> str:
        block_string = json.dumps({
            "index": self.index,
            "timestamp": self.timestamp,
            "data": self.data,
            "previous_hash": self.previous_hash
        }, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain: List[Block] = [self.create_genesis_block()]
        self.difficulty = 4

    def create_genesis_block(self) -> Block:
        return Block(0, time.time(), "Genesis Block", "0")

    def get_latest_block(self) -> Block:
        return self.chain[-1]

    def add_block(self, data: str) -> Block:
        previous_block = self.get_latest_block()
        new_block = Block(
            previous_block.index + 1,
            time.time(),
            data,
            previous_block.hash
        )
        self.chain.append(new_block)
        return new_block

    def is_chain_valid(self) -> bool:
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i-1]

            if current_block.hash != current_block.calculate_hash():
                return False

            if current_block.previous_hash != previous_block.hash:
                return False

        return True

    def find_block_by_data(self, data: str) -> Dict:
        for block in self.chain:
            if block.data == data:
                return {
                    "found": True,
                    "block_index": block.index,
                    "timestamp": block.timestamp,
                    "hash": block.hash
                }
        return {"found": False}

    def save_to_file(self, filename: str = "blockchain.json"):
        with open(filename, 'w') as f:
            chain_data = [{
                "index": block.index,
                "timestamp": block.timestamp,
                "data": block.data,
                "previous_hash": block.previous_hash,
                "hash": block.hash
            } for block in self.chain]
            json.dump(chain_data, f, indent=4)

    @classmethod
    def load_from_file(cls, filename: str = "blockchain.json"):
        try:
            with open(filename, 'r') as f:
                chain_data = json.load(f)
                blockchain = cls()
                blockchain.chain = []
                for block_data in chain_data:
                    block = Block(
                        block_data["index"],
                        block_data["timestamp"],
                        block_data["data"],
                        block_data["previous_hash"]
                    )
                    blockchain.chain.append(block)
                return blockchain
        except FileNotFoundError:
            return cls() 