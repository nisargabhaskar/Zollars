

import datetime as _dt
import hashlib as _hashlib
import json as _json

class Blockchain:
    def __init__(self)-> None:#none is written to mention that the return type of init is none as it is supposed to be
        self.chain = list()

    def mine_block(self,data: str) -> dict:
        previous_block = self.get_previous_block()
        previous_proof = previous_block["proof"]
        index = previous_block["index"] + 1 
        proof = self._proof_of_work(previous_proof = previous_proof, index = index, data = data)
        previous_hash = self._hash(block =previous_block)
        block = self._create_block(data = data, proof = proof, previous_hash = previous_hash, index = index , timestamp = str(_dt.datetime.now()))
        self.chain.append(block)
        return block
    
    def _hash(self, block : dict) -> str:
        encoded_block = _json.dumps(block,sort_keys = True).encode()
        return _hashlib.sha256(encoded_block).hexdigest()

    def _to_digest(self,new_proof:int, previous_proof:int,index: int,data :str) -> bytes:
        to_digest = str(new_proof**3 - (previous_proof**2)*index) + data
        return to_digest.encode()

    def _proof_of_work(self,previous_proof:int,index:int,data:str)-> int :
        new_proof = 1
        checkproof = False
        while not checkproof:
            to_digest = self._to_digest(new_proof=new_proof, previous_proof = previous_proof, index = index, data = data)
            hash_value = _hashlib.sha256(to_digest).hexdigest()
            if hash_value[:4] == "0001":
                checkproof = True
            else :
                new_proof += 1
        return new_proof

    def get_previous_block(self)-> dict :
        return self.chain[-1]

    def _create_block(self,data: str,proof: int,previous_hash: str, index: int,timestamp :str) -> dict:
        block = {
            "index" : index,
            "timestamp" : timestamp,
            "data" : data,
            "proof" : proof,
            "previous_hash" : previous_hash,
        }
        return block

    def is_chain_valid(self) ->bool :
        current_block = self.chain[0]
        block_index = current_block.get("index")
        while block_index < len(self.chain) :
            next_block = self.chain[block_index]
            if next_block["previous_hash"] != self._hash(current_block):
                return False
            current_proof = current_block["proof"]
            next_index,next_data,next_proof = next_block["index"],next_block["data"],next_block["proof"]
            hash_value = _hashlib.sha256(self._to_digest(new_proof = next_proof, previous_proof = current_proof, index = next_index, data = next_data)).hexdigest()
            if hash_value[:4] != "0001":
                return False
            current_block = next_block
            block_index += 1
        return True
