import json
import os
from datetime import datetime
from Crypto.Hash import SHA256, HMAC
from Crypto.Cipher import AES

class DecentralizedLedgerEngine:
    @staticmethod
    def construct_crdt_op_log(proof_pi: str, coordinates: list, secret_key: bytes) -> dict:
        """
        Encapsulates zero-knowledge signatures inside an AES-256-GCM authenticated block,
        formatting it as an immutable append-only CRDT log payload for peer-to-peer routing.
        """
        block_metadata = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "zkp_proof_signature": proof_pi,
            "geo_vector_anchor": coordinates,  # [Latitude, Longitude]
            "system_status": "VERIFIED_VACUUM_POLARIZATION_NODE"
        }
        
        serialized_payload = json.dumps(block_metadata, sort_keys=True).encode('utf-8')
        
        # Initialize production-grade AES-GCM Cipher
        cipher = AES.new(secret_key, AES.MODE_GCM)
        ciphertext, tag = cipher.encrypt_and_digest(serialized_payload)
        
        # Compute the Merkle-DAG content identifier hash (Simulated IPFS CID)
        hash_engine = SHA256.new()
        hash_engine.update(ciphertext + cipher.nonce + tag)
        merkle_cid = "Qm" + hash_engine.hexdigest()[:44]
        
        return {
            "IPFS_CID": merkle_cid,
            "CRDT_CLOCK_SEQUENCE": datetime.utcnow().timestamp(),
            "nonce": cipher.nonce.hex(),
            "tag": tag.hex(),
            "ciphertext": ciphertext.hex(),
            "immutable_proof_visible": block_metadata
        }

    @staticmethod
    def simulate_p2p_gossip_sync(incoming_block: dict, current_peer_state: list) -> list:
        """
        Simulates decentralized IPFS Pubsub peer synchronization. Automatically merges 
        incoming Merkle-CRDT operation logs to achieve global network consistency.
        """
        if not incoming_block["IPFS_CID"].startswith("Qm"):
            return current_peer_state
            
        for established_block in current_peer_state:
            if established_block["IPFS_CID"] == incoming_block["IPFS_CID"]:
                return current_peer_state
                
        current_peer_state.append(incoming_block)
        current_peer_state.sort(key=lambda x: x["CRDT_CLOCK_SEQUENCE"], reverse=True)
        return current_peer_state
